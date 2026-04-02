---
name: brand-extract
description: Extract brand signals from raw HTML for downstream generation.
version: 0.2.0
permissions:
  filesystem: none
  network: false
triggers:
- command: /brand-extract
metadata:
  openclaw:
    emoji: ':wrench:'
---

# Overview

<!-- oc:section id="overview" source="authored" checksum="81b998efbfa0" generated="2026-03-19" -->
Extract brand signals from raw HTML provided via stdin. Parses meta tags, heading text, color references, and company identity. Outputs structured JSON with brandName, tagline, description, colorPalette, and voiceKeywords. This is the second Lobster pipeline step — receives HTML from demo-web-fetch and feeds structured brand data to demo-generate.

Enhanced (v0.2.0): also consumes Dembrandt design tokens (`artifacts/design-tokens.json`) and a classified image library (`artifacts/image-library.yaml`) when available. When these inputs exist, they take precedence over inferred HTML values. Fallback to HTML inference is always preserved.
<!-- /oc:section id="overview" -->

## Usage

<!-- oc:section id="usage" source="authored" checksum="f861f8013c3d" generated="2026-03-19" -->
## Steps

1. Receive raw HTML + brand signals summary from stdin (output of demo-web-fetch)
2. Parse the HTML to extract: page title, meta description, theme-color, og:image URL, h1/h2 headings, prominent text blocks
3. Infer: company/person name, primary tagline, brand voice keywords, color palette hints
4. **Enhanced: check for `artifacts/design-tokens.json`** — if present, load it and use as the authoritative source for colors and typography instead of inferring from HTML:
   - Extract `color.*` token groups → populate `colorPalette` (hex values, named roles)
   - Extract `typography.*` token groups → populate `typography` (fontFamily, scale, weights)
   - Mark `tokensSource: "dembrandt"` in output
5. **Enhanced: check for `artifacts/image-library.yaml`** — if present, parse the entries array and include classified images in the brand profile:
   - Include all entries as-is in the `imageLibrary` array
   - Use hero/headshot images to inform voiceKeywords (e.g., presence of headshots → add "personal")
   - Mark `imageSource: "extracted"` in output
6. Output valid JSON to stdout:
```json
{
  "brandName": "...",
  "tagline": "...",
  "description": "...",
  "colors": ["#hex1", "#hex2"],
  "voiceKeywords": ["warm", "professional"],
  "ogImage": "url",
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
  "typography": {
    "fontFamily": "Inter, sans-serif",
    "headingFont": "Playfair Display",
    "scale": "1.25"
  },
  "tokensSource": "dembrandt",
  "imageSource": "extracted"
}
```

## Fallback Behavior

- If `artifacts/design-tokens.json` does not exist: infer colors and typography from HTML meta tags, CSS variables, and inline styles as before (v0.1 behavior). Set `tokensSource: "inferred"`.
- If `artifacts/image-library.yaml` does not exist: omit `imageLibrary` from output or set to empty array. Set `imageSource: "none"`.
- Both fallbacks can be active simultaneously — behavior degrades gracefully.

## Output

Valid JSON to stdout — one object, no markdown wrapping. All new fields (`designTokens`, `imageLibrary`, `typography`, `tokensSource`, `imageSource`) are optional and omitted when not available.

## Error Handling

- Empty stdin: output JSON with brandName "Unknown" and empty arrays
- Malformed HTML: best-effort extraction, never fail
- Malformed design tokens JSON: log warning, fall back to HTML inference (`tokensSource: "inferred"`)
- Malformed image library YAML: log warning, omit imageLibrary from output
<!-- /oc:section id="usage" -->

## Requirements

<!-- oc:section id="requirements" source="authored" checksum="5d05bddc2bff" generated="2026-03-19" -->
- Filesystem: `none`
- Network: `false` (processes HTML already fetched)
- No binary dependencies
- No env vars required
- Optional inputs: `artifacts/design-tokens.json` (W3C tokens format), `artifacts/image-library.yaml` (classified image manifest)
<!-- /oc:section id="requirements" -->
