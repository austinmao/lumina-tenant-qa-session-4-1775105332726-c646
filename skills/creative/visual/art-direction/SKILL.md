---
name: art-direction
description: "Create campaign visual concepts, moodboards, photography direction, and color palettes"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /art-direction
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Art Direction

Create visual concepts for campaigns, moodboards, photography direction briefs, and color palette selections. This skill translates brand strategy and campaign objectives into visual direction that guides designers, photographers, and content creators toward a cohesive visual outcome.

## When to Use

- Developing the visual concept for a new campaign (retreat launch, seasonal promotion, event)
- Creating a moodboard for a website redesign, landing page, or email series
- Writing a photography direction brief for a photo shoot or stock photo selection
- Selecting or extending color palettes for a specific campaign or content initiative
- Establishing visual tone for a new content series (blog, social, video)
- Reviewing visual assets for consistency with the art direction brief

## Context Loading

Before any art direction work:
1. Read `<brand_root>/brand-guide.md` for the brand's visual identity system
2. Read `<brand_root>/tokens/design-system.yaml` for the design system's color, typography, and spacing tokens
3. Read the campaign brief or strategic brief for objectives, audience, and messaging
4. Review existing campaign visual assets in `assets/` for consistency with prior work
5. Read `<brand_root>/assets/logos/` inventory to understand available brand marks

## Moodboard Creation

### Purpose
A moodboard captures the intended visual feeling of a campaign before any design work begins. It aligns all stakeholders on visual direction and prevents costly revisions later.

### Moodboard Structure

Every moodboard includes:

1. **Visual Theme Statement** (1-2 sentences)
   - What emotional response should the visuals evoke?
   - What story do the visuals tell?
   - Example: "Warm, intimate, grounded. Visuals feel like a personal invitation into a trusted space -- not a sales pitch."

2. **Color Direction**
   - Primary palette: 2-3 colors from the brand system
   - Accent palette: 1-2 campaign-specific colors (must harmonize with brand)
   - Mood: warm/cool, saturated/muted, light/dark
   - Specific hex values tied to design tokens where possible

3. **Typography Direction**
   - Headline treatment (font, weight, size range, letter-spacing)
   - Body text treatment
   - Accent text (pullquotes, callouts, labels)
   - Any campaign-specific typographic flourishes (hand-lettered elements, custom treatments)

4. **Photography Direction**
   - Subject matter (people, places, objects, abstract)
   - Lighting (natural, studio, golden hour, diffused)
   - Composition (close-up, wide, centered, rule of thirds)
   - Color treatment (warm grade, desaturated, vibrant)
   - What to avoid (stock photo cliches, forced smiles, sterile environments)

5. **Texture and Pattern**
   - Background treatments (solid, gradient, textured, photographic)
   - Pattern usage (geometric, organic, none)
   - Surface quality (matte, glossy, tactile, paper-like)

6. **Reference Images**
   - 5-10 reference images that capture the intended feeling
   - For each reference, note what specifically is relevant (color palette, composition, mood, texture)
   - References are directional, not literal -- note what to take and what to leave

### Output Format

```markdown
## Moodboard: [Campaign Name]

### Visual Theme
[1-2 sentence statement]

### Color Direction
| Role | Color | Hex | Token |
|---|---|---|---|
| Primary | [name] | #XXXXXX | [token ref] |
| Secondary | [name] | #XXXXXX | [token ref] |
| Accent | [name] | #XXXXXX | [new/token ref] |

### Typography Direction
- Headlines: [font, weight, style notes]
- Body: [font, weight, style notes]
- Accent: [font, weight, style notes]

### Photography Direction
[Detailed brief — see Photography Direction section]

### Texture & Pattern
[Description of background and surface treatments]

### References
1. [Description of reference image and what to take from it]
2. ...
```

## Photography Direction

### Subject Direction

For campaigns featuring people:
- Authentic expressions (not posed or forced)
- Environmental context (real settings, not studio backdrops)
- Diversity in representation (age, ethnicity, body type) -- reflect the actual community
- Activity-based shots (doing, not just standing)
- Candid moments over staged compositions

For campaigns featuring spaces:
- Atmosphere over architecture (how it feels, not just how it looks)
- Natural light preferred
- Human presence or evidence of human activity (lived-in, not showroom)
- Scale references (show how the space relates to people)

### Lighting Brief

| Lighting Style | When to Use | Visual Effect |
|---|---|---|
| Natural window light | Intimate, warm campaigns | Soft shadows, warm tones |
| Golden hour (outdoor) | Aspirational, transformative | Warm glow, long shadows |
| Overcast diffused | Calm, contemplative | Even light, muted shadows |
| Studio soft box | Product shots, portraits | Controlled, professional |
| Candlelight/fire | Ritual, ritual | Warm, intimate, dramatic |

### Color Grading Direction

Describe the post-processing treatment:
- Warm shift (orange/yellow shadows) vs cool shift (blue shadows)
- Saturation level (vivid, natural, desaturated)
- Contrast (high contrast/dramatic vs low contrast/dreamy)
- Specific adjustments (lift blacks, crush shadows, split toning)

### What to Avoid

Document anti-patterns explicitly:
- Generic stock photo aesthetics (perfectly diverse group laughing at salad)
- Over-processed HDR look
- Cliche spiritual imagery (lotus flowers, chakra diagrams, generic meditation poses)
- Clinical or corporate environments
- Forced or inauthentic expressions

## Color Palette Selection

### Extending the Brand Palette

When a campaign needs colors beyond the core brand palette:
1. Start with the brand's primary and secondary colors
2. Select accent colors that harmonize (analogous, complementary, or triadic)
3. Test the accent colors against all brand backgrounds (light, dark)
4. Verify accessibility (contrast ratios for text usage)
5. Define usage rules (accent is for CTAs only, not backgrounds)

### Seasonal and Campaign Palettes

For time-limited campaigns:
- Derive from the brand palette (never replace it)
- Maximum 2 new accent colors per campaign
- Document the palette with hex values, usage rules, and expiry date
- Remove campaign colors from the system after the campaign ends

### Color Accessibility

All color combinations must pass WCAG AA:
- Normal text on background: 4.5:1 contrast ratio minimum
- Large text on background: 3:1 contrast ratio minimum
- Interactive elements: 3:1 contrast ratio against adjacent colors
- Never rely on color alone to convey meaning (add icons, labels, or patterns)

## Visual Review Criteria

When reviewing visual assets against the art direction brief:
1. **On-brand**: does it align with the brand's visual identity system?
2. **On-brief**: does it match the campaign's visual direction?
3. **Accessible**: do color combinations pass contrast requirements?
4. **Authentic**: does it feel genuine, not generic?
5. **Consistent**: does it match other assets in the same campaign?

Rate each criterion: pass, conditional pass (minor adjustment needed), fail (redo required).

## Boundaries

- Never produce finished design files (PSDs, Figma files, illustrations). Output is direction documents.
- Never select specific stock photos for purchase -- provide direction for selection.
- Never override the brand identity system without Creative Director approval.
- Never approve visual assets that fail accessibility contrast requirements.

## Dependencies

- `brand-standards` -- brand visual identity system that all art direction must follow
- `brand-identity-design` -- design system tokens and specifications
- `illustration` -- custom illustration direction (separate skill)
- `ui-ux-design` -- component design that consumes art direction

## State Tracking

- `moodboards` -- keyed by campaign name: status (draft/approved), visual theme, color palette, approval date
- `photoBriefs` -- keyed by campaign name: subject direction, lighting, color grading, status
- `campaignPalettes` -- keyed by campaign name: accent colors, usage rules, expiry date
