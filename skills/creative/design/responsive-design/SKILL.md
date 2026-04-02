---
name: responsive-design
description: "Implement responsive layouts with container queries, fluid typography, and CSS Grid"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /responsive-design
metadata:
  openclaw:
    emoji: "📱"
    requires:
      bins: []
      env: []
---

# Responsive Design

Implement modern responsive design with container queries, fluid typography, CSS Grid, Flexbox, and mobile-first breakpoint strategies. Use when building adaptive interfaces, implementing fluid layouts, or creating component-level responsive behavior.

## When to Use

- Implementing mobile-first responsive layouts
- Using container queries for component-based responsiveness
- Creating fluid typography and spacing scales
- Building complex layouts with CSS Grid and Flexbox
- Designing breakpoint strategies for design systems

## Core Techniques

### Container Queries
Component-level responsiveness independent of viewport. Use `container-type: inline-size` on parent, then `@container (min-width: 400px)` for component breakpoints. Container query units (`cqi`, `cqw`) scale relative to container width.

### Fluid Typography
CSS `clamp()` for smooth scaling between breakpoints:
```css
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--text-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
```

### CSS Grid Responsive Layout
`repeat(auto-fit, minmax(min(300px, 100%), 1fr))` for intrinsic responsive grids. Named grid areas with media query overrides for page layouts. Subgrid for nested grid alignment.

### Mobile-First Breakpoints
Base mobile styles, enhance with `min-width` media queries:
- sm: 640px (landscape phones)
- md: 768px (tablets)
- lg: 1024px (laptops)
- xl: 1280px (desktops)

### Dynamic Viewport Units
Use `100dvh` (dynamic viewport height) instead of `100vh` — accounts for mobile browser UI changes. `100svh` for small viewport, `100lvh` for large viewport.

## Key Patterns

1. **Responsive navigation:** Mobile hamburger menu, desktop horizontal nav with `lg:hidden`/`lg:flex` toggles
2. **Responsive images:** `<picture>` with art direction, `srcSet` for resolution switching, `loading="lazy"` for below-fold
3. **Responsive tables:** Horizontal scroll wrapper on mobile, card-based layout alternative for narrow screens
4. **Responsive containers:** Max-width container with responsive padding (`px-4 sm:px-6 lg:px-8`)

## Best Practices

1. Mobile-first: start with mobile styles, enhance for larger screens
2. Content breakpoints over device breakpoints
3. Fluid values over fixed values for typography and spacing
4. Container queries for component-level responsiveness
5. Test on real devices — simulators miss real-world issues
6. Touch targets: maintain 48x48px minimum on mobile
7. Use logical properties (`inline`/`block`) for internationalization
