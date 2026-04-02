---
name: sanity-dashboard-config
description: "Configure Sanity Studio dashboard with custom desk structure and document types"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /sanity-dashboard-config
metadata:
  openclaw:
    emoji: "🎛️"
    requires:
      bins: ["node"]
---

## Overview

Generates `sanity.config.ts` with a custom desk structure that organises documents by type, adds live previews, and configures the media plugin. Also writes supporting desk structure helper files. Use after `sanity-schema-gen` has produced the schema types.

## Steps

### 1. Read Schema Types

Scan `schemas/index.ts` (or `schemas/` directory) to discover which document types are registered. If no schemas are found, ask the user to run `sanity-schema-gen` first or provide the type list manually.

### 2. Classify Types

Group discovered types into desk structure sections:

| Section | Types |
|---|---|
| **Content** | post, page, author, category |
| **Navigation** | navigation |
| **Site Settings** | settings |
| **Media** | image, media |

Types not in the list above go into a catch-all **Other** section.

### 3. Generate `sanity.config.ts`

Write `sanity.config.ts` at the project root:

```ts
import { defineConfig } from 'sanity'
import { structureTool } from 'sanity/structure'
import { visionTool } from '@sanity/vision'
import { media } from 'sanity-plugin-media'
import { schemaTypes } from './schemas'
import { structure } from './desk-structure'

export default defineConfig({
  name: 'default',
  title: process.env.SANITY_STUDIO_PROJECT_NAME ?? 'Studio',
  projectId: process.env.SANITY_STUDIO_PROJECT_ID!,
  dataset: process.env.SANITY_STUDIO_DATASET ?? 'production',
  plugins: [
    structureTool({ structure }),
    visionTool(),
    media(),
  ],
  schema: { types: schemaTypes },
})
```

### 4. Generate `desk-structure.ts`

Write `desk-structure.ts` with a `structure` export. Use `S.list()` with named items for each section. For each document type add `S.listItem().title(...).child(S.documentList().title(...).filter('_type == $type', { type: '<type>' }))`.

For types that support preview, add `.child(S.document().views([S.view.form(), S.view.component(PreviewPane).title('Preview')]))` (stub component reference; actual preview component is wired in `sanity-preview-routes`).

### 5. Generate `.env.local` Entries

Append the required Sanity Studio env vars to `.env.local` (create if missing, do not overwrite existing keys):
```
SANITY_STUDIO_PROJECT_ID=<placeholder>
SANITY_STUDIO_DATASET=production
SANITY_STUDIO_PROJECT_NAME=My Studio
```
Print a reminder: "Replace placeholders in .env.local with your actual project ID."

### 6. List Required Packages

Print the npm install command for any plugins referenced:
```bash
npm install sanity-plugin-media @sanity/vision
```

## Output

- `sanity.config.ts` — Studio configuration with desk structure and plugins
- `desk-structure.ts` — custom desk structure helper
- `.env.local` — appended with Sanity Studio env var placeholders

## Error Handling

- No schemas found → ask user to provide type list manually; generate config with `schemaTypes: []` placeholder
- Env file write conflict → print the required env vars to console instead of writing; do not overwrite existing values
