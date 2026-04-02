---
name: image-generate
description: "Generate brand-consistent AI images to fill visual gaps in website previews"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /image-generate
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env: ["OPENAI_API_KEY"]
      bins: ["curl", "python3"]
---

## Overview

AI image generation for website preview pipelines. Receives a gap list of image slots that could not be filled from the customer's existing site (e.g., hero, background, headshot) plus brand profile data. Generates one image per slot using the OpenAI image generation API (gpt-image-1), sized 1024x1024. Writes each image to `artifacts/generated-images/` and produces a `generated-images.yaml` manifest. On API failure, creates a branded SVG color-block placeholder instead.

## Steps

1. Read inputs:
   - `image-strategy.yaml` or an explicit gap list: each entry has `slot` (e.g., `hero`, `background`, `headshot`) and an optional `generate_prompt_hint`
   - `brand-profile.yaml`: contains `colors` (hex array), `typography.primary_font`, `style_keywords` (array of tone/aesthetic words)
2. For each slot in the gap list, construct a generation prompt:
   - Start with the slot type description (see Slot Prompts below)
   - Append brand color context: "Brand primary color: {hex}. Secondary: {hex}."
   - Append style keywords from the brand profile: "Visual style: {keyword1}, {keyword2}."
   - Append the `generate_prompt_hint` from strategy if provided
   - Keep prompt under 1000 characters
3. Call OpenAI image generation API for each slot:
   ```
   POST https://api.openai.com/v1/images/generations
   Authorization: Bearer $OPENAI_API_KEY
   {
     "model": "gpt-image-1",
     "prompt": "<constructed prompt>",
     "n": 1,
     "size": "1024x1024"
   }
   ```
4. Download the returned image URL to `artifacts/generated-images/<slot>-<index>.png` using curl.
5. On API failure (non-200, rate limit, quota exceeded):
   - Log the error with slot name and HTTP status
   - Create a branded SVG placeholder: a rectangle filled with the brand primary color, centered text showing the slot label in the brand font family
   - Write to `artifacts/generated-images/<slot>-<index>.svg`
   - Continue with remaining slots — one failure does not halt generation
6. After all slots are processed, write `generated-images.yaml` manifest:
   ```yaml
   entries:
     - slot: hero
       local_path: "artifacts/generated-images/hero-0.png"
       source: generated
       model: gpt-image-1
       prompt_summary: "Wide cinematic shot..."
       fallback: false
     - slot: background
       local_path: "artifacts/generated-images/background-0.svg"
       source: generated
       model: fallback-svg
       prompt_summary: ""
       fallback: true
   ```
7. Generate exactly N images (one per gap slot). Do not generate extras.

## Slot Prompts

Use these base descriptions per slot type:

- `hero`: "Wide cinematic photograph, warm natural light, human presence implied, aspirational and inviting atmosphere, professional editorial quality"
- `background`: "Abstract textured background, soft gradients, no sharp subjects, suitable for overlaying text, minimal and sophisticated"
- `headshot`: "Professional portrait photograph, natural light, warm expression, blurred background, editorial quality"
- `product`: "Clean product photography on neutral background, soft shadows, professional studio lighting"
- `event`: "Candid group photograph at an intimate workshop or retreat setting, authentic expressions, warm ambient light"
- `decorative`: "Abstract geometric pattern, brand-aligned colors, subtle texture, non-distracting"

## Output

- `artifacts/generated-images/` — PNG images (or SVG fallbacks) named `<slot>-<index>.png`
- `generated-images.yaml` — manifest of all generated images with metadata

## Error Handling

- Missing `OPENAI_API_KEY`: notify user "Set OPENAI_API_KEY in environment" and stop before making any API calls
- Per-slot API failure: create SVG placeholder, set `fallback: true` in manifest, continue
- All API calls fail: produce all SVG placeholders; manifest remains complete with `fallback: true` on every entry
- Invalid brand profile: use neutral fallback values (color: `#1a1a1a`, style: "professional, clean")

## Requirements

- Filesystem: `write` (writes generated images and manifest)
- Network: `true` (calls OpenAI API and downloads image URLs)
- Env: `OPENAI_API_KEY`
- Bins: `curl` (image downloads), `python3` (SVG placeholder generation if needed)
- Reasoning level: high — creative prompt construction and brand alignment matter
