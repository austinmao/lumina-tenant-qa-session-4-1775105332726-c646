---
name: cross-browser-testing
description: "Run WCAG 2.2 accessibility audits and cross-browser compatibility checks"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /cross-browser-testing
metadata:
  openclaw:
    emoji: "♿"
    requires:
      bins: []
      env: []
---

# Accessibility & Cross-Browser Testing

Conduct WCAG 2.2 accessibility audits with automated testing, manual verification, and remediation guidance. Test cross-browser compatibility and ensure consistent behavior. Use when auditing websites for accessibility, fixing WCAG violations, or validating cross-browser rendering.

## When to Use

- Conducting accessibility audits (WCAG 2.2 AA)
- Fixing accessibility violations found by automated tools
- Meeting ADA/Section 508 requirements
- Testing cross-browser compatibility
- Implementing accessible component patterns

## WCAG 2.2 Conformance Levels

| Level | Description | Required For |
|---|---|---|
| A | Minimum accessibility | Legal baseline |
| AA | Standard conformance | Most regulations (target this) |
| AAA | Enhanced accessibility | Specialized needs |

## POUR Principles

**Perceivable:** All images have alt text (decorative: `alt=""`). Video has captions. Color not sole means of conveying info. Text contrast 4.5:1 (large text 3:1). Content reflows at 400% zoom.

**Operable:** All functionality keyboard accessible. No keyboard traps. Tab order logical. Focus indicator visible (3px solid outline). Skip to main content link. No content flashes >3 times/second.

**Understandable:** `<html lang="en">` set. Consistent navigation across pages. Error messages linked to fields with `aria-describedby`. Required fields indicated. Error suggestions specific.

**Robust:** Valid HTML (no duplicate IDs). Custom widgets have ARIA roles, states, properties. Status messages use `role="status"` with `aria-live="polite"`.

## Automated Testing

```bash
npx @axe-core/cli https://example.com
npx pa11y https://example.com
lighthouse https://example.com --only-categories=accessibility
```

Playwright integration: inject `axe-core`, run `axe.run(document)` with WCAG 2.2 AA tags, assert zero violations.

## Common Fixes

**Missing form labels:** Add `<label for="id">` or `aria-label` or `aria-labelledby`.
**Insufficient contrast:** Increase color contrast to 4.5:1 minimum.
**Keyboard navigation:** Add `tabindex="0"`, `role="button"`, handle Enter/Space/Escape/Arrow keys.
**Focus management:** Return focus to trigger element when modal closes. Trap focus inside open modals.

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Best Practices

**Do:** Start accessibility from design phase, test with real users, use semantic HTML first (reduces ARIA needs), automate 30-50% of testing, document accessible patterns.
**Do Not:** Rely only on automated testing, use ARIA as first solution, hide focus outlines, disable zoom, use color as the only indicator.
