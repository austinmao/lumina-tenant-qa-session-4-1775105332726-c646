---
name: website-testing
description: "Audit website pages for accessibility, performance, brand consistency, and SEO compliance"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /website-testing
metadata:
  openclaw:
    emoji: "🧪"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Website Testing

Test built website pages for accessibility, performance, brand consistency, and SEO compliance. This is an evaluator skill -- it tests what other agents built and produces structured audit reports. The generator/evaluator separation is a core principle: builders build, this skill tests.

## When to Use

- Auditing a built page before deployment
- Running the full QA suite (accessibility, performance, brand, SEO) on a page
- Producing structured audit reports for remediation tracking
- Validating that fixes have resolved previously reported issues

## Context Loading

Before any audit:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/asset-checklist.md` for brand compliance gates
3. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Audit Categories

Every page gets all four categories checked, even if the request only mentions one. Never skip an audit category.

### 1. Accessibility (WCAG AA)
- Color contrast ratios (4.5:1 normal text, 3:1 large text/UI)
- Keyboard navigation (tab order, focus indicators, no keyboard traps)
- Screen reader compatibility (alt text, ARIA labels, heading hierarchy)
- Touch targets (minimum 44x44px)
- Form labeling and error messaging
- Motion/animation reduced-motion support

**Hard gate**: Never approve a page that has any `critical` or `major` accessibility failure. WCAG AA is a hard gate, not a suggestion.

### 2. Performance
- Core Web Vitals (LCP, CLS, INP) against thresholds
- Page weight and resource optimization
- Image format and compression
- JavaScript bundle analysis
- Third-party script impact

### 3. Brand Consistency
- Design tokens match the approved design spec
- Logo usage follows brand guide
- Typography matches brand fonts and hierarchy
- Color usage within brand palette
- Spacing and layout consistency with other pages

### 4. SEO Compliance
- Schema markup present and valid
- Meta tags (title, description, OG tags) complete
- URL structure matches taxonomy
- Heading hierarchy (single H1, logical H2-H6 order)
- Internal linking structure
- Image alt text present and descriptive

## Issue Severity

| Severity | Criteria |
|---|---|
| `critical` | WCAG AA violation, broken functionality, security issue |
| `major` | Significant brand deviation, missing schema markup, performance regression |
| `minor` | Style inconsistency, non-blocking improvement opportunity |

## Report Format

```
## QA Audit — [page name]

**Verdict**: pass | conditional-pass | fail
**Issues**: [total] ([critical] critical, [major] major, [minor] minor)

### Accessibility
| Check | Status | Expected | Actual | Owner |
|---|---|---|---|---|

### Performance
| Check | Status | Expected | Actual | Owner |
|---|---|---|---|---|

### Brand Consistency
| Check | Status | Expected | Actual | Owner |
|---|---|---|---|---|

### SEO Compliance
| Check | Status | Expected | Actual | Owner |
|---|---|---|---|---|
```

### Clean Pass
"QA audit complete. All checks passed. Page is clear for deployment."

### Summary for Orchestrator
One-line summary per page with verdict and blocker count. Detail available on request.

## Routing Remediation

Issues are routed to the responsible owner:
- Accessibility and performance issues -> Frontend Engineer
- Brand consistency issues -> Creative Director
- SEO issues -> SEO/GEO Strategist

Track remediation status until all issues are resolved.

## Boundaries

- Never fix code, modify designs, or write content. Produce audit reports only.
- Never approve a page for production deployment. Report audit results to the orchestrator.
- Never skip an audit category.

## Dependencies

- `performance-audit` -- detailed Core Web Vitals analysis
- `brand-review-gate` -- brand compliance checking
- `seo-monitoring` -- SEO compliance validation

## State Tracking

- `auditReports` -- keyed by page slug: audit date, verdict, issue counts by severity, remediation status
- `openIssues` -- active issues awaiting remediation with owner and deadline
- `baselineMetrics` -- Core Web Vitals baselines per page for regression detection
