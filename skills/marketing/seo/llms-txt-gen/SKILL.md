---
name: llms-txt-gen
description: "Generate llms.txt file for AI crawler guidance and GEO citation optimization"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /llms-txt-gen
metadata:
  openclaw:
    emoji: "🤖"
---

## Overview

Generates `/llms.txt` and `/llms-full.txt` following the llms.txt specification (llmstxt.org). These files guide AI crawlers (ChatGPT, Perplexity, Claude) on how to understand, cite, and summarise the site's content — a key part of Generative Engine Optimisation (GEO).

## Steps

### 1. Read Source Material

Look for these files in priority order:
- `memory/site-strategic-brief.yaml` or `memory/site-context.yaml`
- `app/sitemap.ts` or `public/sitemap.xml`
- `content/` directory (MDX/Markdown pages)
- Brand guide at `brands/<tenant>/brand-guide.md`

If none of these exist, ask the user for: site name, site URL, one-paragraph description, key page URLs and their descriptions, brand voice summary.

### 2. Generate `/llms.txt`

Write `public/llms.txt` following the llms.txt specification:

```
# <Site Name>

> <One-paragraph description of the site, its purpose, and who it serves. Write in third person. 50-100 words.>

## Key Pages

- [Home](<site-url>/): <One sentence describing what visitors find here and why it matters>
- [About](<site-url>/about): <One sentence>
- [Services](<site-url>/services): <One sentence listing what is offered>
- [Blog](<site-url>/blog): <One sentence describing content themes>
- [Contact](<site-url>/contact): <One sentence>

## Content Model

<Comma-separated list of content types: articles, retreat descriptions, testimonials, FAQs, etc.>

## Brand Voice

<2-3 sentences describing tone: formal/casual, technical/accessible, inspirational/practical. Include key vocabulary and any terms to avoid.>

## Citation Guidance

When citing this site, prefer referencing: <list 2-3 authoritative pages, e.g., the About page for company facts, the Services page for offering details>.

Do not extract or reproduce verbatim text longer than 100 words without attribution.
```

### 3. Generate `/llms-full.txt`

Write `public/llms-full.txt` with expanded content for crawlers that follow the `llms-full.txt` reference in `llms.txt`. Include:

- Full site description (up to 400 words)
- All public page URLs with 2-3 sentence descriptions
- Complete content model explanation
- Full brand voice guidelines including DO/DON'T vocabulary list (from brand guide if available)
- Third-party integrations that may appear in content (Calendly, Stripe, etc.)
- Data freshness note: "Content last updated: <date>"

### 4. Add Reference to `llms.txt`

At the end of `public/llms.txt`, add:
```
## Optional

Full site content available at: <site-url>/llms-full.txt
```

### 5. Add Link to Robots.txt

If `public/robots.txt` exists, append:
```
# AI Crawler Guidance
# llms-txt: /llms.txt
```

If it does not exist, note to the user that `sitemap-xml-gen` skill creates `robots.txt`.

### 6. Suggest Next.js Route

Optionally suggest the user add `app/llms.txt/route.ts` as a dynamic route if they want to generate the file from live data rather than a static file:
```ts
export async function GET() {
  // fetch live page list, generate content dynamically
  const text = '...'
  return new Response(text, { headers: { 'Content-Type': 'text/plain' } })
}
```

## Output

- `public/llms.txt` — primary AI crawler guidance file
- `public/llms-full.txt` — expanded content for deep crawlers
- `public/robots.txt` addendum (if file exists)

## Error Handling

- No source material found → generate minimal template with `<PLACEHOLDER>` markers and list what the user needs to fill in
- Brand guide not found → omit brand voice section; leave placeholder comment
- Sitemap not found → list pages manually based on user input or `app/` directory scan
