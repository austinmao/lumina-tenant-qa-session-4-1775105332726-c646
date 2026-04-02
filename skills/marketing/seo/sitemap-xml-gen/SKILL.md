---
name: sitemap-xml-gen
description: "Generate sitemap.xml and robots.txt for a Next.js site"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /sitemap-xml-gen
metadata:
  openclaw:
    emoji: "🗺️"
    requires:
      bins: ["node"]
---

## Overview

Generates a complete `sitemap.xml` (or Next.js `app/sitemap.ts`) and a `robots.txt` for a Next.js App Router site. Assigns priority weights and lastmod dates per page type. Disallows admin and API routes from crawlers.

## Steps

### 1. Discover Routes

Scan the `app/` directory for all public page files (`page.tsx`, `page.ts`, `page.js`, `page.mdx`). Exclude:
- `app/api/**` — API routes
- `app/(admin)/**` or `app/admin/**` — admin panels
- `app/_*/**` — private route groups
- Files where the route segment is wrapped in `()` (route groups) — include their children, not the group itself

Build a route list. For each route, determine the URL path by stripping `app/`, removing `page.tsx`, and converting `[slug]` to `:slug` notation (mark as dynamic).

### 2. Assign Priority Weights

Apply these priority rules:

| Route pattern | Priority | Change frequency |
|---|---|---|
| `/` (homepage) | 1.0 | daily |
| `/about`, `/services`, `/programs`, `/retreats` | 0.8 | weekly |
| `/blog`, `/posts` (index) | 0.8 | daily |
| `/blog/[slug]`, `/posts/[slug]` (individual) | 0.6 | monthly |
| `/faq`, `/pricing`, `/contact` | 0.7 | monthly |
| Everything else | 0.4 | monthly |

Dynamic routes (`[slug]`) need a data source to enumerate URLs. Add a comment `// TODO: replace with dynamic URL list from CMS or filesystem` for each dynamic route.

### 3. Generate Next.js `app/sitemap.ts`

Write `app/sitemap.ts` using the Next.js Metadata API (preferred over a static XML file):

```ts
import { MetadataRoute } from 'next'

const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://example.com'

export default function sitemap(): MetadataRoute.Sitemap {
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: siteUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${siteUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    // ... additional static routes
  ]

  // TODO: fetch dynamic routes from CMS and add here
  // const posts = await client.fetch('*[_type == "post"]{ slug, _updatedAt }')
  // const postRoutes = posts.map(post => ({ url: `${siteUrl}/blog/${post.slug.current}`, ... }))

  return [...staticRoutes]
}
```

Include all discovered static routes. Add commented-out boilerplate for each dynamic route type found.

### 4. Generate `robots.txt`

Write `public/robots.txt`:

```
User-agent: *
Crawl-delay: 10
Disallow: /api/
Disallow: /admin/
Disallow: /_next/
Disallow: /api/draft/
Allow: /

Sitemap: <NEXT_PUBLIC_SITE_URL>/sitemap.xml
```

Replace `<NEXT_PUBLIC_SITE_URL>` with the literal placeholder — the user should update this with their actual domain.

If a `public/robots.txt` already exists, print the additions to the console rather than overwriting.

### 5. Verify NEXT_PUBLIC_SITE_URL

Check if `NEXT_PUBLIC_SITE_URL` is set in `.env.local`. If not, append the placeholder:
```
NEXT_PUBLIC_SITE_URL=https://your-domain.com
```
Print a reminder to set this before deploying.

## Output

- `app/sitemap.ts` — Next.js dynamic sitemap (replaces static XML)
- `public/robots.txt` — crawler directives
- `.env.local` addition for `NEXT_PUBLIC_SITE_URL` if missing

## Error Handling

- `app/` directory not found → ask for project root path; do not generate empty sitemap
- No page files found → generate minimal sitemap with homepage only and list what was searched
- `robots.txt` already exists → print additions to console; do not overwrite
