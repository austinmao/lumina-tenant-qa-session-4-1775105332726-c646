---
name: graphic-design
description: "Create social media graphics / design email headers / build presentation decks / produce infographics"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /graphic-design
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      os: ["darwin"]
---

# Graphic Design Skill

Produces specifications and code for visual assets: social media graphics, email headers, presentation decks, and infographics. Generates SVG/HTML with design tokens and platform-specific dimensions. Ported from Naksha-studio's graphic-designer reference.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` for colors, fonts, spacing.
4. Read `<brand_root>/brand-guide.md` for logo usage rules.

---

## Steps

### 1. Determine asset type

| Asset type | Subtypes |
|---|---|
| **Social media** | Instagram post (1080x1080), story (1080x1920), LinkedIn (1200x627), Twitter/X (1600x900), Facebook cover (820x312), OG image (1200x630) |
| **Email header** | Full-width hero (600x300), Logo bar (600x80), Divider (600x120) |
| **Presentation** | Title slide (1920x1080), Content, Section break, Data, Quote, CTA slide |
| **Infographic** | Vertical (800xN), Process flow, Comparison, Timeline, Data viz |

### 2. Define visual composition

**Layout grid**: Safe zones (10% inset for social), text zones, logo placement, image zones.

**Typography hierarchy per format**:
- Social: headline 48-72px bold, sub 24-36px, body 18-24px
- Email: headline 28px bold, sub 16-20px, body 14-16px
- Slides: headline 60-80px bold, sub 32-40px, body 24-32px
- Infographic: headline 36-48px bold, sub 20-28px, body 14-18px

**Color rules**:
- Background: brand surface or dark variant
- Text: primary with sufficient contrast (WCAG AA)
- Accents: primary or accent for highlights
- Photo overlay: 60-80% dark for text legibility

### 3. Generate the asset

Produce as SVG (social, email, infographic) or HTML/CSS (presentations). All visual properties reference design tokens.

### 4. Apply brand constraints

- Logo: exact brand asset, never stretch or recolor
- Colors: only from token palette
- Fonts: only from brand font stacks
- No clip art or stock cliches

### 5. Platform-specific exports

Generate size variants per platform from the same composition.

---

## Output

Write to `<site_dir>/graphics/<type>/` and summary to `memory/reports/graphic-design-<type>.md`:

```markdown
## Graphic Design — <type>
Site: <site_id> | Date: YYYY-MM-DD

### Asset Spec
[dimensions, safe zones, typography]

### Platform Variants
[table of sizes]

### Files Generated
[list]
```

---

## Guidelines

- Social text must be readable at 50% zoom (540px width minimum legibility).
- Email headers: use web-safe font fallbacks (custom fonts stripped by email clients).
- Slides: 6x6x6 rule (6 words headline, 6 bullets max, 6 words per bullet).
- Max 3 colors per graphic (excluding photos and neutrals).
- All graphics need alt text for accessibility.

---

## Error Handling

- No site context: prompt `/site <name>`.
- Brand assets missing: note in output, use placeholder dimensions.
- Unsupported type: show supported list and ask user to choose.
