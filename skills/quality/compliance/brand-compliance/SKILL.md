---
name: brand-compliance
description: "Audit logo usage, color compliance, typography checks, and brand guideline enforcement"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /brand-compliance
metadata:
  openclaw:
    emoji: "✅"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Brand Compliance

Audit visual assets, web pages, emails, and marketing materials for compliance with brand guidelines -- logo usage, color palette, typography, spacing, tone of voice, and imagery standards. This is an evaluator skill that checks what others produced and generates structured compliance reports.

## When to Use

- Auditing a built page, email, or marketing asset before deployment
- Checking logo usage across materials (placement, sizing, clear space, color variants)
- Verifying color usage against the approved brand palette
- Checking typography for correct font usage, hierarchy, and sizing
- Reviewing imagery and photography for brand alignment
- Running a brand compliance sweep across all tenant-facing assets
- Validating design tokens are correctly applied in code

## Context Loading

Before any compliance audit:
1. Read `<brand_root>/brand-guide.md` for the complete brand identity system
2. Read `<brand_root>/tokens/design-system.yaml` for design token specifications
3. Read `<brand_root>/assets/logos/` for the logo inventory and usage rules
4. Read the art direction brief for the campaign (if auditing campaign assets)
5. Read existing compliance reports for known issues and historical decisions

## Audit Categories

### 1. Logo Usage

Check every instance of the logo against the brand guidelines:

#### Placement Rules
| Check | Criteria | Severity |
|---|---|---|
| Correct logo variant | Right variant for context (color, black, white) | critical |
| Minimum size | Logo meets minimum display size | major |
| Clear space | Required clear space respected around logo | major |
| Background contrast | Logo is legible on its background | critical |
| No modifications | Logo not stretched, rotated, recolored, or cropped | critical |
| Correct file format | SVG for web, PNG for email, vector for print | minor |

#### Logo Variant Selection
| Context | Correct Variant |
|---|---|
| Light background | Color logo or black logo |
| Dark background | White logo |
| Favicon / small icon | Icon variant (no wordmark) |
| Email header | Horizontal variant (PNG format) |
| Social media avatar | Icon variant, square crop |

#### Common Violations
- Logo used at less than minimum size (appears as a blur)
- Logo placed on a busy photographic background without contrast treatment
- Logo recolored to match a campaign palette (use approved variants only)
- Clear space invaded by text, imagery, or other elements
- Outdated logo version used (check against the canonical file in brand assets)

### 2. Color Compliance

Verify all colors used match the approved brand palette:

#### Color Audit Checklist
| Check | Criteria | Severity |
|---|---|---|
| Primary colors match | Hex values match design tokens exactly | critical |
| Secondary colors match | Hex values within approved palette | major |
| Campaign colors approved | Any non-brand colors documented and approved | major |
| Background/foreground contrast | WCAG AA compliance (4.5:1 text, 3:1 large/UI) | critical |
| Gradient usage | Gradients follow approved direction and stops | minor |
| Dark mode | Colors adapt correctly in dark mode (if supported) | major |

