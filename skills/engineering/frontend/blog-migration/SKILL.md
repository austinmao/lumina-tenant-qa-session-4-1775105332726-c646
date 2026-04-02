---
name: blog-migration
description: "Migrate blog posts from Squarespace / migrate blog posts from [path/to/export.xml] / migrate blog posts from [path/to/export.json] / convert blog posts to MDX / import blog from WordPress"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /migrate-blog
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["python3", "jq"]
      os: ["darwin"]
---

# Blog Migration Skill

Converts a Squarespace/WordPress WXR XML export or Ghost/Contentful JSON export into MDX files at `web/src/data/blog/`, runs brand and compliance audit on each post, and generates redirect entries for the blueprint redirect map.

**Export file path MUST be supplied as a trigger parameter. Never hardcoded.**

## Trigger Phrases

- `/migrate-blog ~/Downloads/export.xml`
- `/migrate-blog ~/Downloads/export.json`
- "migrate blog posts from [path/to/export.xml]"
- "migrate blog posts from [path/to/export.json]"
- "import blog from Squarespace"
- "convert blog posts to MDX"

## Supported Export Formats

| Extension | Format | Source Platforms |
|---|---|---|
| `.xml` | WXR (WordPress eXtended RSS 1.x/2.x) | Squarespace, WordPress, Ghost XML |
| `.json` | Normalized JSON | Ghost JSON, Contentful, custom exports |

Format is auto-detected from the file extension of the path provided.

---

## Algorithm

### Step 1 — Accept and validate export file path

Accept export file path as a trigger parameter (e.g., `/migrate-blog ~/Downloads/export.xml`).

If no path provided:
> "Please provide the export file path. Usage: /migrate-blog [path/to/export.xml] or /migrate-blog [path/to/export.json]"

Stop here.

If file does not exist at the expanded path:
> "File not found: [path]. Check the path and try again."

Stop here.

Detect format from extension:
- `.xml` → WXR mode
- `.json` → JSON mode
- Other → "Unsupported file extension. Provide a .xml (WXR) or .json export file."

### Step 2 — Parse export and extract posts

**WXR/XML mode:**

```python
import xml.etree.ElementTree as ET

tree = ET.parse(export_path)
root = tree.getroot()

ns = {
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wp': 'http://wordpress.org/export/1.2/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'excerpt': 'http://wordpress.org/export/1.0/excerpt/',
}

items = root.findall('.//item')
posts = []
for item in items:
    post_type = item.findtext('wp:post_type', namespaces=ns)
    status = item.findtext('wp:status', namespaces=ns)
    if post_type != 'post' or status != 'publish':
        continue  # skip pages, attachments, drafts
    posts.append(item)
```

**JSON mode:**

Parse the JSON file. Detect schema variant:
- Ghost JSON: look for `data.posts` array
- Contentful JSON: look for `entries` array with `sys.contentType.sys.id == "blogPost"`
- Custom: look for top-level `posts` array

Extract each post entry. Skip drafts (`status != "published"` or equivalent).

### Step 3 — Normalize to internal schema

For each post, map to the normalized internal schema regardless of source format:

| Field | WXR/XML source | JSON source |
|---|---|---|
| `title` | `<title>` | `title` |
| `slug` | `<wp:post_name>` or derived from `<link>` | `slug` or derived from `title` |
| `date` | `<pubDate>` (RFC2822) converted to ISO | `published_at` or `created_at` |
| `author` | `<dc:creator>` | `primary_author.name` or `author` |
| `body_html` | `<content:encoded>` (CDATA) | `html` or `mobiledoc` rendered to HTML |
| `categories` | `<category domain="category">` tags | `tags` filtered to category type |
| `tags` | `<category domain="post_tag">` tags | `tags` filtered to tag type |
| `excerpt` | `<excerpt:encoded>` or first 160 chars of body | `custom_excerpt` or first 160 chars |

Slug generation (if not explicit):
- Lowercase the title
- Replace spaces and special chars with hyphens
- Strip leading/trailing hyphens

### Step 4 — Convert HTML body to MDX

Apply these conversion rules in order:

