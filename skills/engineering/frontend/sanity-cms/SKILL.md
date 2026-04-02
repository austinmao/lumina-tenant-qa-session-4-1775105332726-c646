---
name: sanity-cms
description: "Build and manage content with Sanity.io headless CMS — schemas, GROQ queries, Studio customization"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Integrate Sanity.io as the headless CMS for web projects. Define schemas, write GROQ queries, customize Studio, and connect to Next.js.

## When to Use
- Setting up a new Sanity project
- Defining content schemas (pages, blog posts, settings)
- Writing GROQ queries for data fetching
- Customizing Sanity Studio

## Key Patterns
- Schema files in sanity/schemas/
- GROQ queries co-located with components
- Portable Text rendering with custom components
- Image pipeline with hotspot/crop support
- Preview mode for draft content
- Webhook-triggered revalidation for ISR
