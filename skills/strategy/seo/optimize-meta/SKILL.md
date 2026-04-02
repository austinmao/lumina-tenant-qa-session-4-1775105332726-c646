---
name: optimize-meta
description: "Optimize page title and meta description / improve snippet targeting"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "✏️"
    requires:
      os: ["darwin"]
---

# Meta Optimization Skill

Reviews and optimizes page titles, meta descriptions, and heading hierarchy for search engine visibility and featured snippet targeting.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `domain`, `brand_root`, and `site_dir` from site context.
3. Read `<brand_root>/voice.md` or `<brand_root>/brand-guide.md` for brand-aligned language and messaging guidelines.

---

## Steps

### 1. Current state audit

1. Accept a page path from the user (or audit all pages if requested).
2. Read the page source from `<site_dir>/<page_path>`.
3. Extract current: `<title>`, `<meta name="description">`, `<h1>`, `<h2>`-`<h6>` hierarchy.

### 2. Title optimization

- Target: under 60 characters (Google truncates at ~60).
- Include the primary keyword near the beginning.
- Include the brand name at the end when space allows (e.g., "Page Topic | Brand").
- Avoid keyword stuffing -- one primary keyword, natural phrasing.
- Present: current title, character count, proposed title, character count.

### 3. Meta description optimization

- Target: 120-155 characters (Google truncates at ~155).
- Include the primary keyword naturally.
- Include a clear value proposition or call to action.
- Use active voice aligned with the brand guide's messaging.
- Present: current description, character count, proposed description, character count.

### 4. Heading hierarchy review

- Verify exactly one `<h1>` that includes the primary keyword.
- Check heading levels are sequential (no skipping h2 -> h4).
- Suggest improvements for headings that could better target related keywords.

### 5. Featured snippet targeting

For pages with informational intent:
- Identify snippet-eligible structures: definition paragraphs, numbered lists, comparison tables.
- Suggest content format changes to increase snippet eligibility.
- Recommend adding a concise answer paragraph (40-60 words) directly after the target heading.

---

## Output

```markdown
## Meta Optimization — <page_path>
Site: <domain> | Date: YYYY-MM-DD

### Title
| | Value | Chars |
|---|---|---|
| Current | ... | XX |
| Proposed | ... | XX |

### Meta Description
| | Value | Chars |
|---|---|---|
| Current | ... | XXX |
| Proposed | ... | XXX |

### Heading Hierarchy
[Current hierarchy with issues flagged]

### Snippet Opportunities
[Recommended content structure changes]
```

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If page file does not exist: report the expected path and stop.
- If brand guide is not found: proceed without brand constraints but note this in the output.
