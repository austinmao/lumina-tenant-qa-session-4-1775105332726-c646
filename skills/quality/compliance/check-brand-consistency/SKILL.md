---
name: check-brand-consistency
description: "Check page against brand guidelines / validate brand compliance before publish"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      os: ["darwin"]
---

# Brand Consistency Check Skill

Validates a page against brand guidelines before publishing. Checks colors, typography, logo usage, CTA language, and voice alignment.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read brand assets:
   - `<brand_root>/brand-guide.md` -- voice, positioning, words to avoid.
   - `<brand_root>/tokens/design-system.yaml` -- color palette, typography scale.
   - `<brand_root>/asset-checklist.md` -- required brand assets per page type (if exists).

---

## Steps

### 1. Color validation

- Extract all color values used on the page (CSS custom properties, inline styles, class-based tokens).
- Compare against the approved palette in `design-system.yaml`.
- Flag any color not in the approved palette.
- Check that primary and accent colors are used in their designated roles.

### 2. Typography validation

- Check font families match the brand spec.
- Verify font sizes follow the typographic scale (no arbitrary sizes).
- Check line heights and letter spacing conform to the design system.
- Flag any inline font overrides that deviate from tokens.

### 3. Logo usage

- If the page includes a logo, verify:
  - Correct logo variant for the context (horizontal, vertical, icon).
  - Minimum clear space around the logo.
  - Logo is not stretched, recolored, or modified.
- Cross-reference logo filenames against `assets/brand/logos/`.

### 4. CTA language

- Extract all button and link text on the page.
- Compare against approved CTA language from the brand guide.
- Flag CTAs that use generic language ("Click here", "Submit") instead of brand-aligned phrases.
- Check the primary CTA matches the brand guide's designated primary CTA.

### 5. Voice and tone

- Sample 3-5 content blocks from the page.
- Check against brand guide guardrails (words to avoid, tone guidelines).
- Flag any language that conflicts with brand positioning (e.g., "hypey" or "salesy" phrasing if the brand prohibits it).

### 6. Asset checklist (if available)

- If `<brand_root>/asset-checklist.md` exists, verify all required assets for this page type are present.

---

## Output

```markdown
## Brand Consistency Report — <page_path>
Site: <site_id> | Date: YYYY-MM-DD

### Compliance Score: X/10

### Issues
#### Colors
- [list deviations]

#### Typography
- [list deviations]

#### Logo
- [list issues]

#### CTAs
- [list non-compliant CTAs with suggested replacements]

#### Voice & Tone
- [list flagged phrases with suggested alternatives]

### Passed
- [list compliant checks]
```

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If brand guide is not found at `<brand_root>/brand-guide.md`: report the missing file and stop -- brand check cannot run without it.
- If design tokens file is missing: skip color/typography token validation but note it in the report.
