---
name: sanity-preview-routes
description: "Add Sanity live preview routes to Next.js app"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /sanity-preview-routes
metadata:
  openclaw:
    emoji: "👁️"
    requires:
      bins: ["node"]
---

## Overview

Adds Sanity live preview support to an existing Next.js App Router project. Creates draft-mode enable/disable API routes, wraps page components with `draftMode()`, and configures GROQ live queries for real-time content updates in the Studio preview pane.

## Steps

### 1. Create Draft Enable Route

Write `app/api/draft/enable/route.ts`:

```ts
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const secret = searchParams.get('secret')
  const slug = searchParams.get('slug') ?? '/'

  if (secret !== process.env.SANITY_PREVIEW_SECRET) {
    return new Response('Invalid secret', { status: 401 })
  }

  const dm = await draftMode()
  dm.enable()
  redirect(slug)
}
```

### 2. Create Draft Disable Route

Write `app/api/draft/disable/route.ts`:

```ts
import { draftMode } from 'next/headers'
import { redirect } from 'next/navigation'

export async function GET() {
  const dm = await draftMode()
  dm.disable()
  redirect('/')
}
```

### 3. Create Sanity Client Helpers

Write `lib/sanity/client.ts` (skip if already exists):

```ts
import { createClient } from 'next-sanity'

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET ?? 'production',
  apiVersion: '2024-01-01',
  useCdn: true,
})

export const previewClient = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET ?? 'production',
  apiVersion: '2024-01-01',
  useCdn: false,
  token: process.env.SANITY_API_READ_TOKEN,
  perspective: 'previewDrafts',
})
```

Write `lib/sanity/fetch.ts`:
```ts
import { client, previewClient } from './client'
import { draftMode } from 'next/headers'

export async function sanityFetch<T>({ query, params = {} }: { query: string; params?: Record<string, unknown> }): Promise<T> {
  const dm = await draftMode()
  const c = dm.isEnabled ? previewClient : client
  return c.fetch<T>(query, params)
}
```

### 4. Inject `draftMode()` Into Page Components

Scan `app/` for page files that fetch Sanity content (look for GROQ query patterns or `client.fetch` calls). For each found page:
- Import `sanityFetch` from `lib/sanity/fetch` (replace direct `client.fetch` calls)
- Add a banner shown only in draft mode:
  ```tsx
  const dm = await draftMode()
  // Near top of JSX:
  {dm.isEnabled && (
    <div style={{ background: '#f59e0b', padding: '8px', textAlign: 'center', fontSize: 14 }}>
      Preview mode active — <a href="/api/draft/disable">Exit preview</a>
    </div>
  )}
  ```

### 5. Add Preview URL to Sanity Studio Config

Append preview URL configuration to `sanity.config.ts` (if it exists):
```ts
preview: {
  select: { title: 'title', slug: 'slug.current' },
  prepare: ({ title, slug }) => ({
    title,
    media: () => null,
    subtitle: `/${slug}`,
  }),
},
```
Add preview panel URL: `${process.env.NEXT_PUBLIC_SITE_URL}/api/draft/enable?secret=${process.env.SANITY_PREVIEW_SECRET}&slug=/{slug}`

### 6. Update `.env.local`

Append the following env var placeholders (do not overwrite existing keys):
```
SANITY_PREVIEW_SECRET=<generate a random 32-char string>
SANITY_API_READ_TOKEN=<viewer token from sanity.io/manage>
NEXT_PUBLIC_SANITY_PROJECT_ID=<your project ID>
NEXT_PUBLIC_SANITY_DATASET=production
```

List the npm install command: `npm install next-sanity`

## Output

- `app/api/draft/enable/route.ts`
- `app/api/draft/disable/route.ts`
- `lib/sanity/client.ts`
- `lib/sanity/fetch.ts`
- Modified page components (draft mode banner + `sanityFetch` usage)
- `.env.local` additions

## Error Handling

- `SANITY_PREVIEW_SECRET` missing at runtime → enable route returns 401; remind user to set env var
- Page components not found → report which pages were skipped; do not create placeholder pages
- `lib/sanity/client.ts` already exists → skip creation, only create `fetch.ts`