#### Common Violations
- Close-but-wrong hex values (e.g., `#1A1A1A` instead of the brand's `#111111`)
- Unapproved accent colors introduced without documentation
- Brand colors used for unintended purposes (e.g., error red used as a decorative element)
- Contrast failure between text and background

### 3. Typography

Verify all text uses the correct fonts, weights, sizes, and hierarchy:

#### Typography Audit Checklist
| Check | Criteria | Severity |
|---|---|---|
| Font family | Correct font loaded and applied | critical |
| Font weight | Approved weights only (no unauthorized bold/light) | major |
| Heading hierarchy | H1 > H2 > H3 in size and weight, single H1 per page | critical |
| Body text size | Minimum 16px body text on web | major |
| Line height | Matches design token specification | minor |
| Letter spacing | Matches design token specification | minor |
| Font fallback | System fallback font specified in CSS | minor |
| Font loading | No FOIT (Flash of Invisible Text) — use font-display: swap | major |

#### Common Violations
- Using system fonts where the brand font should load
- Heading hierarchy violations (H3 used as the largest text on a page)
- Body text smaller than 16px (readability issue)
- Missing font-weight variants (using browser faux-bold instead of the bold weight)
- Inconsistent letter-spacing on headings across pages

### 4. Imagery and Photography

Verify imagery aligns with the brand's visual direction:

#### Imagery Audit Checklist
| Check | Criteria | Severity |
|---|---|---|
| On-brand style | Matches the art direction / photography brief | major |
| Image quality | High resolution, no pixelation at display size | major |
| Color grading | Consistent with brand color treatment | minor |
| Alt text | Descriptive alt text on every meaningful image | critical |
| Stock photo quality | No generic stock photo cliches | minor |
| Diversity | Representation aligns with brand values | major |
| Decorative images | Properly marked as `aria-hidden` or `role="presentation"` | minor |

### 5. Tone of Voice

Verify written content follows the brand voice guidelines:

#### Voice Audit Checklist
| Check | Criteria | Severity |
|---|---|---|
| Kill list compliance | No words from the brand kill list | critical |
| Voice characteristics | Matches documented voice traits | major |
| Terminology consistency | Uses approved terms (not rejected alternatives) | major |
| CTA alignment | CTAs match approved CTA patterns | minor |
| Headline tone | Headlines match brand headline style | minor |

See the `brand-review-gate` skill for detailed voice compliance checking.

### 6. Design Token Compliance

For web pages and applications, verify design tokens are correctly applied:

#### Token Audit Checklist
| Check | Criteria | Severity |
|---|---|---|
| Spacing scale | Spacing values match the design system scale | minor |
| Border radius | Radius values match design tokens | minor |
| Shadow values | Box shadows match design tokens | minor |
| Breakpoints | Responsive breakpoints match the design system | major |
| Component patterns | UI components follow established patterns | major |
| CSS custom properties | Design tokens referenced via variables, not hardcoded | minor |

## Compliance Report Format

```markdown
## Brand Compliance Audit — [Asset/Page Name]

**Date**: [date]
**Auditor**: [name or agent]
**Brand guide version**: [version or date]

### Summary
**Verdict**: compliant | conditional-pass | non-compliant
**Issues**: [total] ([critical] critical, [major] major, [minor] minor)

### Logo Usage
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Correct variant | pass | Color logo on light background | - |
| Minimum size | fail | Logo at 40px, minimum is 60px | Increase to 60px minimum |
| Clear space | pass | 20px clearance maintained | - |

### Color Compliance
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Primary colors | pass | Hex values match tokens | - |
| Contrast ratio | fail | CTA button text: 3.2:1 (requires 4.5:1) | Darken button background |

### Typography
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Font family | pass | Brand font loaded correctly | - |
| Heading hierarchy | fail | Two H1 elements on page | Change second H1 to H2 |

### Imagery
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Alt text | fail | Hero image missing alt text | Add descriptive alt text |

### Tone of Voice
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Kill list | fail | "Transform your life" used (kill list) | Rewrite per brand guide |

### Design Tokens
| Check | Status | Finding | Remediation |
|---|---|---|---|
| Spacing | pass | All spacing on design scale | - |
```

## Sweep Audit

For auditing all pages of a site:

1. Compile the page inventory from the sitemap
2. Audit each page against all categories
3. Aggregate findings into a summary report
4. Prioritize by severity: fix all critical issues first, then major, then minor

### Sweep Summary Format

```markdown
## Brand Compliance Sweep — [Site Name]

**Pages audited**: [n]
**Overall verdict**: [compliant / needs-remediation / non-compliant]

### Issue Distribution
| Category | Critical | Major | Minor | Total |
|---|---|---|---|---|
| Logo | [n] | [n] | [n] | [n] |
| Color | [n] | [n] | [n] | [n] |
| Typography | [n] | [n] | [n] | [n] |
| Imagery | [n] | [n] | [n] | [n] |
| Voice | [n] | [n] | [n] | [n] |
| Tokens | [n] | [n] | [n] | [n] |

### Most Common Issues
1. [Issue type] — [count] occurrences across [n] pages
2. [Issue type] — [count] occurrences across [n] pages

### Pages Requiring Remediation
| Page | Critical | Major | Verdict |
|---|---|---|---|
| [page URL] | [n] | [n] | non-compliant |
| [page URL] | [n] | [n] | conditional-pass |
```

## Issue Severity

| Severity | Criteria |
|---|---|
| `critical` | Logo misuse, accessibility violation (contrast, alt text), kill list violation, heading hierarchy broken |
| `major` | Wrong color hex, unauthorized font weight, stock photo cliche, missing font loading strategy, broken responsive layout |
| `minor` | Spacing off-scale, border radius mismatch, gradient direction wrong, letter-spacing inconsistency |

## Routing Remediation

Route issues to the responsible owner:
- Logo, color, imagery, and token issues -> Creative Director
- Typography and font loading issues -> Frontend Engineer
- Tone of voice and kill list violations -> Copywriter
- Accessibility issues (contrast, alt text) -> Frontend Engineer + QA Engineer

## Boundaries

- Never modify designs, code, or content. Produce compliance reports only.
- Never approve assets with critical brand violations.
- Never override the brand guide without Creative Director approval.
- Never skip a category -- all six categories are checked on every audit.

## Dependencies

- `brand-standards` -- brand guidelines that define compliance criteria
- `brand-review-gate` -- voice compliance checking (complementary skill)
- `brand-identity-design` -- design token specifications
- `website-testing` -- broader QA that includes brand compliance as one category

## State Tracking

- `auditReports` -- keyed by asset/page name: audit date, verdict, issue counts by severity
- `openIssues` -- active compliance issues: asset, category, severity, owner, status
- `sweepResults` -- keyed by sweep date: pages audited, overall verdict, issue distribution
