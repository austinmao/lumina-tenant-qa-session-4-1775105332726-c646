---
name: design-templates
description: "Generate a page template / scaffold a landing page, dashboard, pricing, auth, blog, ecommerce, portfolio, docs, SaaS, or onboarding layout"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /design-templates
metadata:
  openclaw:
    emoji: "📐"
    requires:
      os: ["darwin"]
---

# Design Templates Skill

Generates production-ready page templates across 10 categories. Each template comes with semantic HTML structure, design token assignments, responsive breakpoints, component inventory, and content slots. Ported from Naksha-studio's template-gallery reference.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` for design tokens. If absent, use sensible defaults and note in output.
4. Read `<brand_root>/brand-guide.md` if available for brand-specific layout preferences.

---

## Steps

### 1. Select template category

The user specifies one of 10 categories:

| # | Category | Typical use |
|---|---|---|
| 1 | **Landing** | Marketing page, hero + social proof + CTA |
| 2 | **Dashboard** | Admin panel, sidebar nav + data grid + charts |
| 3 | **Pricing** | Plan comparison, feature matrix, toggle annual/monthly |
| 4 | **Auth** | Login, signup, forgot password, 2FA |
| 5 | **Blog** | Article list, article detail, author page |
| 6 | **Ecommerce** | Product grid, product detail, cart, checkout |
| 7 | **Portfolio** | Project grid, project detail, about page |
| 8 | **Docs** | Sidebar nav + search + content area + table of contents |
| 9 | **SaaS** | Feature showcase, integrations, testimonials, changelog |
| 10 | **Onboarding** | Multi-step wizard, progress indicator, completion |

### 2. Define the template structure

For the selected category, produce:

#### Section inventory

List all sections in order with:
- Section name and purpose
- Layout pattern (full-width, contained, split, grid)
- Content slots (heading, body, media, CTA, form)
- Background treatment (surface, elevated, accent, dark)

#### Component inventory

List every unique component needed:
- Component name
- Token assignments (colors, typography, spacing, radius, shadow)
- Interactive states (default, hover, focus, active, disabled)
- Size variants (sm, md, lg)

#### Responsive behavior

Specify layout at 4 breakpoints:

| Breakpoint | Width | Layout changes |
|---|---|---|
| Mobile | 320-767px | Single column, stacked sections, hamburger nav |
| Tablet | 768-1023px | 2-column grid where applicable, condensed nav |
| Desktop | 1024-1439px | Full layout, sidebar visible |
| Wide | 1440px+ | Max-width container, centered |

### 3. Generate template code

Produce Next.js App Router JSX with:
- Tailwind utility classes mapped to design tokens
- Semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<article>`, `<footer>`)
- Accessibility attributes (ARIA landmarks, roles, labels)
- Content slots as props with sensible defaults
- Responsive modifiers (`sm:`, `md:`, `lg:`, `xl:`)

### 4. Generate content slot guide

For each content slot, specify:
- Character limit (heading: 60, subheading: 120, body paragraph: 300)
- Tone guidance ("action-oriented for CTA, empathetic for testimonials")
- Image specs (aspect ratio, minimum resolution, alt text requirements)

---

## Output

Write template files to `<site_dir>/templates/<category>/`:

```
<site_dir>/templates/<category>/
  page.tsx                    # Next.js page component
  components/                 # Page-specific components
  template-spec.md            # Section inventory, component list, responsive spec
  content-slots.md            # Content requirements per slot
```

Summary report to `memory/reports/design-template-<category>.md`:

```markdown
## Design Template — <category>
Site: <site_id> | Date: YYYY-MM-DD

### Sections
| # | Section | Layout | Background |
[table]

### Components
| Component | Variants | States |
[table]

### Responsive Summary
[breakpoint behavior]

### Files Generated
[list]
```

---

## Guidelines

- Every template must pass WCAG AA without modification. Build accessibility in, do not bolt it on.
- Use CSS Grid for page layout and Flexbox for component layout. Do not use floats or absolute positioning for layout.
- All templates must work without JavaScript for above-the-fold content (progressive enhancement).
- Never use placeholder images in templates. Use content slots with explicit dimension requirements instead.
- Landing pages: hero section must be visible without scrolling at 768px height. No auto-playing video.
- Dashboard templates: sidebar must be collapsible on mobile. Data tables must be scrollable horizontally.
- Auth templates: password inputs must support show/hide toggle. Forms must support autofill.
- Pricing templates: the recommended plan must be visually distinct (elevated card, different border/shadow).

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If the category is not in the list of 10: show the category list and ask user to choose.
- If design tokens are missing: generate template with hardcoded defaults and flag in the report.
- If the template directory already exists: ask before overwriting.
