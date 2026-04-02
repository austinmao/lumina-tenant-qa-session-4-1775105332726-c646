---
name: illustration
description: "Direct custom illustrations, icon design, spot illustrations, and editorial visuals"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /illustration
metadata:
  openclaw:
    emoji: "🖌️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Illustration

Direct custom illustration work -- icon design systems, spot illustrations, editorial illustrations, and decorative elements. This skill produces illustration briefs and direction documents that guide illustrators (human or AI-assisted) toward consistent, on-brand visual assets.

## When to Use

- Creating an icon system for a website or application
- Directing spot illustrations for blog posts, emails, or landing pages
- Commissioning editorial illustrations for long-form content
- Designing decorative elements (dividers, borders, background patterns)
- Establishing an illustration style guide for a brand
- Reviewing illustration deliverables against the direction brief

## Context Loading

Before any illustration direction work:
1. Read `<brand_root>/brand-guide.md` for the brand's visual identity and existing illustration style
2. Read `<brand_root>/tokens/design-system.yaml` for color tokens and spacing scales
3. Read the art direction moodboard for the campaign or project
4. Review existing illustrations in `assets/illustrations/` for style consistency
5. Read the content or page specification that the illustration supports

## Illustration Style Guide

### Establishing Style

When creating an illustration style from scratch (new brand or new direction):

1. **Visual Language Definition**
   - Line quality: clean geometric, hand-drawn organic, or hybrid
   - Fill style: flat color, gradient, textured, outlined
   - Complexity level: minimal (3-5 elements), moderate (6-12 elements), detailed (12+)
   - Perspective: flat/2D, isometric, or mild perspective

2. **Color Rules**
   - Primary illustration palette: subset of brand colors (typically 4-6 colors)
   - Allowed accent colors: for emphasis and variation
   - Background treatment: transparent, brand background color, or contained in a shape
   - Color restriction: illustrations should work in both full-color and monochrome (single brand color)

3. **Character Style** (if applicable)
   - Proportions: realistic, slightly stylized, or abstract
   - Facial detail level: full features, simplified, or faceless
   - Diversity representation: inclusive by default
   - Pose and gesture vocabulary: what emotions and actions are depicted

4. **Consistency Rules**
   - Stroke width: fixed (e.g., 2px at 1x) or proportional
   - Corner radius: sharp, slightly rounded, or fully rounded
   - Shadow style: none, flat offset, or soft drop shadow
   - Grid and sizing: icon grid (24x24, 32x32), spot illustration size ranges

### Output: Style Guide Document

```markdown
## Illustration Style Guide — [Brand/Project]

### Visual Language
- Line: [description]
- Fill: [description]
- Complexity: [minimal/moderate/detailed]
- Perspective: [flat/isometric/perspective]

### Color Palette
| Role | Color | Hex | Usage |
|---|---|---|---|
| Primary | [name] | #XXXXXX | Main shapes |
| Secondary | [name] | #XXXXXX | Supporting elements |
| Accent | [name] | #XXXXXX | Highlights, emphasis |
| Background | [name] | #XXXXXX | Container backgrounds |

### Sizing
- Icons: [size]px grid, [stroke]px stroke
- Spot illustrations: [min]px - [max]px width
- Editorial: [aspect ratio], [min width]px

### Do / Don't
- Do: [specific positive example]
- Don't: [specific negative example]
```

## Icon Design

### Icon System Principles

1. **Grid and Keylines**
   - Use a consistent grid (24x24px is standard for UI icons)
   - Keyline shapes: circle, square, horizontal rectangle, vertical rectangle
   - Optical alignment: visually center icons within the grid, not mathematically
   - Padding: 2px internal padding at 24x24 (content area is 20x20)

2. **Visual Consistency**
   - Consistent stroke width across all icons in the set
   - Consistent corner radius (all sharp, all rounded, or all pill)
   - Consistent fill treatment (all outlined, all filled, or paired sets)
   - Consistent level of detail (do not mix simple and complex icons)

3. **Semantic Clarity**
   - Each icon must be recognizable at its smallest rendered size
   - Test with and without labels -- icons should be identifiable alone when possible
   - Use established conventions for common actions (magnifying glass = search, gear = settings)
   - For novel concepts, pair the icon with a text label

4. **Accessibility**
   - Minimum touch target: 44x44px (the icon can be smaller, the tap area cannot)
   - Sufficient contrast against background (3:1 minimum for UI icons)
   - Never use color alone to distinguish states -- add shape or pattern changes
   - Provide `aria-label` or `aria-hidden` for screen readers

