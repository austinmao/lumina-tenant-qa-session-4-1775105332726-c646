---
name: brand-kit-generation
description: "Generate a brand kit from 1-2 colors / create brand palette, type scale, spacing, and CSS variables"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /brand-kit
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      os: ["darwin"]
---

# Brand Kit Generation Skill

Generates a complete brand kit from as few as 1-2 input colors: full color palette (primary, secondary, accent, neutral, semantic), type scale, spacing system, CSS custom properties, and a visual reference card. Ported from Naksha-studio's /brand-kit command.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Check if `<brand_root>/tokens/design-system.yaml` already exists — if so, warn the user before overwriting.

---

## Steps

### 1. Accept color inputs

Minimum input: one primary color (hex, HSL, or OKLCH).

| Input | Required | Derivation if absent |
|---|---|---|
| Primary color | Yes | N/A |
| Secondary color | No | 180-degree hue rotation in OKLCH from primary |
| Accent color | No | 30-degree analogous shift from primary |
| Neutral base | No | Desaturated primary (chroma < 0.02) |
| Background | No | Neutral-50 (near-white with warm/cool tint from primary) |

### 2. Generate color palette

For each color role, produce an 11-step scale (50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950) using OKLCH interpolation:

**Algorithm**:
1. Convert input hex to OKLCH (Lightness, Chroma, Hue).
2. Set the input as the 500 (base) step.
3. For lighter steps (50-400): increase L linearly, decrease C slightly.
4. For darker steps (600-950): decrease L linearly, decrease C slightly.
5. Preserve Hue constant across the entire scale.

**Semantic colors** (derived automatically):
- `success`: green hue (H ~145), medium chroma
- `warning`: amber hue (H ~85), medium chroma
- `error`: red hue (H ~25), medium chroma
- `info`: blue hue (H ~250), medium chroma

Each semantic color gets 3 stops: light (background), base (text/icon), dark (hover).

### 3. Generate type scale

Use a configurable modular ratio (default: 1.25 Major Third):

| Token | Calc | Default size | Usage |
|---|---|---|---|
| `--font-xs` | base / ratio^2 | 10.24px | Labels, fine print |
| `--font-sm` | base / ratio | 12.8px | Captions, metadata |
| `--font-base` | base | 16px | Body copy |
| `--font-md` | base * ratio | 20px | Lead text |
| `--font-lg` | base * ratio^2 | 25px | Section headings (h3) |
| `--font-xl` | base * ratio^3 | 31.25px | Page headings (h2) |
| `--font-2xl` | base * ratio^4 | 39.06px | Hero headings (h1) |
| `--font-3xl` | base * ratio^5 | 48.83px | Display text |

Include line-height and letter-spacing mappings:
- Body sizes (xs-md): line-height 1.5-1.7, letter-spacing normal
- Heading sizes (lg-3xl): line-height 1.1-1.3, letter-spacing -0.02em to -0.04em

### 4. Generate spacing system

4px base unit, geometric progression:

```
0, 1(4px), 2(8px), 3(12px), 4(16px), 5(20px), 6(24px),
8(32px), 10(40px), 12(48px), 16(64px), 20(80px), 24(96px), 32(128px)
```

### 5. Generate additional scales

**Border radius**: `none(0), sm(2px), md(4px), lg(8px), xl(12px), 2xl(16px), full(9999px)`

**Shadows** (using primary hue for tinted shadows):
```
--shadow-xs: 0 1px 2px oklch(0% 0 <hue> / 0.04);
--shadow-sm: 0 1px 3px oklch(0% 0 <hue> / 0.06);
--shadow-md: 0 4px 6px oklch(0% 0 <hue> / 0.08);
--shadow-lg: 0 10px 15px oklch(0% 0 <hue> / 0.1);
--shadow-xl: 0 20px 25px oklch(0% 0 <hue> / 0.12);
```

**Transitions**:
```
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
```

### 6. Output files

Write all assets to `<brand_root>/tokens/`:

```
<brand_root>/tokens/
  design-system.yaml         # Machine-readable token dictionary
  brand-kit.css              # CSS custom properties (light + dark mode)
  brand-kit.scss             # SCSS variables
  brand-kit.json             # JSON token export
  palette-reference.md       # Visual reference card (markdown table with hex values)
```

---

## Output

Summary report to `memory/reports/brand-kit-generation.md`:

```markdown
## Brand Kit Generation Report
Site: <site_id> | Date: YYYY-MM-DD

### Input
- Primary: <hex> (OKLCH: L C H)
- Secondary: <hex> (<derived|user-provided>)
- Accent: <hex> (<derived|user-provided>)

### Palette
| Role | 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 |
[table with hex values]

### Type Scale
| Token | Size | Line-height |
[table]

### Files Generated
- [list]

### Accessibility Notes
- Primary on white: contrast ratio X:1 (AA pass/fail)
- Primary on dark: contrast ratio X:1 (AA pass/fail)
```

---

## Guidelines

- Always check WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text) between text colors and backgrounds. Flag failures in the report.
- OKLCH is mandatory for perceptual uniformity. Do not use HSL — it produces uneven perceptual lightness steps.
- Never generate more than 5 hue families. Complexity defeats brand recognition.
- The neutral scale must have a tint from the primary hue (chroma 0.005-0.015), not pure gray.
- Dark mode is generated automatically by inverting the semantic scale mappings — never skip it.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If the provided color is invalid (not a valid hex/HSL/OKLCH): ask user to correct the input.
- If the brand_root directory does not exist: create it.
- If tokens directory already has files: ask user whether to overwrite or generate to a new directory.
