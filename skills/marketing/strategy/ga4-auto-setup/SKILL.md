---
name: ga4-auto-setup
description: "Set up GA4 measurement with automatic event taxonomy for Next.js sites"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /ga4-auto-setup
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["node"]
      env: ["NEXT_PUBLIC_GA4_ID"]
---

## Overview

Installs GA4 tracking into a Next.js App Router site via `@next/third-parties`, creates a `useAnalytics()` hook for custom events, sets up standard event taxonomy (page_view, form_submit, button_click, scroll_depth, external_link_click), and documents the event taxonomy in `memory/site-analytics.yaml`.

## Steps

### 1. Install Script in Layout

Update `app/layout.tsx` to load GA4 via `@next/third-parties` (preferred over raw gtag — handles consent and SSR correctly):

```tsx
import { GoogleAnalytics } from '@next/third-parties/google'

// Inside the <html> body, at the bottom:
<GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA4_ID!} />
```

If `@next/third-parties` is not installed, print: `npm install @next/third-parties` and use it. Do not fall back to a raw `<script>` tag unless the user explicitly requests it.

### 2. Create `useAnalytics` Hook

Write `lib/analytics/useAnalytics.ts`:

```ts
'use client'

type EventName =
  | 'page_view'
  | 'form_submit'
  | 'button_click'
  | 'scroll_depth'
  | 'external_link_click'
  | 'cta_click'
  | string

interface EventParams {
  event_category?: string
  event_label?: string
  value?: number
  page_type?: string
  site_name?: string
  user_type?: string
  [key: string]: string | number | boolean | undefined
}

export function useAnalytics() {
  const track = (eventName: EventName, params: EventParams = {}) => {
    if (typeof window === 'undefined' || !window.gtag) return
    window.gtag('event', eventName, {
      site_name: process.env.NEXT_PUBLIC_SITE_NAME,
      ...params,
    })
  }

  return { track }
}
```

Add `declare global { interface Window { gtag: (...args: unknown[]) => void } }` to the file footer.

### 3. Set Up Automatic Event Capture

Write `components/AnalyticsProvider.tsx` as a client component that wraps the app and captures standard events:

```tsx
'use client'

import { useEffect, useRef } from 'react'
import { usePathname } from 'next/navigation'

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const scrollDepthFired = useRef<Set<number>>(new Set())

  // Page view on route change
  useEffect(() => {
    if (typeof window === 'undefined' || !window.gtag) return
    window.gtag('event', 'page_view', { page_path: pathname, site_name: process.env.NEXT_PUBLIC_SITE_NAME })
    scrollDepthFired.current = new Set()
  }, [pathname])

  // Scroll depth: fire at 25%, 50%, 75%, 90%
  useEffect(() => {
    const thresholds = [25, 50, 75, 90]
    const handler = () => {
      const scrolled = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
      thresholds.forEach(t => {
        if (scrolled >= t && !scrollDepthFired.current.has(t)) {
          scrollDepthFired.current.add(t)
          window.gtag?.('event', 'scroll_depth', { depth_percent: t, page_path: pathname })
        }
      })
    }
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [pathname])

  // External link click tracking via event delegation
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      const target = (e.target as HTMLElement).closest('a')
      if (!target) return
      const href = target.getAttribute('href') ?? ''
      if (href.startsWith('http') && !href.includes(window.location.hostname)) {
        window.gtag?.('event', 'external_link_click', { link_url: href, page_path: pathname })
      }
    }
    document.addEventListener('click', handler)
    return () => document.removeEventListener('click', handler)
  }, [pathname])

  return <>{children}</>
}
```

Add `<AnalyticsProvider>` wrapper inside the root layout's `<body>`.

### 4. Create GA4 Custom Dimensions

Print instructions for the user to add in GA4 Admin → Custom Definitions → Custom Dimensions:

| Parameter name | Scope | Display name |
|---|---|---|
| `site_name` | Event | Site Name |
| `page_type` | Event | Page Type |
| `user_type` | Event | User Type |

These must be created manually in the GA4 property — they cannot be set via code alone.

### 5. Document Event Taxonomy

Write `memory/site-analytics.yaml`:

```yaml
ga4_property: "G-XXXXXXXXXX"  # replace with NEXT_PUBLIC_GA4_ID value
last_updated: "<today's date>"

custom_dimensions:
  - name: site_name
    scope: event
  - name: page_type
    scope: event
  - name: user_type
    scope: event

events:
  - name: page_view
    trigger: route change via AnalyticsProvider
    params: [page_path, site_name]
  - name: form_submit
    trigger: manual — call track('form_submit', { event_label: 'retreat-application' })
    params: [event_label, event_category]
  - name: button_click
    trigger: manual — call track('button_click', { event_label: 'hero-cta' })
    params: [event_label, page_path]
  - name: scroll_depth
    trigger: automatic — AnalyticsProvider at 25/50/75/90%
    params: [depth_percent, page_path]
  - name: external_link_click
    trigger: automatic — AnalyticsProvider via click delegation
    params: [link_url, page_path]
```

### 6. `.env.local` Check

If `NEXT_PUBLIC_GA4_ID` is not set in `.env.local`, append placeholder:
```
NEXT_PUBLIC_GA4_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SITE_NAME=Your Site
```

## Output

- Updated `app/layout.tsx` — GA4 script and AnalyticsProvider
- `lib/analytics/useAnalytics.ts` — typed analytics hook
- `components/AnalyticsProvider.tsx` — automatic event capture
- `memory/site-analytics.yaml` — event taxonomy documentation
- `.env.local` additions

## Error Handling

- `NEXT_PUBLIC_GA4_ID` missing at runtime → GA4 script still loads but fires to no property; add a startup check that warns in development
- `window.gtag` undefined → all track calls are no-ops; never throw
- AnalyticsProvider not added to layout → log a reminder after generating the files
