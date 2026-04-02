---
name: generate-schema-markup
description: "Generate JSON-LD structured data for a page / add schema markup"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "🏷️"
    requires:
      os: ["darwin"]
---

# Schema Markup Generator Skill

Generates JSON-LD structured data for website pages. Reads page content and brand context to populate schema fields accurately.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `domain`, `brand_root`, and `site_dir` from site context.
3. Read brand identity from `<brand_root>/brand-guide.md` for Organization schema fields.

---

## Supported Schema Types

| Type | When to use |
|---|---|
| **Organization** | Homepage or about page |
| **Person** | Team member or founder profile page |
| **Article** | Blog posts, news articles |
| **FAQ** | FAQ page or page with Q&A sections |
| **HowTo** | Step-by-step guide or tutorial page |
| **Event** | Retreat, workshop, webinar, or event listing page |
| **BreadcrumbList** | Any page with navigation breadcrumbs |
| **WebSite** | Homepage (with SearchAction if site has search) |

---

## Steps

1. User specifies the page path and schema type (or ask which type if unclear).
2. Read the page content from `<site_dir>/<page_path>` to extract:
   - Page title, description, headings, content sections.
   - Dates, locations, prices (for Event type).
   - Questions and answers (for FAQ type).
   - Steps (for HowTo type).
3. Read brand context for organization name, logo URL, social profiles, contact info.
4. Generate valid JSON-LD wrapped in `<script type="application/ld+json">`.
5. Validate required fields per schema.org spec for the chosen type.
6. Present the JSON-LD block and recommend where to place it (usually in `<head>` or page layout).

---

## Output

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "<Type>",
  ...fields...
}
</script>
```

Include a brief note explaining which fields were populated and any fields that need manual review (e.g., dates, prices).

---

## Guidelines

- Always use `https://` URLs, never `http://`.
- Use the canonical domain from site context for all URLs.
- For `Event` type: include `startDate`, `endDate`, `location`, and `offers` if available.
- For `FAQ` type: each Q&A must have both `acceptedAnswer` and `name`.
- For `Article` type: include `author`, `datePublished`, `dateModified`, `image`.
- Never fabricate dates, prices, or factual claims -- flag missing data for manual entry.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If page file does not exist: report the expected path and stop.
- If required schema fields cannot be extracted from content: list the missing fields and ask user to provide them.
