---
name: quality-standards
description: "Define and enforce quality gates for all creative and engineering output"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Define the quality bar for deliverables. Specify what must pass before anything ships.

## Quality Gates
1. Brand compliance (brand guide adherence)
2. Copy quality (grammar, tone, clarity)
3. Visual consistency (design tokens, spacing, typography)
4. Technical correctness (builds, renders, validates)
5. Accessibility (WCAG AA minimum)
6. Cross-client compatibility (email: Gmail+Outlook+Apple Mail; web: Chrome+Safari+Firefox)
7. Performance (Core Web Vitals: LCP<2.5s, FID<100ms, CLS<0.1)
