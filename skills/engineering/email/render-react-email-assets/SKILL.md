---
name: render-react-email-assets
description: "Deterministically render React Email assets for orchestration pipelines into canonical HTML and plain-text artifacts"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /render-react-email-assets
metadata:
  openclaw:
    emoji: "🧾"
    requires:
      bins: ["pnpm", "node"]
      os: ["darwin"]
---

# Render React Email Assets

Use this skill when a pipeline needs canonical email render artifacts for admin
preview, QA, or downstream delivery records.

This is an orchestration-layer render capability. It is not an email-copy skill
and it is not a freeform HTML generation skill.

## Purpose

The renderer is the deterministic boundary between:

- structured email content inputs
- React Email component rendering
- canonical pipeline artifacts

Pipelines should store rendered HTML and plain text as their operator-facing
artifacts. Source files or template wrappers are implementation details.

## Canonical Output Contract

Every render run must produce:

1. `render_manifest.json`
2. one rendered HTML file per email asset
3. one plain-text file per email asset

The manifest is authoritative. Downstream steps such as verify, brand gate,
record-create, admin preview, and E2E should read subjects and metadata from the
manifest rather than inferring from source files.

## Current Adapters

### 1. Campaign spec bundle

Input: run-scoped Forge JSON specs under `run.paths.forge_specs`

Command:

```bash
pnpm --dir web exec tsx --tsconfig tsconfig.scripts.json \
  scripts/render-react-email-assets.ts --pipeline-id <pipeline-id>
```

Outputs:

- rendered `.html` files under `run.paths.staged_email_dir`
- `.txt` plain-text files under `run.paths.staged_email_dir`
- manifest at `run.paths.render_manifest`

### 2. Template registry

For registry-backed templates such as newsletters, the current concrete render
engine remains `templates/email/render.ts`. Pipelines that still use that path
should adopt this skill's output contract when they migrate:

- canonical HTML output
- canonical plain text output
- render manifest describing subject, asset slug, sequence, and metadata

## Rules

- Rendered HTML, not TSX source, is the canonical asset for admin preview.
- Plain text must be generated alongside HTML for every email asset.
- The render step must be deterministic and must not call a model.
- Store render metadata with each asset: subject, preview text, variant,
  source type, and plain text.
- Downstream pipeline steps must not depend on implementation markers such as
  `CampaignEmailTemplate` string checks.

## Notes

- Authoring skills such as `react-email-templates` and `email-campaign-html`
  are upstream of this renderer.
- Delivery skills consume the outputs of this renderer; they should not be the
  place where the render contract is invented.
