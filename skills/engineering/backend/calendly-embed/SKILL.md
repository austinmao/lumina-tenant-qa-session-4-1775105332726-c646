---
name: calendly-embed
description: "Embed Calendly scheduling widget in a Next.js page component"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /calendly-embed
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins: ["node"]
---

## Overview

Creates a `CalendlyWidget` React component that embeds the Calendly inline scheduling widget in a Next.js page. Accepts `eventUrl`, `prefillName`, and `prefillEmail` props, handles the `event_scheduled` callback for post-booking logic, and adds UTM source tracking. Fully typed with TypeScript.

## Steps

### 1. Gather Requirements

Ask the user for:
- Calendly event URL (e.g., `https://calendly.com/yourname/30min`)
- Whether to show UTM tracking params
- Post-booking action: redirect to a URL, show a message, or fire a custom callback
- Any prefill fields known at render time (name, email from context or query params)

### 2. Generate TypeScript Types

Write `types/calendly.ts`:

```ts
export interface CalendlyEventPayload {
  event: 'calendly.event_scheduled'
  payload: {
    event: { uri: string }
    invitee: { uri: string; email: string; name: string }
  }
}

export interface CalendlyWidgetProps {
  eventUrl: string
  prefillName?: string
  prefillEmail?: string
  utmSource?: string
  utmMedium?: string
  utmCampaign?: string
  onEventScheduled?: (payload: CalendlyEventPayload['payload']) => void
  height?: number
}
```

### 3. Generate CalendlyWidget Component

Write `components/CalendlyWidget.tsx`:

```tsx
'use client'

import { useEffect, useRef } from 'react'
import Script from 'next/script'
import { CalendlyEventPayload, CalendlyWidgetProps } from '@/types/calendly'

export function CalendlyWidget({
  eventUrl,
  prefillName,
  prefillEmail,
  utmSource,
  utmMedium,
  utmCampaign,
  onEventScheduled,
  height = 700,
}: CalendlyWidgetProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  const buildUrl = () => {
    const url = new URL(eventUrl)
    if (prefillName) url.searchParams.set('name', prefillName)
    if (prefillEmail) url.searchParams.set('email', prefillEmail)
    if (utmSource) url.searchParams.set('utm_source', utmSource)
    if (utmMedium) url.searchParams.set('utm_medium', utmMedium)
    if (utmCampaign) url.searchParams.set('utm_campaign', utmCampaign)
    return url.toString()
  }

  useEffect(() => {
    const handler = (e: MessageEvent) => {
      if (e.origin !== 'https://calendly.com') return
      try {
        const data: CalendlyEventPayload = typeof e.data === 'string' ? JSON.parse(e.data) : e.data
        if (data.event === 'calendly.event_scheduled' && onEventScheduled) {
          onEventScheduled(data.payload)
        }
      } catch {
        // ignore non-Calendly messages
      }
    }
    window.addEventListener('message', handler)
    return () => window.removeEventListener('message', handler)
  }, [onEventScheduled])

  return (
    <>
      <Script src="https://assets.calendly.com/assets/external/widget.js" strategy="lazyOnload" />
      <div
        ref={containerRef}
        className="calendly-inline-widget"
        data-url={buildUrl()}
        style={{ minWidth: 320, height }}
      />
    </>
  )
}
```

### 4. Generate Example Usage

Write `app/book/page.tsx` as an example integration:

```tsx
import { CalendlyWidget } from '@/components/CalendlyWidget'

export default function BookPage() {
  return (
    <main>
      <h1>Book a Call</h1>
      <CalendlyWidget
        eventUrl="https://calendly.com/your-username/30min"
        utmSource="website"
        utmMedium="hero-cta"
        onEventScheduled={(payload) => {
          console.log('Meeting booked with', payload.invitee.email)
          // TODO: fire GA4 event, update CRM, redirect
        }}
      />
    </main>
  )
}
```

Replace `your-username/30min` with the actual event URL from the user.

### 5. Notes on `onEventScheduled` Callback

The `onEventScheduled` callback fires client-side via `postMessage`. Common follow-up actions:
- Fire a GA4 `generate_lead` event using `window.gtag`
- Redirect: `router.push('/booking-confirmed')`
- Update CRM: POST to an internal API route with invitee data

Add a comment block in the generated code listing these options.

## Output

- `types/calendly.ts` — TypeScript interfaces
- `components/CalendlyWidget.tsx` — reusable embed component
- `app/book/page.tsx` — example usage page

## Error Handling

- Invalid `eventUrl` format → log a console warning; still render the widget (Calendly will show its own error)
- `onEventScheduled` throws → catch in the message handler and log; do not crash the component
- Calendly script fails to load → widget container remains empty; no fallback required (Calendly's CDN is highly reliable)
