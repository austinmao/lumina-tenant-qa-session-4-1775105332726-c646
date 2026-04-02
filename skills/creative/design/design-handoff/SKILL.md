---
name: design-handoff
description: "Create developer handoff documentation / generate specs, measurements, and asset lists for a design"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /design-handoff
metadata:
  openclaw:
    emoji: "📋"
    requires:
      os: ["darwin"]
---

# Design Handoff Skill

Generates comprehensive developer handoff documentation from a design: exact measurements, token references, component specs, interaction notes, asset inventory, and implementation checklist. Bridges the gap between design intent and code implementation. Ported from Naksha-studio's /design-handoff command.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` for token references.

---

## Steps

### 1. Identify the handoff scope

Accept from the user:
- **Scope**: full page, section, or individual component
- **Design source**: file path, component name, or description
- **Target framework**: Next.js + Tailwind (default), React + CSS Modules, or vanilla HTML/CSS

### 2. Generate measurement spec

For each visual element, document:

| Property | Value | Token reference |
|---|---|---|
| Width | 600px / 100% / fit-content | `--container-max` |
| Height | auto / 48px / aspect-[16/9] | `--space-12` |
| Padding | 16px 24px | `--space-4 --space-6` |
| Margin | 0 0 24px | `--space-0 --space-6` |
| Gap | 16px | `--space-4` |
| Font size | 20px | `--text-lg` |
| Font weight | 700 | bold |
| Line height | 1.3 | heading default |
| Letter spacing | -0.02em | heading default |
| Color | #1a1a1a | `--color-text-primary` |
| Background | #ffffff | `--color-surface` |
| Border | 1px solid #e8e0d4 | `--color-border` |
| Border radius | 8px | `--radius-lg` |
| Shadow | 0 4px 6px rgba(0,0,0,0.07) | `--shadow-md` |

### 3. Generate component spec

For each unique component:

```markdown
### Component: <name>

**Layout**: Flex row / Grid 3-col / Block
**Variants**: default, hover, active, disabled, loading
**Size variants**: sm (32px height), md (40px), lg (48px)

#### Props
| Prop | Type | Default | Required |
|---|---|---|---|
| label | string | — | Yes |
| variant | 'primary' \| 'secondary' | 'primary' | No |
| disabled | boolean | false | No |
| onClick | () => void | — | No |

#### States
| State | Changes from default |
|---|---|
| Hover | Background darkens 10%, cursor: pointer |
| Focus | Ring: 2px offset, primary-500 |
| Active | Scale: 0.98, background darkens 15% |
| Disabled | Opacity: 0.5, cursor: not-allowed |
| Loading | Content replaced with spinner, pointer-events: none |

#### Responsive
| Breakpoint | Changes |
|---|---|
| < 768px | Full width, text-sm |
| 768-1024px | Auto width, text-base |
| > 1024px | Fixed width, text-base |
```

### 4. Generate asset inventory

| Asset | Format | Dimensions | Usage |
|---|---|---|---|
| Logo | SVG + PNG@2x | 220x59 | Header |
| Hero image | WebP + JPEG fallback | 1440x600 | Hero background |
| Icon set | SVG sprite | 24x24 | UI icons |
| Favicon | ICO + PNG | 32x32, 180x180 | Browser tab, iOS |

### 5. Generate interaction notes

Document every interaction that is not obvious from static design:
- Hover animations (what property, duration, easing)
- Click/tap feedback
- Scroll-triggered animations (trigger point, direction)
- Form validation behavior (when to validate, error placement)
- Loading state transitions
- Navigation transitions (page-level, section-level)
- Keyboard shortcuts and tab order

### 6. Generate implementation checklist

A developer-facing checklist:

```markdown
- [ ] Set up design tokens (CSS custom properties or Tailwind config)
- [ ] Create base layout (header, main, footer)
- [ ] Implement each section top-to-bottom
- [ ] Add responsive behavior at all 4 breakpoints
- [ ] Implement all interactive states (hover, focus, active, disabled)
- [ ] Add loading states and skeleton screens
- [ ] Implement form validation
- [ ] Add animations (entrance, hover, scroll-triggered)
- [ ] Add reduced-motion fallbacks
- [ ] Verify WCAG AA compliance (contrast, keyboard nav, screen reader)
- [ ] Cross-browser test (Chrome, Firefox, Safari, Edge)
- [ ] Performance audit (LCP < 2.5s, CLS < 0.1)
```

---

## Output

Write handoff documentation to `<site_dir>/handoff/<scope-name>/`:

```
<site_dir>/handoff/<scope-name>/
  measurements.md              # Every element with exact measurements + token refs
  components.md                # Component specs with props, states, responsive
  assets.md                    # Asset inventory with format, size requirements
  interactions.md              # Animation, hover, scroll, form behavior
  implementation-checklist.md  # Developer checklist
  README.md                    # Overview and quick-start
```

Summary report to `memory/reports/design-handoff-<scope>.md`.

---

## Guidelines

- Every measurement must reference a design token. If a measurement does not map to a token, flag it as a potential inconsistency.
- Component specs must include ALL interactive states, not just the default and hover.
- Asset inventory must specify required formats (WebP primary, JPEG/PNG fallback).
- Never assume the developer can see the original design. The handoff must be self-sufficient.
- Tab order must be explicitly documented if it differs from DOM order.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If design tokens are missing: generate measurements in absolute values and flag the gap.
- If the scope is ambiguous: ask the user to clarify which page, section, or component.
