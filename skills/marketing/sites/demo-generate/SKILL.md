---
name: demo-generate
description: Generate a premium branded single-page website HTML and a branded welcome
  email HTML from structured brand data. This is the final Lobster pipeline step in
  the demo-brand-preview workflow. Receives brand JSON from demo-brand-extract, produces
  two standalone HTML documents.
version: 0.2.0
permissions:
  filesystem: write
  network: false
triggers:
- command: /demo-generate
metadata:
  openclaw:
    emoji: ':wrench:'
---

# Overview

<!-- oc:section id="overview" source="authored" checksum="7d3081376727" generated="2026-03-19" -->
Generate two standalone HTML documents from structured brand data: a premium branded single-page website and a professional welcome email at agency-quality visual standards. The LLM uses the brand signals (name, tagline, colors, voice) to produce HTML with inline CSS that reflects the brand identity at agency quality. Outputs valid JSON with siteHtml and emailHtml keys. This is the third Lobster pipeline step — receives brand JSON via stdin and writes results to stdout for the orchestrator.

Enhanced (v0.2.0): when the brand profile includes `designTokens`, `imageLibrary`, or `generatedImages`, uses real token values and real image URLs in the generated HTML. Also passes through `designSystemHtml` from the design-system-doc stage. Outputs extended JSON including `designTokens`, `imageLibrary`, and `warnings`.
<!-- /oc:section id="overview" -->

## Usage

<!-- oc:section id="usage" source="authored" checksum="092567b04b95" generated="2026-03-19" -->
## Steps

1. Receive structured brand JSON from stdin (output of demo-brand-extract)
2. Parse brand data: brandName, tagline, description, colors, voiceKeywords
3. **Enhanced: check for `designTokens` in the brand profile** — if present, use token values for all color and typography declarations:
   - Replace inferred accent colors with exact token hex values (e.g., `color.brand.primary.$value`)
   - Apply token font families to CSS `font-family` declarations
   - Never override with generic fallback colors when tokens are available
4. **Enhanced: check for `imageLibrary` in the brand profile** — if present, use real image URLs in the generated preview:
   - Hero images (`classification: hero`): use as `<img src="...">` in the hero section
   - Headshot images (`classification: headshot`): use in team/about sections
   - Product images (`classification: product`): use in feature/product sections
   - Background images (`classification: background`): use as CSS `background-image`
   - Logo images (`classification: logo`): use in nav/header
   - Use the highest `quality_score` image per slot; fall back to CSS color block if none available
   - **Slot cardinality rules (enforced in script, not LLM prompt)**:
     - `logo`: exactly 1 — the primary nav/header logo, selected by **contrast ratio against the nav background color** (estimated from the brand palette's darkest prominent color). This correctly picks the white logo for dark navs and the dark logo for light navs, rather than guessing by file size or pixel width. Subsequent logos are excluded.
     - `hero`: exactly 1 — the primary hero image or portrait. A second portrait creates a multi-image hero layout the LLM wasn't instructed to handle.
     - `feature-N`: up to 3, always 1-indexed (`feature-1`, `feature-2`, `feature-3`). No bare `feature` slot.
   - **Hero image CSS** (enforced in PROSE_TASK): `object-position: top center` is required alongside `object-fit: cover` to prevent head cropping on portrait photos in a 16:9 container.
5. **Enhanced: check for `generatedImages` in the brand profile** — if present, use AI-generated images for hero and background gap slots not covered by imageLibrary:
   - AI-generated images take lower priority than extracted real images
   - Apply to empty slots only (hero, background) where no real image was placed
6. Generate a complete standalone HTML page (siteHtml):
   - Dark elegant aesthetic with the brand colors as accent
   - Hero section with company name + tagline
   - About section with description
   - CTA section
   - All CSS inline in a style tag
   - Self-contained except Google Fonts CDN
   - Real `<img>` tags with actual URLs when imageLibrary is available; placeholder CSS color blocks otherwise
7. Generate a complete standalone email HTML (emailHtml):
   - Table-based layout, email-safe CSS
   - Branded header, personalized greeting
   - Key value proposition, CTA button
   - Mobile-friendly
8. **Enhanced: pass through `designSystemHtml`** — if provided as input (from the design-system-doc stage), include it in the output JSON as-is. Do not generate it; only pass through.
9. Output valid JSON to stdout:
```json
{
  "brandName": "...",
  "tagline": "...",
  "siteHtml": "<!DOCTYPE html>...",
  "emailHtml": "<!DOCTYPE html>...",
  "designSystemHtml": "<!DOCTYPE html>...",
  "designTokens": { "color": {}, "typography": {} },
  "imageLibrary": [
    {
      "id": "img-001",
      "url": "https://...",
      "local_path": "image-library/001_hero.jpg",
      "classification": "hero",
      "alt_text": "...",
      "quality_score": 0.8
    }
  ],
  "warnings": []
}
```

## Output Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `brandName` | string | yes | From brand profile |
| `tagline` | string | yes | From brand profile |
| `siteHtml` | string | yes | Escaped full HTML document |
| `emailHtml` | string | yes | Escaped full HTML document |
| `designSystemHtml` | string | no | Passed through from design-system-doc stage; omitted if that stage was skipped |
| `designTokens` | object | no | Passed through from brand profile; omitted if not available |
| `imageLibrary` | array | no | Passed through from brand profile; omitted or empty if not available |
| `warnings` | array | yes | Empty array if all stages succeeded; strings describing degraded stages |

## Error Handling

- Invalid brand JSON input: generate with fallback brand name and neutral colors; add warning entry
- Missing `designTokens`: fall back to color inference from brand profile `colors` array; add `"designTokens unavailable, using inferred colors"` to warnings
- Missing `imageLibrary`: generate placeholder CSS color blocks for all image slots; add `"imageLibrary unavailable, using color placeholders"` to warnings
- Generation failure: output error JSON with status field
<!-- /oc:section id="usage" -->

## Requirements

<!-- oc:section id="requirements" source="authored" checksum="d772e77eaf00" generated="2026-03-19" -->
- Filesystem: `write` (writes result JSON to temp file for large outputs)
- Network: `false` (generation is pure LLM work, no external calls)
- No binary dependencies
- No env vars required (model selection handled by gateway config, not hardcoded)
- Optional inputs in brand profile: `designTokens` (W3C tokens object), `imageLibrary` (classified image array), `generatedImages` (AI-generated image paths)
- Optional pass-through input: `designSystemHtml` (HTML string from design-system-doc stage)
<!-- /oc:section id="requirements" -->
