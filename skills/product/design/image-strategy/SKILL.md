---
name: image-strategy
description: "Determine image sourcing strategy: which slots to extract from customer site vs generate with AI"
version: "1.1.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /image-strategy
metadata:
  openclaw:
    emoji: "📋"
---

## Overview

Creative Director decision layer for image sourcing in the website preview pipeline. Evaluates the extracted `image-catalog.yaml` (or `image-library.yaml`), and when available, `image-classifications.yaml` (vision-classified), against required visual slots and decides for each slot whether to use an existing extracted image or generate a new one with AI. Outputs `image-strategy.yaml` containing per-slot sourcing decisions. The gap list (slots marked `generated`) feeds directly into `image-generate`.

## Required Slots

The website preview pipeline requires these visual slots to be filled:

| Slot | Purpose | Logo rule |
|---|---|---|
| `hero` | Main above-fold image | Never AI-generate if extracted |
| `background` | Section or page background texture | Can generate |
| `portrait` | Team or founder portrait | Can generate |
| `feature` | Product, offer, or content photograph | Can generate |
| `logo` | Brand logo mark | **Always prefer extracted — never AI-generate** |

**Note:** `press-logo` images are NEVER used to fill the brand `logo` slot and are excluded from all sourcing decisions. They represent third-party logos for social proof sections, not the brand's own identity mark.

Additional slots may be provided by the pipeline; apply the same decision logic.

## Steps

1. Read inputs:
   - `image-classifications.yaml` (preferred, from vision classifier): images with `classification`, `confidence`, `image_id`, `local_path`
   - `image-catalog.yaml` or `image-library.yaml` (fallback if classifications unavailable): extracted images with `classification` and `quality_score` per entry
   - `brand-profile.yaml`: used for context on brand style (does not affect sourcing decision, but informs prompt hints)
   - Optional: a list of required slots passed as input (defaults to the five slots above)
2. **Classification source priority**: prefer `image-classifications.yaml` when available. For entries in that file, confidence >= 0.7 from vision → treat as reliable for sourcing decisions (equivalent to `quality_score >= 0.6`). Exclude `press-logo` and `decorative` entries from slot matching.
3. For each required slot, locate all classified images whose `classification` matches the slot:
   - Map `portrait` → `portrait` slot; `feature` → `feature` slot
   - `press-logo` images are EXCLUDED — never fill any slot
   - If multiple matches exist, select the one with the highest `confidence` (vision) or `quality_score` (heuristic)
   - If no match exists, the slot is unfilled
4. Apply the decision matrix:
   - `quality_score >= 0.6` → **use extracted** (source: `extracted`)
   - `0.4 <= quality_score < 0.6` → **use extracted** (marginal quality; note in output)
   - `quality_score < 0.4` → **generate** (too low quality; source: `generated`)
   - Slot unfilled → **generate** (source: `generated`)
   - **Logo slot exception**: always `extracted` if any logo image exists in catalog, regardless of quality_score. If no logo is found, mark source as `none` (do not generate a logo with AI — logos require brand authenticity)
4. For each slot marked `generated`, construct a `generate_prompt_hint`:
   - Describe what would make this slot ideal for the specific brand context
   - Include any relevant style signals from `brand-profile.yaml` (e.g., "warm earthy tones", "outdoor retreat setting")
   - Keep the hint under 200 characters; it is appended to the base slot prompt in `image-generate`
5. For each slot marked `extracted`, set `image_id` to the `id` field of the selected catalog entry.
6. Write `image-strategy.yaml`:
   ```yaml
   slots:
     - slot: hero
       source: extracted
       image_id: "img-003"
       quality_score: 0.82
       generate_prompt_hint: ""
     - slot: background
       source: generated
       image_id: ""
       quality_score: 0.0
       generate_prompt_hint: "Warm desert tones, subtle texture, suitable for overlaying white text"
     - slot: logo
       source: none
       image_id: ""
       quality_score: 0.0
       generate_prompt_hint: ""
   gap_list:
     - background
     - headshot
   ```
   - `gap_list`: array of slot names where `source: generated` — this is the direct input to `image-generate`

## Decision Matrix Summary

```
confidence >= 0.7 (vision) or quality_score >= 0.6 → extracted
0.4 <= quality_score < 0.6 → extracted (marginal)
quality_score < 0.4 → generated
slot unfilled → generated
logo, any quality → extracted
logo, not found → none (skip AI generation)
press-logo → excluded (never fill any slot)
decorative → excluded (never fill any slot)
```

## Output

- `image-strategy.yaml`: per-slot decisions with `source`, `image_id`, `quality_score`, and `generate_prompt_hint`
- `gap_list` array in the YAML: slots that need AI generation

## Error Handling

- Empty catalog (no extracted images): all slots default to `generated`; logo slot defaults to `none`
- Missing `brand-profile.yaml`: set `generate_prompt_hint` to empty string; continue
- Unrecognized slot name in input list: apply standard decision matrix, include in output
- Catalog entry missing `quality_score`: treat as `0.0` (unfilled)

## Requirements

- Filesystem: `read` (reads catalog and brand profile)
- Network: `false` (pure LLM reasoning, no external calls)
- No binary dependencies
- No env vars required
