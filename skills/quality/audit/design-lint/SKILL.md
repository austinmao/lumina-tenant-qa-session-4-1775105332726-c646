---
name: design-lint
description: "Lint a component or page for design token compliance — colors, spacing, typography"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /design-lint
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Design Lint Skill

Check a component or page for compliance with the project's design system tokens. Validates that colors, spacing, typography, border radii, and shadows use defined tokens rather than arbitrary values. Produces a compliance report and routes all violations to Canvas (visual designer).

## Usage

```
/design-lint <path-to-component-or-page>
```

Example:

```
/design-lint web/src/app/retreats/page.tsx
/design-lint web/src/components/Hero.tsx
```

---

## Prerequisites

Before linting, locate the design token source. Check in order:

1. `brands/your-brand/tokens/design-system.yaml` — primary token file
2. `tailwind.config.ts` or `tailwind.config.js` — Tailwind theme tokens
3. CSS custom properties in global stylesheet (e.g., `web/src/app/globals.css`)

If no design tokens are defined anywhere, report "No design tokens found — cannot perform design lint. Define tokens before running this audit." and produce a partial report listing all hardcoded values found.

---

## Color Compliance (30% weight)

Extract all color values from the target file. For each color:

- **Check against token palette** — the value must match a defined design token color
- **Flag hardcoded hex/rgb/hsl values** — any color not from the token palette is a violation
- **Tailwind class check** — if using Tailwind, verify color classes use custom theme colors (e.g., `text-brand-primary`) not default palette colors (e.g., `text-blue-500`)
- **Opacity variants** — color with opacity must use the token-defined opacity scale, not arbitrary values
- **Semantic naming** — flag colors used for purposes that don't match their semantic name (e.g., `error` color used for non-error UI)

Report format per violation:
```
- Line <n>: <value> — expected token: <suggested-token> | severity: <warning|error>
```

Score this section 0-100. Deduct points per hardcoded value.

---

## Spacing Compliance (25% weight)

Extract all spacing values (margin, padding, gap, width, height when used for spacing):

- **Check against spacing scale** — values must come from the defined spacing scale (e.g., 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- **Flag arbitrary spacing** — values like `13px`, `7px`, `23rem` that don't align with the scale
- **Tailwind class check** — verify spacing classes use theme values; flag arbitrary values like `p-[13px]`
- **Negative spacing** — acceptable if the token scale supports it; flag negative values outside the scale
- **Consistent units** — flag mixed unit usage within the same file (e.g., some values in `px`, others in `rem`)

Score this section 0-100.

---

## Typography Compliance (25% weight)

Extract all typography-related values:

- **Font family** — must match defined font stack tokens; flag any font not in the design system
- **Font size** — must match the type scale; flag arbitrary sizes (e.g., `font-size: 13px` when scale uses 12/14/16/18/20/24)
- **Font weight** — must use defined weight tokens; flag numeric weights not in the system (e.g., `350`)
- **Line height** — must match defined line height ratios; flag arbitrary values
- **Letter spacing** — must match defined tracking values; flag arbitrary values
- **Tailwind class check** — verify text size classes use theme tokens; flag `text-[13px]`

Score this section 0-100.

---

## Border & Shadow Compliance (10% weight)

- **Border radius** — must match defined radius tokens; flag arbitrary radii
- **Border width** — must match defined width tokens
- **Box shadow** — must match defined shadow tokens; flag custom shadow values not in the system
- **Border color** — must match defined color tokens (overlaps with Color Compliance but checked here for border-specific context)

Score this section 0-100.

---

## Consistency Patterns (10% weight)

- **Component spacing consistency** — similar components should use the same spacing patterns; flag divergent spacing between siblings
- **Responsive scaling** — spacing and typography should scale proportionally across breakpoints; flag components that use desktop spacing at mobile
- **Dark mode tokens** — if dark mode is supported, verify all colors reference tokens with dark mode variants; flag hardcoded colors that won't adapt

Score this section 0-100.

---

## Scoring

Calculate the overall design lint score as a weighted sum:

| Section | Weight |
|---|---|
| Color Compliance | 30% |
| Spacing Compliance | 25% |
| Typography Compliance | 25% |
| Border & Shadow Compliance | 10% |
| Consistency Patterns | 10% |

```
overall = (color * 0.30) + (spacing * 0.25) + (typography * 0.25) + (border * 0.10) + (consistency * 0.10)
```

**Score bands:**

| Score | Rating |
|---|---|
| 90-100 | Compliant — all values use tokens |
| 75-89 | Mostly Compliant — minor violations |
| 50-74 | Non-Compliant — significant hardcoded values |
| 0-49 | Critical — design system not followed |

---

## Output Format

```
Design Lint Report: <path>
Date: <YYYY-MM-DD>
Token Source: <path-to-design-tokens>
Overall Score: <score>/100 (<rating>)

[Color Compliance] <score>/100
  Violations: <count>
  - Line <n>: <value> — expected: <token> | severity: <level>
  ...

[Spacing Compliance] <score>/100
  Violations: <count>
  - Line <n>: <value> — expected: <token> | severity: <level>
  ...

[Typography Compliance] <score>/100
  Violations: <count>
  - Line <n>: <value> — expected: <token> | severity: <level>
  ...

[Border & Shadow Compliance] <score>/100
  Violations: <count>
  ...

[Consistency Patterns] <score>/100
  ...

Total Violations: <count>
Auto-fixable: <count> (values with clear token mappings)

Recommended Fix Order:
  1. <highest impact>
  2. ...
```

Save the report to `memory/reports/design-lint-report.md`.

---

## Issue Routing

All design token violations are routed to **Canvas** (visual designer, `agents/website/visual-designer`).

- Token additions (new values not in the system): Canvas decides whether to add or replace
- Violations with clear token mappings: may be auto-fixed by Nova after Canvas approval
- Do not fix violations directly — produce the report and hand off
