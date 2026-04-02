---
name: image-classify
description: "Classify downloaded images into semantic slots using vision AI and metadata signals"
version: "2.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /image-classify
metadata:
  openclaw:
    emoji: "🏷️"
    requires:
      bins: ["python3"]
      env: ["OPENAI_API_KEY"]
---

## Overview

Classifies downloaded website images into seven semantic categories using vision model inference (GPT-5.4 mini) combined with metadata signals (URL, alt text, CSS classes, dimensions). Returns a classification and confidence score for each image. Delegates to `scripts/image-classify.py`. Falls back to heuristic-only mode when `OPENAI_API_KEY` is unavailable — pipeline never fails.

## Classification Categories (v2.0)

| Category | Definition |
|---|---|
| `hero` | Wide landscape scene, stage photo, keynote panorama. Aspect ratio > 1.5:1. Dominant visual. |
| `portrait` | Headshot or portrait of a person. Face clearly visible and prominent. Solo subject. |
| `logo` | The brand's OWN logotype, wordmark, icon mark, or monogram. Never AI-generate. |
| `press-logo` | Third-party company logos for social proof ("As seen in…"). NOT the brand's logo. |
| `feature` | Product, offer, book cover, course thumbnail, or content-supporting visual. |
| `background` | Texture, gradient, or ambient photo rendered behind other content. |
| `decorative` | No semantic meaning — dividers, shapes, generic stock. **Default when uncertain.** |

## Steps

1. Receive inputs:
   - `--library <path>`: path to `image-library.yaml` (required — downloaded images with `local_path`, `src`, `alt`, `classification`, `priority`)
   - `--catalog <path>`: path to `image-catalog.yaml` (optional — richer DOM metadata including `dimensions`, `css_classes`, `page_position`)
   - `--output <path>`: output path for `image-classifications.yaml`
2. Run the classify script:
   ```bash
   python3 $REPO_ROOT/scripts/image-classify.py \
     --library "$IMAGE_LIBRARY_MANIFEST" \
     [--catalog "$IMAGE_CATALOG"] \
     --output "$IMAGE_CLASSIFICATIONS" \
     [--model gpt-5.4-mini] \
     [--detail low]
   ```
3. If the script exits 0: return the output YAML path to the caller.
4. If the script exits 1 (hard failure — missing input file, corrupt YAML): report the error.

## Fallback Mode

When `OPENAI_API_KEY` is unset, the script automatically applies heuristic rules (exit 0):

1. Dimensions exactly match 3+ other images in the set → `press-logo`
2. Aspect ratio > 2.5:1 and width > 800px → `hero`
3. Near-square dimensions (ratio < 1.3:1) and file < 20KB → `logo`
4. Portrait orientation (height > width × 1.2) and file > 50KB → `portrait`
5. Both dimensions < 100px → `decorative`
6. Everything else → `feature`

Use `--fallback-only` to force heuristic mode regardless of API key.

## Output

`image-classifications.yaml` with this schema:

```yaml
schema_version: "1.0"
meta:
  source: image-classify.py
  model: gpt-5.4-mini          # "heuristic" when API unavailable
  detail: low
  classified_at: "2026-03-22T12:00:00Z"
  total: 15
  vision_classified: 15
  fallback_classified: 0
classifications:
  - image_id: "logo-62d045be36"
    src: "https://example.com/brand.jpg"
    local_path: "/path/to/brand.jpg"
    classification: logo
    original_classification: logo
    confidence: 0.95
    reasoning: "Typographic wordmark showing brand initials in dark blue"
```

`image_id` is derived from the filename stem (e.g., `logo-62d045be36.jpg` → `logo-62d045be36`).

## Error Handling

- `OPENAI_API_KEY` missing → auto-switch to heuristic-only mode, exit 0
- API rate limit (429) → exponential backoff, 3 retries per image
- API error (5xx) → retry once, then heuristic fallback for that image
- Image file > 10MB → resize to 2048px max if Pillow available, else heuristic fallback
- Image file missing on disk → mark as `decorative` with confidence 0.1, continue
- Unparseable API response → heuristic fallback for that image
- Empty library → write empty output, exit 0

## Requirements

- Filesystem: `read` (reads library and catalog YAML, image files)
- Network: `true` (calls OpenAI vision API)
- Binary: `python3`
- Env var: `OPENAI_API_KEY` (optional — auto-fallback to heuristics if missing)
- Python deps: `pyyaml` (required), `openai` SDK (optional), `Pillow` (optional, for resize)
