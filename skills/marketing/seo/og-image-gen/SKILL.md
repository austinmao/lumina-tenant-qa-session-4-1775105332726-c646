---
name: og-image-gen
description: "Generate Open Graph images for pages using Next.js ImageResponse"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /og-image-gen
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: ["node"]
---

## Overview

Creates a Next.js `app/og/route.tsx` that generates branded Open Graph images (1200×630px) using `ImageResponse` from `@vercel/og`. Reads brand colors and typography from `brands/<tenant>/tokens/design-system.yaml`. Adds `og:image` meta tags to `app/layout.tsx`.

## Steps

### 1. Read Brand Tokens

Read `brands/<tenant>/tokens/design-system.yaml` (or `docs/brand/brand-ref.yaml` as fallback) to extract:
- `primary` color (hex) — background or accent
- `surface` / `background` color — card background
- `text` color — body and heading text
- `fontFamily.heading` — heading font name (use Google Fonts URL for ImageResponse)
- `fontFamily.body` — body font name

If no brand file is found, use safe defaults: background `#0f172a`, text `#ffffff`, accent `#6366f1`.

Ask the user which tenant/brand to use if multiple exist under `brands/`.

### 2. Generate OG Image Route

Write `app/og/route.tsx`:

```tsx
import { ImageResponse } from 'next/og'
import { NextRequest } from 'next/server'

export const runtime = 'edge'

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const title = searchParams.get('title') ?? 'Welcome'
  const description = searchParams.get('description') ?? ''
  const type = searchParams.get('type') ?? 'page' // page | post | event

  // Load brand font (replace with actual font URL from brand tokens)
  // const fontData = await fetch(new URL('/fonts/brand-heading.woff', request.url)).then(r => r.arrayBuffer())

  return new ImageResponse(
    (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end',
          width: '100%',
          height: '100%',
          background: '<PRIMARY_BG_COLOR>',
          padding: 60,
          fontFamily: 'sans-serif',
        }}
      >
        {type !== 'page' && (
          <div style={{ fontSize: 20, color: '<ACCENT_COLOR>', marginBottom: 16, textTransform: 'uppercase', letterSpacing: 2 }}>
            {type}
          </div>
        )}
        <div style={{ fontSize: 64, fontWeight: 700, color: '<TEXT_COLOR>', lineHeight: 1.1, maxWidth: 900 }}>
          {title}
        </div>
        {description && (
          <div style={{ fontSize: 28, color: '<MUTED_TEXT_COLOR>', marginTop: 24, maxWidth: 800 }}>
            {description}
          </div>
        )}
        <div style={{ position: 'absolute', top: 60, right: 60, display: 'flex', alignItems: 'center', gap: 12 }}>
          {/* Brand logo — replace with actual logo or site name */}
          <div style={{ fontSize: 22, color: '<TEXT_COLOR>', fontWeight: 600 }}>
            {process.env.NEXT_PUBLIC_SITE_NAME ?? 'Your Site'}
          </div>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  )
}
```

Replace color placeholders with actual hex values from brand tokens. Add a comment block listing all substituted values for traceability.

### 3. Add `og:image` to Layout

Update `app/layout.tsx` to add `openGraph` metadata. If a `metadata` export already exists, merge into it:

```ts
export const metadata: Metadata = {
  // ... existing metadata ...
  openGraph: {
    images: [
      {
        url: '/og?title=Your+Site+Name',
        width: 1200,
        height: 630,
        alt: 'Your Site Name',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    images: ['/og?title=Your+Site+Name'],
  },
}
```

### 4. Add Per-Page OG Image

For blog post or event pages (if `app/blog/[slug]/page.tsx` or similar exists), add dynamic metadata:

```ts
export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const post = await getPost(params.slug) // replace with actual fetch
  return {
    openGraph: {
      images: [`/og?title=${encodeURIComponent(post.title)}&type=post&description=${encodeURIComponent(post.excerpt ?? '')}`],
    },
  }
}
```

Add this boilerplate to each dynamic page found in `app/`. Leave `getPost` as a placeholder if the data fetching function name is unknown.

### 5. List npm Dependencies

Print: `npm install @vercel/og` (bundled with Next.js 13.3+ — usually not needed separately).

## Output

- `app/og/route.tsx` — edge-rendered OG image generator
- Updated `app/layout.tsx` — default OG image meta tags
- Updated dynamic page files — per-page OG image metadata

## Error Handling

- Brand tokens not found → use default dark theme colors; add comment noting the placeholder
- `app/layout.tsx` has no existing metadata export → create a new one; do not merge into page-level components
- Font file missing → skip custom font loading; use system `sans-serif` (ImageResponse default)
