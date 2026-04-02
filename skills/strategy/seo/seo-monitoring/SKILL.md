---
name: seo-monitoring
description: "Monitor SEO health with technical audits, schema markup validation, and redirect management"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /seo-monitoring
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# SEO Monitoring

Monitor ongoing SEO health across the active site. This is a cross-cutting skill that participates in research, architecture, content review, QA, and post-launch monitoring phases. It provides technical SEO audits, schema markup validation, meta optimization checks, redirect map management, and cannibalization detection.

## When to Use

- Running a technical SEO audit on the active site
- Validating schema markup on built pages
- Checking meta tags (title, description, OG tags) for optimization
- Managing the redirect map after URL changes
- Detecting keyword cannibalization between pages

## Context Loading

Before any SEO monitoring work:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/messaging.md` and `<brand_root>/content-system.md` for keyword context
3. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Monitoring Areas

### 1. Technical SEO Audit
- **Crawlability** -- robots.txt, sitemap.xml, noindex/nofollow tags
- **Indexation** -- pages indexed vs. expected, orphan pages
- **Page speed** -- Core Web Vitals integration (defer to `performance-audit` for detailed analysis)
- **Mobile-friendliness** -- responsive design, viewport configuration
- **SSL/HTTPS** -- mixed content, certificate validity
- **Canonical tags** -- correct self-referencing, cross-domain canonicals

### 2. Schema Markup Validation
- JSON-LD structured data present on appropriate pages
- Schema types match page content (Organization, Event, FAQ, Course, Article, etc.)
- Required properties populated with accurate data
- Schema validates against Google's Rich Results Test requirements

Output format: JSON-LD blocks with the target page and expected rich result type noted.

### 3. Meta Optimization
Per-page meta tag review:
- **Title tag** -- includes primary keyword, under 60 characters, unique across site
- **Meta description** -- includes primary keyword, under 160 characters, compelling click trigger
- **OG tags** -- og:title, og:description, og:image populated for social sharing
- Character counts and keyword placement noted

### 4. Redirect Map Management
Maintain the site's redirect map:
- Every URL change requires a corresponding redirect entry
- Track redirect chains (no chain longer than 3 hops)
- Validate that redirects resolve to 200 status pages
- Flag redirect loops

### 5. Cannibalization Detection
Identify pages competing for the same keywords:
- Pages with overlapping primary keyword targets
- Pages with similar title tags or meta descriptions
- Internal linking that sends conflicting signals
- Recommended resolution: consolidate, differentiate, or canonical

## Report Format

### Technical SEO Audit
```
## SEO Audit — [site] — [date]

### Crawlability
| Check | Status | Details |
|---|---|---|

### Indexation
| Page Count | Expected | Indexed | Gap |
|---|---|---|---|

### Issues
| Issue | Severity | Affected Pages | Recommendation |
|---|---|---|---|
```

### Schema Markup Spec
```json
{
  "@context": "https://schema.org",
  "@type": "[type]",
  // ... properties
}
```
With target page and expected rich result type noted.

### Meta Optimization
Per-page table: title tag, meta description, OG tags, character counts, keyword placement.

## Boundaries

- Never write primary page copy. Provide keyword targets and meta optimization; the Copywriter writes the copy.
- Never modify page designs, wireframes, or production code. Advise; other agents implement.
- Never implement schema markup directly in code. Produce the specification; the Frontend Engineer implements.
- Every recommendation must serve both search engines and human visitors. Reject any technique that degrades user experience for ranking gain.

## State Tracking

- `keywordTargets` -- keyed by page slug: primary keyword, secondary keywords, search volume, last updated
- `redirectMap` -- array of old URL to new URL mappings with reason and implementation status
- `schemaMarkup` -- keyed by page slug: schema type, status (`spec` | `implemented` | `verified`)
- `seoIssues` -- array of active issues with severity, affected pages, and resolution status