1. **Images**: `<img src="..." alt="...">` → `![alt](src)`
2. **Headings**: `<h1>` → `#`, `<h2>` → `##`, etc.
3. **Bold/Italic**: `<strong>` → `**`, `<em>` → `*`
4. **Links**: `<a href="...">text</a>` → `[text](url)`
5. **Blockquotes**: `<blockquote>` → `> ` prefix
6. **Ordered lists**: `<ol><li>` → `1. ` numbered items
7. **Unordered lists**: `<ul><li>` → `- ` items
8. **Code**: `<code>` → backtick inline, `<pre>` → fenced code block
9. **Line breaks**: `<br>` → newline; `<p>` → double newline
10. **Strip**: remove all remaining HTML tags; decode HTML entities
11. **Squarespace artifacts**: remove `[gallery type="..." ids="..."]` shortcodes; remove `<!-- more -->` markers

### Step 5 — Build MDX frontmatter

```yaml
---
title: "Post Title"
slug: "post-slug"
date: "2024-01-15"
author: "Austin Mao"
categories:
  - "Category Name"
excerpt: "First 160 characters of content or manual excerpt"
brand_audit:
  status: "pass"      # pass | flagged
  violations: []      # list of violation strings if flagged
  severity: "low"     # low | medium | high (only present if flagged)
migrated_from: "https://[the organization's domain]/blog/original-slug"
---
```

### Step 6 — Run brand-standards + compliance-audit

For each post, invoke `brand-standards` and `compliance-audit` skills on the body content.

Flag violations in the frontmatter `brand_audit` section:
- `status: "flagged"` if any violations found
- List each violation string in `violations`
- Set `severity` to highest severity found across all violations

Log flagged posts to stdout: `FLAGGED: /blog/[slug] — [N violations, highest severity: X]`

### Step 7 — Write MDX files

Write each post to `web/src/data/blog/[slug].mdx` with:
- Complete frontmatter from Step 5 (including brand_audit results from Step 6)
- MDX body from Step 4

If a file already exists at `web/src/data/blog/[slug].mdx`:
- Log: `SKIPPED (exists): /blog/[slug]` — do not overwrite
- Count as skipped in summary

### Step 8 — Generate redirect entries

For each successfully migrated post, generate a redirect entry:

```yaml
- old: "/blog/original-slug"
  new: "/blog/migrated-slug"
  type: 301
  source: "squarespace-export"
  notes: "Blog post migrated — slug preserved"
```

If the new slug differs from the original slug, update the `notes` field:
```yaml
  notes: "Blog post migrated — slug changed from 'original-slug' to 'migrated-slug'"
```

Append all redirect entries to the `redirects` section in `docs/website/blueprint.md`.

### Step 9 — Output summary

```
Blog Migration Complete — YYYY-MM-DD

Export: [path/to/export.xml] (WXR format)
Total items in export: 390
Blog posts extracted: 312
Skipped (not published): 45
Skipped (not post type): 33

Migrated: 308
Skipped (already exists): 4

Brand audit:
  Passed: 285
  Flagged (low):    18
  Flagged (medium):  4
  Flagged (high):    1

Redirects generated: 308 (appended to docs/website/blueprint.md)

Run `grep "flagged" web/src/data/blog/*.mdx` to review brand violations.
```

---

## Error Handling

| Condition | Response |
|---|---|
| No export path provided | Usage instructions; stop |
| File not found | "File not found: [path]"; stop |
| Unsupported extension | "Unsupported file extension"; stop |
| XML parse error | "XML parse failed at line N: [error]. Check the export file is valid WXR." |
| JSON parse error | "JSON parse failed: [error]. Check the export file is valid JSON." |
| Unknown JSON schema | "Unknown JSON schema. Expected `data.posts`, `entries`, or `posts` array." |
| File write permission denied | "Cannot write to web/src/data/blog/ — check directory permissions" |
| `docs/website/blueprint.md` missing | Create it first with the redirect map section stub |

---

## Constitution Check

- **Principle I (Human-in-the-Loop)**: Local file writes only (no external sends). Autonomous OK.
- **Principle III (Security)**: Reads only the file path supplied at trigger time. No network access.
- **Principle IV (Brand and Voice)**: brand-standards + compliance-audit run on every post.
- **Principle V (Transparency)**: Summary output lists all counts and flagged violations.

## Notes

- Squarespace exports use WXR 1.2 format — parse with `http://wordpress.org/export/1.2/` namespace
- `web/src/data/blog/` must exist before migration; create with `mkdir -p web/src/data/blog/`
- Slug conflicts are resolved by keeping the first file (most recent export wins on re-run)
- HTML entity decoding: `&amp;` → `&`, `&lt;` → `<`, `&gt;` → `>`, `&nbsp;` → space, `&mdash;` → —
- Squarespace exports may include image attachments as `<item>` elements with `wp:post_type = attachment` — skip these
