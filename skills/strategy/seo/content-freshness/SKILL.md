---
name: content-freshness
description: "Scan deployed pages for stale content, broken links, outdated statistics, and missing images"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /content-freshness
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["curl"]
      env: []
      os: ["darwin"]
---

# Content Freshness

Run freshness scans on deployed website pages, detecting stale content, broken links, outdated statistics, missing images, and dead external references. This skill produces reports for human review -- it never auto-fixes content.

## When to Use

- Running a daily or weekly freshness scan of the active site
- Checking for stale dates, statistics, or testimonial attributions
- Detecting broken internal and external links
- Identifying missing images or dead references

## Context Loading

Read `memory/site-context.yaml` to determine the active site domain and sitemap. If it does not exist, respond: "No active site set. Run `/site <name>` first." and stop.

Only monitor the single active site domain from site context. Never scan domains not listed as active.

## Scan Categories

### 1. Stale Content Detection
Flag any page content with:
- Dates older than 90 days
- Statistics referencing prior years
- Testimonials with stale attribution
- Outdated pricing or capacity numbers
- References to past events as upcoming

Report each finding with: page URL, stale element, current age.

### 2. Broken Link Detection
Check every internal link and external reference:
- HTTP 4xx/5xx responses
- DNS failures
- Redirect chains longer than 3 hops
- Timeout failures

Report broken links grouped by page.

### 3. Missing Image Detection
Check for:
- Broken `src` attributes
- 404 responses on image URLs
- Missing alt text (accessibility)

Report each with page URL and image path.

## Issue Severity

| Severity | Criteria |
|---|---|
| `high` | Customer-facing and clearly wrong (broken CTA link, wrong pricing, 404 hero image) |
| `medium` | Ambiguous or partially stale (date from 4 months ago, redirect chain) |
| `low` | Minor (slightly outdated stat, non-critical external link) |

## Report Format

```
# Freshness Report — [date]

## Summary
- Pages scanned: [N]
- Issues found: [N] (high: [N], medium: [N], low: [N])

## High Severity
| Page | Issue Type | Element | Details |
|---|---|---|---|

## Medium Severity
...

## Low Severity
...
```

Issue types: `stale-date` | `broken-link` | `missing-image` | `dead-reference` | `outdated-stat`

When no issues are found: "Freshness scan complete. 0 issues across N pages."

## Notification Rules

- Alert the user only when high-severity issues are found
- Medium and low findings stay in the report file only
- Write reports to `memory/logs/freshness/YYYY-MM-DD.md`
- If a report for today already exists, append a timestamped section rather than overwriting

## Boundaries

- Never modify, edit, or delete any website content, page, or asset. Read-only.
- Never auto-fix stale content, broken links, or missing images. Report findings for human triage.
- Never crawl or scan domains outside the active site.

## State Tracking

- `lastScanDate` -- ISO 8601 timestamp of most recent completed scan
- `knownIssues` -- issue fingerprints from previous scan (for tracking resolution vs. new regressions)
- `pageInventory` -- list of pages scanned with last-scanned timestamp per page
- `suppressedFindings` -- issues acknowledged and marked as acceptable (not re-reported)
