---
name: design-system-architecture
description: "Generate design tokens and component library / create a Tailwind config from brand tokens"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /design-system-architecture
metadata:
  openclaw:
    emoji: "🏗️"
    requires:
      os: ["darwin"]
---

# Design System Architecture Skill

Generates a complete design system from brand tokens: design token files (CSS custom properties, Tailwind config, SCSS variables), component library structure, and spacing/typography/color scales. Ported from Naksha-studio's design-tokens and design-system commands.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` if it exists — use as input tokens.
4. If no design-system.yaml exists, check for `<brand_root>/brand-guide.md` to extract colors, fonts, and spacing.

---

## Steps

### 1. Gather brand inputs

Accept from user or extract from brand files:

| Input | Required | Default | Example |
|---|---|---|---|
| Primary color | Yes | None | `#8b7355` |
| Secondary color | No | Computed complement | `#1a1a1a` |
| Accent color | No | Computed from primary | `#c9a96e` |
| Font family (heading) | No | `Georgia, serif` | `Inter, sans-serif` |
| Font family (body) | No | `Georgia, serif` | `Lora, serif` |
| Base font size | No | `16px` | `18px` |
| Base spacing unit | No | `4px` | `8px` |
| Border radius scale | No | `4px` | `8px` |
| Brand name | Yes | From site context | `the organization` |

### 2. Generate color scale

From each input color, generate a 10-step scale (50-950) using the OKLCH color space for perceptual uniformity:

```
--color-primary-50:  oklch(97% 0.02 <hue>);
--color-primary-100: oklch(94% 0.04 <hue>);
--color-primary-200: oklch(88% 0.06 <hue>);
--color-primary-300: oklch(78% 0.08 <hue>);
--color-primary-400: oklch(68% 0.10 <hue>);
--color-primary-500: oklch(58% 0.12 <hue>);   /* base */
--color-primary-600: oklch(48% 0.10 <hue>);
--color-primary-700: oklch(38% 0.08 <hue>);
--color-primary-800: oklch(28% 0.06 <hue>);
--color-primary-900: oklch(18% 0.04 <hue>);
--color-primary-950: oklch(12% 0.02 <hue>);
```

Generate semantic aliases:
- `--color-text-primary`: 900 (light) or 50 (dark)
- `--color-text-secondary`: 700 (light) or 200 (dark)
- `--color-text-muted`: 500
- `--color-surface`: 50 (light) or 900 (dark)
- `--color-surface-elevated`: white (light) or 800 (dark)
- `--color-border`: 200 (light) or 700 (dark)
- `--color-accent`: primary-500

### 3. Generate typography scale

Use a modular scale ratio (default 1.25 — Major Third):

| Token | Size | Line-height | Weight | Usage |
|---|---|---|---|---|
| `--text-xs` | 12px | 1.5 | 400 | Fine print, labels |
| `--text-sm` | 14px | 1.5 | 400 | Secondary text, captions |
| `--text-base` | 16px | 1.6 | 400 | Body copy |
| `--text-lg` | 20px | 1.5 | 500 | Lead paragraphs |
| `--text-xl` | 25px | 1.3 | 600 | Section headings (h3) |
| `--text-2xl` | 31px | 1.2 | 700 | Page headings (h2) |
| `--text-3xl` | 39px | 1.1 | 700 | Hero headings (h1) |
| `--text-4xl` | 49px | 1.1 | 800 | Display headings |

### 4. Generate spacing scale

From the base spacing unit (default 4px), generate a power-of-2 scale:

```
--space-0: 0px;
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
```

### 5. Generate border radius and shadow scales

```
--radius-none: 0;
--radius-sm: 2px;
--radius-md: 4px;
--radius-lg: 8px;
--radius-xl: 12px;
--radius-2xl: 16px;
--radius-full: 9999px;

--shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);
--shadow-md: 0 4px 6px oklch(0% 0 0 / 0.07);
--shadow-lg: 0 10px 15px oklch(0% 0 0 / 0.1);
--shadow-xl: 0 20px 25px oklch(0% 0 0 / 0.1);
```

### 6. Generate Tailwind v4 config

Produce a `tailwind.config.ts` that maps all tokens:

```typescript
import type { Config } from "tailwindcss";

export default {
  theme: {
    colors: {
      primary: { /* 50-950 from step 2 */ },
      secondary: { /* ... */ },
      accent: { /* ... */ },
      neutral: { /* ... */ },
    },
    fontFamily: {
      heading: ["<heading-font>", "serif"],
      body: ["<body-font>", "serif"],
      ui: ["<ui-font>", "sans-serif"],
    },
    fontSize: { /* from step 3 */ },
    spacing: { /* from step 4 */ },
    borderRadius: { /* from step 5 */ },
    boxShadow: { /* from step 5 */ },
  },
} satisfies Config;
```

### 7. Generate CSS custom properties file

Write a `design-tokens.css` file with all tokens as CSS custom properties, organized by category (colors, typography, spacing, borders, shadows), including a `@media (prefers-color-scheme: dark)` block with inverted semantic aliases.

### 8. Generate component token mapping

For each standard component type, produce a token mapping table:

| Component | Background | Text | Border | Radius | Padding | Shadow |
|---|---|---|---|---|---|---|
| Button (primary) | primary-600 | white | none | md | space-3 space-6 | sm |
| Button (secondary) | transparent | primary-600 | primary-300 | md | space-3 space-6 | none |
| Card | surface-elevated | text-primary | border | lg | space-6 | md |
| Input | surface | text-primary | border | md | space-3 space-4 | none |
| Badge | primary-100 | primary-700 | none | full | space-1 space-3 | none |
| Alert | accent-50 | accent-900 | accent-200 | md | space-4 | none |

---

## Output

Write all generated files to `<site_dir>/design-system/`:

```
<site_dir>/design-system/
  tokens/
    design-tokens.css          # CSS custom properties
    design-tokens.scss         # SCSS variables
    design-tokens.json         # JSON token dictionary
  tailwind.config.ts           # Tailwind v4 config
  component-tokens.md          # Component token mapping table
  README.md                    # Usage guide
```

Also write a summary report to `memory/reports/design-system-architecture.md`:

```markdown
## Design System Architecture Report
Site: <site_id> | Date: YYYY-MM-DD

### Token Summary
- Colors: N scales (primary, secondary, accent, neutral) x 11 steps = NN tokens
- Typography: N sizes
- Spacing: N steps
- Borders: N radius values
- Shadows: N elevation levels

### Component Mappings
- N components mapped to token references

### Files Generated
- [list of files with paths]
```

---

## Guidelines

- Always generate both light and dark mode tokens. Dark mode is not optional.
- Never hardcode pixel values in component code — always reference token variables.
- Keep the color palette under 5 hues total (primary, secondary, accent, neutral, error/success/warning). More than 5 indicates the brand lacks focus.
- Typography scale must have no more than 8 sizes. If the user requests more, advise consolidation.
- Tailwind config must use the `satisfies Config` pattern for type safety.
- OKLCH color space is mandatory for perceptual uniformity. Do not fall back to HSL unless explicitly requested.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If no brand colors are available from any source: ask user to provide at least one primary color.
- If Tailwind is not in the project's dependencies: still generate the config (it serves as documentation) but note in the report that `tailwindcss` is not installed.
- If the design-system directory already exists: ask user whether to overwrite or merge.
