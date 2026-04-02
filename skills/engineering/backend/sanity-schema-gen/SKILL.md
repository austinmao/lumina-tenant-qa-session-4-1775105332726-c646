---
name: sanity-schema-gen
description: "Generate Sanity CMS schema files from a content model YAML"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /sanity-schema-gen
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins: ["node"]
---

## Overview

Reads a `content-model.yaml` file and generates Sanity Studio TypeScript schema files using `defineType` and `defineField` patterns — one file per content type. Writes all schemas into a `schemas/` directory and exports them from a root `schemas/index.ts`.

## Steps

1. Read `content-model.yaml` from the current directory. Expected structure:
   ```yaml
   types:
     - name: page
       title: Page
       fields: [title, slug, body, seo]
     - name: post
       title: Blog Post
       fields: [title, slug, publishedAt, author, body, categories, seo]
   ```
   If the file is missing, stop and ask the user for the content model path.

2. For each content type in the YAML, generate a TypeScript schema file at `schemas/<type-name>.ts`. Use these field templates:

   | Field name pattern | Sanity type | Options |
   |---|---|---|
   | `title` | `string` | required validation |
   | `slug` | `slug` | source: `title`, required validation |
   | `body` | `array` of `block` | rich text with marks and lists |
   | `author` | `reference` | to: `[{type: 'author'}]` |
   | `image` / ends with `Image` | `image` | with `alt` string field, hotspot: true |
   | `publishedAt` | `datetime` | |
   | `categories` | `array` of `reference` | to: `[{type: 'category'}]` |
   | `navigation` | `array` of `object` | label + href fields |
   | `seo` | `object` | metaTitle, metaDescription, ogImage fields |
   | `settings` | `object` | siteName, siteUrl, logo fields |
   | Unknown field | `string` | with a comment `// TODO: verify type` |

3. Apply `defineType` / `defineField` pattern consistently:
   ```ts
   import { defineType, defineField } from 'sanity'

   export default defineType({
     name: 'page',
     title: 'Page',
     type: 'document',
     fields: [
       defineField({ name: 'title', title: 'Title', type: 'string', validation: Rule => Rule.required() }),
       defineField({ name: 'slug', title: 'Slug', type: 'slug', options: { source: 'title' }, validation: Rule => Rule.required() }),
     ],
   })
   ```

4. Handle the six standard content types explicitly:
   - **page**: title, slug, body, seo object
   - **post**: title, slug, publishedAt, author reference, body, categories array, seo object
   - **author**: name, slug, bio, image with hotspot
   - **navigation**: title, items array (label, href, external boolean)
   - **settings**: siteName, siteUrl, logo image, socialLinks array
   - **image** (media): alt, caption, asset reference — used as a shared image type

5. Generate `schemas/index.ts` that imports and re-exports all types:
   ```ts
   import page from './page'
   import post from './post'
   // ...
   export const schemaTypes = [page, post, author, navigation, settings]
   ```

6. Print a summary listing each file written and its field count.

## Output

- `schemas/<type>.ts` — one file per content type
- `schemas/index.ts` — barrel export for all schema types

## Error Handling

- Missing `content-model.yaml` → ask user for file path; do not generate empty schemas
- Unknown field names → generate as `type: 'string'` with `// TODO: verify type` comment
- Duplicate type names in YAML → generate both, log a warning to the user
