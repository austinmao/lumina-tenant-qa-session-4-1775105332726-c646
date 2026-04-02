---
name: tailwind-design-system
description: "Build design systems with Tailwind CSS v4, design tokens, and component libraries"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /tailwind-design-system
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: []
      env: []
---

# Tailwind Design System (v4)

Build production-ready design systems with Tailwind CSS v4 including CSS-first configuration with `@theme`, design tokens, CVA component variants, responsive patterns, dark mode, and accessibility. Use when creating component libraries, implementing theming, or standardizing UI patterns.

## When to Use

- Creating a component library with Tailwind v4
- Implementing design tokens and theming with CSS-first configuration
- Building responsive and accessible components
- Migrating from Tailwind v3 to v4

## Key v4 Changes

| v3 Pattern | v4 Pattern |
|---|---|
| `tailwind.config.ts` | `@theme` in CSS |
| `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| `darkMode: "class"` | `@custom-variant dark (&:where(.dark, .dark *))` |
| `theme.extend.colors` | `@theme { --color-*: value }` |
| `require("tailwindcss-animate")` | CSS `@keyframes` in `@theme` + `@starting-style` |

## Core Patterns

### 1. CSS-First Configuration with `@theme`
Define all design tokens (colors, radii, animations) inside `@theme` blocks in CSS. Use OKLCH color space for better perceptual uniformity. Dark mode overrides via `.dark` class with `@custom-variant`.

### 2. CVA (Class Variance Authority) Components
Type-safe component variants with `cva()`. Define base styles, variant options (default, destructive, outline, ghost, link), and sizes. Use with `cn()` utility (`clsx` + `tailwind-merge`).

### 3. Compound Components (React 19)
React 19 passes `ref` as a regular prop — no `forwardRef` needed. Build Card, CardHeader, CardTitle, CardContent, CardFooter as separate composable components.

### 4. Responsive Grid System
Container and Grid components with CVA variants. Use `repeat(auto-fit, minmax(...))` for intrinsic responsive grids.

### 5. Dark Mode with CSS
`@custom-variant dark` for class-based dark mode. ThemeProvider with localStorage persistence. System preference detection via `prefers-color-scheme`.

### 6. Native CSS Animations
`@keyframes` inside `@theme` for animations. `@starting-style` for entry animations on native popover/dialog elements.

## Advanced v4 Patterns

- **Custom utilities:** `@utility` directive for reusable patterns
- **Theme modifiers:** `@theme inline` for referencing CSS variables, `@theme static` for always-output variables
- **Namespace clearing:** `--color-*: initial` to clear defaults
- **Container queries:** Define breakpoints in `@theme`
- **Semi-transparent variants:** `color-mix(in oklab, ...)` for alpha variants

## v3 to v4 Migration Checklist

- Replace `tailwind.config.ts` with CSS `@theme` block
- Change `@tailwind` directives to `@import "tailwindcss"`
- Move colors to `@theme { --color-*: value }`
- Replace `darkMode: "class"` with `@custom-variant dark`
- Move `@keyframes` inside `@theme`
- Replace `forwardRef` (React 19 passes ref as prop)
- Consider OKLCH colors for better perception
- Replace custom plugins with `@utility` directives
