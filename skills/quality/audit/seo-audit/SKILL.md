---
name: seo-audit
description: "Audit page SEO: meta tags, structured data, Open Graph, canonicals, and heading hierarchy"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /seo-audit
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl"]
      env: []
      os: ["darwin"]
---

# SEO Audit Skill

Audit a page or set of pages for SEO health across six categories. Each category is independently scored, then combined into a single weighted overall score. Report blocking issues first, then scored findings, then recommendations.

---

## Meta Tags (30% weight)

Check each of the following. Any missing item is a finding.

- **Title tag** — present; length 50–60 characters; contains primary keyword
- **Meta description** — present; length 150–160 characters; unique per page; compelling enough to drive click-through
- **Viewport meta** — `<meta name="viewport" content="width=device-width, initial-scale=1">` present
- **Charset declaration** — `<meta charset="utf-8">` present, placed before title
- **Robots meta** — present; value is `index, follow` unless the page is intentionally excluded from indexing; flag any unintentional `noindex`

---

## Open Graph & Social (20% weight)

- **og:title** — present; matches or closely relates to the title tag
- **og:description** — present; 155–200 characters recommended
- **og:image** — present; dimensions ≥ 1200×630 px; hosted on same domain or CDN (not third-party)
- **og:url** — present; matches the canonical URL exactly
- **og:type** — set to an appropriate value (`website`, `article`, `event`, etc.)
- **Twitter card tags** — `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` all present
- **Twitter card type** — `summary_large_image` for content pages; `summary` acceptable for utility pages

---

## Structured Data (15% weight)

- **JSON-LD block** — at least one `<script type="application/ld+json">` block present in `<head>` or `<body>`
- **Schema type** — `@type` is appropriate for the page context:
  - Homepage → `Organization` or `WebSite`
  - Blog post / article → `Article` or `BlogPosting`
  - Event page → `Event`
  - General content page → `WebPage`
- **Required properties populated** — at minimum: `name`, `description`, `url`
- **Schema.org validity** — no unknown properties; required fields for the chosen type are present; validate against schema.org spec (use Google's Rich Results Test or schema.org validator output if available)
- **No conflicting schema blocks** — multiple JSON-LD blocks allowed; they must not contradict each other on `@type` or `url`

---

## URL & Canonical (15% weight)

- **Canonical tag** — `<link rel="canonical" href="...">` present in `<head>`
- **Canonical URL correct** — canonical href matches the live URL of the page (no redirects, no www/non-www mismatch)
- **No duplicate canonical declarations** — exactly one canonical tag per page
- **Clean URL structure** — no query parameters that define unique content (e.g., `?page=blog-post`); use path-based URLs for content pages
- **Trailing slash consistency** — canonical URL and all internal links to this page use the same trailing slash convention; flag inconsistencies

---

## Heading Hierarchy (10% weight)

- **Single h1** — exactly one `<h1>` per page; flag if zero or more than one
- **Logical heading order** — headings descend without skipping levels (h1 → h2 → h3; never h1 → h3 directly)
- **h1 relates to title tag** — h1 text matches or semantically aligns with the title tag; they need not be identical
- **Keywords in headings** — h1 and at least one h2 contain the primary or secondary target keyword; do not force-insert keywords; flag only if headings are entirely generic

---

## Image SEO (10% weight)

- **Alt text on all images** — every `<img>` has a non-empty `alt` attribute; decorative images may use `alt=""` but must be intentional
- **Descriptive alt text** — alt text describes the image content and, where natural, includes a keyword; flag placeholder values (`image`, `photo`, `IMG_001`)
- **Descriptive file names** — image file names use descriptive slugs (e.g., `retreat-ceremony-altar.jpg`); flag numeric or camera-generated names
- **Dimension attributes** — `width` and `height` attributes present on all `<img>` elements (required for Cumulative Layout Shift prevention)
- **No oversized images** — compare the image's intrinsic dimensions against its displayed (CSS) dimensions; flag images where intrinsic size is more than 2× the display size

---

## Scoring

### Per-category score (0–100)

Count the checks in each category. Score = (checks passing / total checks) × 100. Apply partial credit where a check is partially met (e.g., title present but wrong length = 50% credit on that check).

### Weighted overall score

| Category | Weight |
|---|---|
| Meta Tags | 30% |
| Open Graph & Social | 20% |
| Structured Data | 15% |
| URL & Canonical | 15% |
| Heading Hierarchy | 10% |
| Image SEO | 10% |

Overall = sum of (category score × weight).

### Grade thresholds

| Score | Grade |
|---|---|
| 90–100 | A — Production ready |
| 75–89 | B — Minor fixes recommended |
| 60–74 | C — Several issues to resolve |
| Below 60 | D — Significant work required |

### Blocking issues (must fix before any deploy)

The following findings block a passing audit regardless of overall score:

1. Missing title tag
2. Missing canonical tag
3. Missing or duplicate h1

Flag blocking issues at the top of the audit report before the scored breakdown.

---

## Audit Report Format

```
# SEO Audit — <Page URL>
Audited: <date>

## Blocking Issues
- [ ] <issue> — <fix required>

## Overall Score: <score>/100 (<grade>)

## Category Breakdown
| Category              | Score | Weight | Contribution |
|-----------------------|-------|--------|--------------|
| Meta Tags             | xx/100 | 30%   | xx.x         |
| Open Graph & Social   | xx/100 | 20%   | xx.x         |
| Structured Data       | xx/100 | 15%   | xx.x         |
| URL & Canonical       | xx/100 | 15%   | xx.x         |
| Heading Hierarchy     | xx/100 | 10%   | xx.x         |
| Image SEO             | xx/100 | 10%   | xx.x         |

## Findings by Category

### Meta Tags
- PASS/FAIL/WARN — <check name>: <detail>

### Open Graph & Social
...

## Recommended Fix Order
1. <blocking issue — highest priority>
2. <highest-weight failing check>
...
```

---

## Issue Routing

All SEO issues identified by this audit are routed to **Nova** (frontend engineer, `agents/frontend/engineer`).

- Provide Nova with the full audit report
- Include the specific file paths affected (e.g., `web/src/app/page.tsx`, `web/src/app/layout.tsx`)
- For structured data issues, include the current JSON-LD block and the corrected version
- For image issues, include the file path and both intrinsic and display dimensions

Nova owns implementation. This skill owns validation only — do not implement fixes directly.
