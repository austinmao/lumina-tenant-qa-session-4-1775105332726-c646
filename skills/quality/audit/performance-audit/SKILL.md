---
name: performance-audit
description: "Audit Core Web Vitals, page weight, and performance metrics with regression detection"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /performance-audit
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Performance Audit

Run performance checks against Core Web Vitals and supplementary metrics, producing structured reports that flag regressions against previous baselines. This skill monitors, compares, and reports -- it never modifies site code or configuration.

## When to Use

- Running a weekly performance check on the active site
- Measuring Core Web Vitals for key pages
- Detecting performance regressions between check cycles
- Auditing page weight, JavaScript bundle size, and third-party script impact

## Context Loading

Read `memory/site-context.yaml` to determine the active site domain. If it does not exist, respond: "No active site set. Run `/site <name>` first." and stop.

Only monitor the single active site domain. Never scan or benchmark domains outside the active site.

## Core Web Vitals

Measure for every key page:

| Metric | Good Threshold | Description |
|---|---|---|
| LCP (Largest Contentful Paint) | <= 2.5s | Loading performance |
| CLS (Cumulative Layout Shift) | <= 0.1 | Visual stability |
| INP (Interaction to Next Paint) | <= 200ms | Interactivity responsiveness |

Report each metric with its score and whether it passes Google's "good" threshold.

## Regression Detection

Compare every metric against the previous report:
- Any metric that worsened by more than 10% is flagged as a regression
- Any metric that crossed from "good" to "needs improvement" (or worse) is flagged as a critical regression
- Report the delta (previous value, current value, percentage change)

## Supplementary Metrics

Check additional performance signals:
- **Total page weight** -- combined size of all resources
- **Image optimization** -- format (WebP/AVIF preferred), compression level, appropriate dimensions
- **JavaScript bundle size** -- total JS payload and per-bundle breakdown
- **Third-party scripts** -- count, blocking impact, and load contribution
- **Font loading** -- strategy (swap/optional/block) and total font weight

## Report Format

### Scorecard
```
## Performance Scorecard — [date]

| Metric | Value | Status | Delta |
|---|---|---|---|
| LCP | [value] | [pass/fail] | [+/-N% vs previous] |
| CLS | [value] | [pass/fail] | [+/-N% vs previous] |
| INP | [value] | [pass/fail] | [+/-N% vs previous] |

**Overall grade**: [A-F based on CWV pass rate]
```

### Regressions Section
For each regression: metric name, previous value, current value, delta percentage, affected page(s).

### Supplementary Metrics
Summary table with regressions highlighted.

### Clean Report
"Performance check complete. All CWV passing. No regressions vs. previous report."

## Notification Rules

- Alert the user only when:
  - A Core Web Vital crosses from "good" to "needs improvement" or worse
  - Total page weight increases by more than 20%
- All other findings stay in the report file only
- Write reports to `memory/logs/performance/YYYY-MM-DD.md`
- If a report for today already exists, append a timestamped section

## Boundaries

- Never modify website code, configuration, assets, or deployment settings. Read-only.
- Never auto-fix performance issues. Report findings with context and severity for human triage.
- Never scan or benchmark domains outside the active site.

## State Tracking

- `lastCheckDate` -- ISO 8601 timestamp of most recent completed check
- `previousBaseline` -- CWV scores and supplementary metrics from the last report (for regression comparison)
- `pagePerformanceHistory` -- per-page CWV trends over recent checks (rolling 4-week window)
- `acknowledgedRegressions` -- regressions reviewed and accepted (not re-flagged)
