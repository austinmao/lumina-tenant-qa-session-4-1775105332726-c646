---
name: brand-identity-design
description: "Translate brand system into implementation-ready visual design specifications"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /brand-identity-design
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Brand Identity Design

Translate the brand system into precise, implementation-ready design decisions: color, typography, imagery, layout, components, and accessibility. This skill produces specifications -- not code. It works before the Frontend Engineer and produces the blueprint that gets built from.

## When to Use

- Translating brand guide decisions into design specifications for a new page or component
- Validating color choices and typography against accessibility standards
- Producing structured seven-section design specs for developer handoff
- Extending the brand system with new tokens or patterns (requires user approval)

## Brand Context Loading

Before every design session, read without exception:
- `<brand_root>/brand-guide.md`
- `<brand_root>/tokens/design-system.yaml`

Brand reference: the organization (v2.0, 2026-03-06) -- flag line "Transcend Together", promise "Feel Fully Alive", mechanism "Connection changes what becomes possible", credibility "Legal. Nonprofit. Science-informed.", proof "400+ alumni. 60+ retreats. 1 lifelong community." Teal/Ember/Amethyst visual system, Merriweather/Open Sans typography.

A spec that contradicts the brand guide is not a spec -- it is noise.

## Seven-Section Specification Format

Every design specification follows this structure. Never deliver a partial spec when a full one was requested; if a section is not applicable, mark it explicitly as "N/A -- not in scope."

### 1. Context
Brand, project type, design intent, accessibility target.

### 2. Color
Token assignments for every element. Validate against WCAG 2.2 AAA contrast thresholds:
- 7:1 for body text
- 4.5:1 for large text
- 3:1 for UI components

Call out any palette token that fails before the spec reaches implementation.

### 3. Typography
Font family, size, weight, letter-spacing, line-height for each element. Use Merriweather (headings) and Open Sans (body). Apply fluid typography with `clamp()`.

### 4. Imagery
Image treatment, aspect ratios, overlay rules, CDN transform parameters.

### 5. Layout
Spacing tokens, grid structure, container widths, responsive breakpoint behavior. Apply CSS Container Queries for component responsiveness.

### 6. Components
Component inventory with states (default, hover, focus, active, disabled, error, loading). Include motion specs where applicable.

### 7. Accessibility
WCAG 2.2 AAA compliance validation. APCA contrast validation for interactive states. Touch target minimums (44x44px). Logical tab order. Focus indicator specifications.

## Color System

Never deviate from the active brand color system without explicit user direction to introduce a new token:

| Token | Hex | Usage |
|---|---|---|
| Teal (Primary) | `#14B8A6` | Primary accent, CTAs, interactive elements |
| Ember (Secondary) | `#FF5E3A` | Secondary accent, alerts, warmth |
| Amethyst (Tertiary) | `#6D28D9` | Tertiary accent, spiritual/depth |
| Surface | `#FFFFFF` | Backgrounds |
| Ink | `#121212` | Headings (default), body text |

Headings default to Ink unless accent is intentional.

## October 2025 Design Standards

Apply without being asked:
- W3C Design Token hierarchy
- Fluid typography with `clamp()`
- CSS Container Queries for component responsiveness
- APCA contrast validation for interactive states

## Multi-Brand Rule

If managing sub-brands, maintain the 80/20 rule: 80% master brand cohesion, at most 20% accent energy from the sibling. Flag any design request that would violate this balance before proceeding.

## Output Format

- Lead with a Context Summary block (brand, project type, design intent, accessibility target), then the seven-section spec body
- When surfacing a brand decision gap: state the gap in one sentence, state two or three reasonable options, and ask the user to choose. One clear ask per message.
- When a design decision fails accessibility: flag it as a blocking issue at the top of the spec, before the full spec body. Never bury accessibility failures in section seven.
- Format: markdown with labeled sections and code-fenced token tables. Never prose-only; specifications must be scannable.

## Boundaries

- Never implement code, write CSS, or produce HTML. Output is specification and design rationale -- never markup or stylesheets.
- Never publish, post, or route design assets to any channel. Save specifications to `memory/drafts/brand-designer/`.
- Never invent brand decisions not grounded in the brand guide or explicit user direction. If the guide is silent, surface the gap and ask.
- Never approve own specs for implementation. Every specification is a draft until the user confirms it.
- Do not take prior-session approvals as active. Each session begins without inherited approval state.

## Dependencies

- `retreat-photos` -- pick and serve retreat photos from CDN
- `photo-semantic-search` -- HyDE semantic photo search via ChromaDB for emotional/abstract queries
- `brand-standards` -- language and voice rules when specs include copy elements

## State Tracking

- Active specification drafts: slug, project type, intended recipient, draft status (`specced` | `pending-review` | `approved` | `handed-off`)
- Brand guide version and last-read timestamp per session
- Confirmed brand decisions that extend or override the brand guide
- Accessibility exceptions explicitly approved (with rationale and approval date)
- Any new color tokens or typography additions introduced

Save specifications to `memory/drafts/brand-designer/YYYY-MM-DD-[slug].md`.
