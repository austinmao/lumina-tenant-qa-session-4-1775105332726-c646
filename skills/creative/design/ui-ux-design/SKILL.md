---
name: ui-ux-design
description: "Create component design specs with wireframes, token assignments, interaction states, and motion specs"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /ui-ux-design
metadata:
  openclaw:
    emoji: "🖌️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# UI/UX Design

Create component and page design specifications including wireframes, color/typography token assignments, interaction states, responsive breakpoint maps, and motion specs. This skill produces design artifacts only -- not production code.

## When to Use

- Designing a new page or component that needs a design spec before implementation
- Translating brand guide decisions into component-level visual design
- Specifying interaction states, animation choreography, and responsive behavior
- Creating the design blueprint that the Frontend Engineer builds from

## Context Loading

Before producing any design artifact:
1. Read `memory/site-context.yaml` to determine the active site. If it does not exist, prompt: "No active site set. Run `/site <name>` first."
2. Read `<brand_root>/brand-guide.md` and `<brand_root>/tokens/design-system.yaml`
3. Read `docs/web/web-ref.yaml` for confirmed production breakpoints, layout constraints, and component patterns

## Design Spec Structure

Every design spec includes:

1. **Layout wireframe** -- ASCII by default; break complex components into labeled sub-wireframes
2. **Color token assignments** -- table format: element, token, hex, rationale
3. **Typography choices** -- font family, size, weight, letter-spacing, line-height per element
4. **Interaction states** -- hover, focus, active, disabled states for every interactive element
5. **Responsive behavior** -- mobile/tablet/desktop breakpoint behavior
6. **Motion specs** -- timing, easing, and trigger guidance for animations

## Design Philosophy

### Typography Range
Work the full typographic range within brand fonts: size, weight, letter-spacing, case, and line-height to establish hierarchy. Display text should be expressive, even risky in its scale. Body text should be legible and refined. Pair them like actors in a scene. Typography is a design element, not just content.

### Color Position
Palettes take a clear position: bold and saturated, moody and restrained, or high-contrast and minimal. Lead with a dominant color, punctuate with sharp accents. Avoid timid, non-committal distributions. All choices stay within brand tokens.

### Motion Design
Focus on high-impact moments: one well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise. Include motion specs in every design artifact -- the Frontend Engineer needs timing, easing, and trigger guidance, not just visual layout. For React components, reference the Motion library (Framer Motion / motion-one) as the implementation path.

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap and z-depth. Diagonal flow. Grid-breaking elements. Dramatic scale jumps. Full-bleed moments. Generous negative space OR controlled density.

### Backgrounds and Visual Details
Create atmosphere and depth rather than defaulting to solid colors. Apply creative forms: gradient meshes, noise and grain overlays, geometric patterns, layered transparencies and glassmorphism, dramatic or soft shadows and glows, parallax depth, decorative borders and clip-path shapes, print-inspired textures (halftone, duotone, stipple), knockout typography, and custom cursors -- within the brand's visual sensibility.

### Spec Depth Matches Ambition
A rich atmospheric component needs a comprehensive spec -- full animation choreography, stacking order, effect list, and state breakdowns. A refined minimal component needs precision -- exact spacing values, subtle state transitions, typographic exactness.

## Anti-Patterns (NEVER)

- Predictable layouts and component patterns
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Cookie-cutter designs that lack context-specific character
- No two component specs should share the same layout DNA -- each must feel built specifically for its component's purpose and position

## Accessibility

Design for WCAG AA from the start -- not as a retrofit:
- Every color pairing meets 4.5:1 contrast for normal text and 3:1 for large text or UI components
- Touch targets minimum 44x44px
- Logical tab order
- Clear focus indicators
- No interaction requiring hover-only discovery

## Output Format

- Lead with component name, page/placement context, and wireframe
- Then token assignments, then interaction states
- Color and typography decisions as a table: element, token, hex, rationale
- When discovering a design gap: state the gap, propose a default grounded in the existing brand system, and ask before proceeding
- One design per message unless options are requested

## Boundaries

- Never write production code (TypeScript, JSX, CSS). Output is always design artifacts.
- Never introduce fonts, colors, or spacing outside the brand design system without explicit direction.
- Never hand off to implementation without explicit approval of the design spec.

## Dependencies

- `brand-standards` -- voice and language rules when specs include copy elements
- `brand-identity-design` -- seven-section design specification format for formal specs
- `retreat-photos` -- CDN photo selection for design mockups
- `photo-semantic-search` -- emotional/abstract image queries

## State Tracking

Track in `memory/designer-state.json`:
- `activeSpecs` -- keyed by spec slug: component name, page context, status (`ideation` | `specced` | `pending-approval` | `approved` | `handed-off`), approval timestamp
- `openGaps` -- design decisions awaiting input
- `designDecisions` -- array of decisions made with rationale

Save design specs to `memory/drafts/design/YYYY-MM-DD-[slug].md`.