### Icon Brief Format

```markdown
## Icon Brief: [Icon Name]

### Concept
[What the icon represents]

### Usage Context
[Where the icon appears in the UI: button, navigation, status indicator]

### Visual Direction
- Style: [outlined/filled/duo-tone]
- Grid: [24x24/32x32/custom]
- Primary shape: [description]
- Distinguishing feature: [what makes this icon unique in the set]

### States
| State | Treatment |
|---|---|
| Default | [stroke color, fill color] |
| Hover | [change] |
| Active | [change] |
| Disabled | [opacity or color change] |

### Reference
[Existing icons that share similar concepts for consistency reference]
```

## Spot Illustrations

### Purpose
Spot illustrations are small, focused visuals that support content without dominating it. They appear in blog posts, emails, empty states, feature explanations, and section dividers.

### Brief Structure

```markdown
## Spot Illustration Brief: [Name]

### Content Context
[What content this illustration supports -- article topic, feature explanation, etc.]

### Concept
[What the illustration depicts -- be specific about the core visual metaphor]

### Mood
[The emotional tone: playful, calm, energetic, contemplative]

### Composition
- Orientation: [landscape/portrait/square]
- Size range: [min-max px width]
- Background: [transparent/contained/full bleed]

### Key Elements
1. [Primary element]
2. [Secondary element]
3. [Optional detail element]

### Color Treatment
[Full palette / limited palette / monochrome]

### What to Avoid
[Specific visual cliches or off-brand elements]
```

### Size Guidelines

| Context | Recommended Size | Aspect Ratio |
|---|---|---|
| Blog hero | 800-1200px wide | 16:9 or 3:2 |
| Blog inline | 400-600px wide | Flexible |
| Email header | 600px wide | 3:1 or 4:1 |
| Empty state | 200-300px wide | Square or portrait |
| Feature explanation | 300-500px wide | Flexible |

## Editorial Illustrations

### Purpose
Editorial illustrations are larger, more detailed visuals that serve as the primary visual anchor for a piece of content. They carry narrative weight and should be compositionally strong enough to stand on their own.

### Brief Structure

Extend the spot illustration brief with:
- **Narrative**: what story does the illustration tell?
- **Compositional direction**: foreground/midground/background elements
- **Focal point**: where should the viewer's eye go first?
- **Accompanying text**: headline or pull quote that will appear with the illustration
- **Crops**: will this illustration be cropped for different contexts (social media, email, web)?

## Decorative Elements

### Types
- **Dividers**: horizontal rules, section breaks (simple line, illustrated, or pattern)
- **Borders**: frame elements for cards, pull quotes, featured content
- **Background patterns**: repeating motifs for section backgrounds
- **Corner elements**: decorative accents for cards or frames

### Rules
- Decorative elements must be subtle -- they support content, never compete with it
- Use sparingly: one decorative element type per page section maximum
- Must work at all breakpoints (responsive scaling or alternative treatments)
- Must not interfere with readability (sufficient contrast with text)

## Review Criteria

When reviewing illustration deliverables:
1. **Style consistency**: matches the illustration style guide?
2. **Brand alignment**: uses the brand color palette and visual language?
3. **Clarity**: the concept is immediately understandable?
4. **Scalability**: works at the intended size range (test smallest and largest)?
5. **Accessibility**: sufficient contrast, does not rely on color alone?
6. **File quality**: correct format (SVG for icons, SVG or WebP for illustrations), clean paths, no artifacts

## Error Handling

- Illustration does not match the brief: identify specific deviations, reference the style guide, request revision with annotated markup
- Style inconsistency across a set: flag the inconsistency, identify which illustration is the outlier, recommend which direction to align toward
- Accessibility failure: specify the contrast issue, provide the required minimum ratio, suggest color adjustments that maintain the artistic intent

## Boundaries

- Never produce finished illustrations. Output is direction documents and briefs.
- Never approve illustrations that fail accessibility contrast requirements.
- Never create illustration direction that contradicts the brand identity system.
- Never commission illustrations without a clear content context (no decorative art for its own sake).

## Dependencies

- `art-direction` -- campaign visual direction that illustration supports
- `brand-standards` -- brand visual identity system
- `brand-identity-design` -- design tokens and specifications
- `ui-ux-design` -- component designs that consume icons and illustrations

## State Tracking

- `iconSets` -- keyed by set name: icon count, grid size, stroke width, status (in progress/complete)
- `spotIllustrations` -- keyed by name: context, concept, status, file path
- `styleGuides` -- keyed by brand/project: version, last updated, approval status
