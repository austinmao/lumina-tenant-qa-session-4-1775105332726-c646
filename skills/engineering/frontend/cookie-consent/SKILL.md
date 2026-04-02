---
name: cookie-consent
description: "Add a GDPR cookie consent banner to a Next.js site with analytics opt-in"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /cookie-consent
metadata:
  openclaw:
    emoji: "🍪"
    requires:
      bins: ["node"]
---

## Overview

Creates a GDPR-compliant cookie consent banner for a Next.js App Router site. Includes Accept All / Reject Non-Essential / Preferences modal buttons, localStorage consent persistence, conditional GA4 loading after consent, a cookie policy page, and a server-side consent check via cookie header.

## Steps

### 1. Generate Consent Utilities

Write `lib/consent/index.ts`:

```ts
export type ConsentLevel = 'all' | 'essential' | 'none'

const CONSENT_STORAGE = 'cookie-consent'
const CONSENT_COOKIE = 'cookie-consent'

export function getConsentLevel(): ConsentLevel | null {
  if (typeof window === 'undefined') return null
  return (localStorage.getItem(CONSENT_STORAGE) as ConsentLevel) ?? null
}

export function setConsentLevel(level: ConsentLevel): void {
  localStorage.setItem(CONSENT_STORAGE, level)
  // Mirror to cookie for server-side reads (1 year expiry)
  document.cookie = `${CONSENT_COOKIE}=${level}; max-age=${60 * 60 * 24 * 365}; path=/; SameSite=Lax`
  window.dispatchEvent(new CustomEvent('consent-updated', { detail: { level } }))
}

export function hasConsented(): boolean {
  return getConsentLevel() !== null
}
```

### 2. Generate CookieConsent Banner Component

Write `components/CookieConsent.tsx`:

```tsx
'use client'

import { useState, useEffect } from 'react'
import { getConsentLevel, setConsentLevel, hasConsented, ConsentLevel } from '@/lib/consent'

export function CookieConsent() {
  const [visible, setVisible] = useState(false)
  const [showPreferences, setShowPreferences] = useState(false)
  const [analyticsEnabled, setAnalyticsEnabled] = useState(true)

  useEffect(() => {
    if (!hasConsented()) setVisible(true)
  }, [])

  const accept = (level: ConsentLevel) => {
    setConsentLevel(level)
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div
      role="dialog"
      aria-label="Cookie consent"
      aria-modal="false"
      style={{
        position: 'fixed', bottom: 0, left: 0, right: 0,
        background: '#1e293b', color: '#f8fafc',
        padding: '1.5rem', zIndex: 9999,
        display: 'flex', flexWrap: 'wrap', gap: '0.75rem', alignItems: 'center',
        borderTop: '1px solid #334155',
      }}
    >
      <p style={{ flex: '1 1 300px', margin: 0, fontSize: 14 }}>
        We use cookies to improve your experience and analyse site usage.
        See our <a href="/privacy" style={{ color: '#94a3b8' }}>Privacy Policy</a> and{' '}
        <a href="/cookies" style={{ color: '#94a3b8' }}>Cookie Policy</a>.
      </p>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button onClick={() => accept('essential')} style={btnSecondary}>Reject non-essential</button>
        <button onClick={() => setShowPreferences(true)} style={btnSecondary}>Preferences</button>
        <button onClick={() => accept('all')} style={btnPrimary}>Accept all</button>
      </div>

      {showPreferences && (
        <div role="dialog" aria-label="Cookie preferences" style={modal}>
          <h2 style={{ marginTop: 0 }}>Cookie Preferences</h2>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
            <input type="checkbox" checked disabled readOnly />
            Essential cookies (always on — required for site to function)
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <input
              type="checkbox"
              checked={analyticsEnabled}
              onChange={e => setAnalyticsEnabled(e.target.checked)}
            />
            Analytics cookies (GA4 — helps us understand site usage)
          </label>
          <div style={{ marginTop: 16, display: 'flex', gap: 8 }}>
            <button onClick={() => { accept(analyticsEnabled ? 'all' : 'essential'); setShowPreferences(false) }} style={btnPrimary}>
              Save preferences
            </button>
            <button onClick={() => setShowPreferences(false)} style={btnSecondary}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  )
}

const btnPrimary = { background: '#3b82f6', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: 4, cursor: 'pointer', fontSize: 14 }
const btnSecondary = { background: 'transparent', color: '#94a3b8', border: '1px solid #475569', padding: '0.5rem 1rem', borderRadius: 4, cursor: 'pointer', fontSize: 14 }
const modal = { position: 'fixed' as const, top: '50%', left: '50%', transform: 'translate(-50%, -50%)', background: '#1e293b', border: '1px solid #334155', borderRadius: 8, padding: '2rem', zIndex: 10000, minWidth: 320, maxWidth: 480 }
```

### 3. Generate Conditional Analytics Loader

Write `components/ConsentAwareAnalytics.tsx`:

```tsx
'use client'

import { useEffect, useState } from 'react'
import { GoogleAnalytics } from '@next/third-parties/google'
import { getConsentLevel } from '@/lib/consent'

export function ConsentAwareAnalytics() {
  const [analyticsAllowed, setAnalyticsAllowed] = useState(false)

  useEffect(() => {
    const check = () => setAnalyticsAllowed(getConsentLevel() === 'all')
    check()
    window.addEventListener('consent-updated', check)
    return () => window.removeEventListener('consent-updated', check)
  }, [])

  if (!analyticsAllowed || !process.env.NEXT_PUBLIC_GA4_ID) return null
  return <GoogleAnalytics gaId={process.env.NEXT_PUBLIC_GA4_ID} />
}
```

### 4. Update Root Layout

In `app/layout.tsx`, add inside `<body>`:
```tsx
import { CookieConsent } from '@/components/CookieConsent'
import { ConsentAwareAnalytics } from '@/components/ConsentAwareAnalytics'

// At the bottom of <body>:
<CookieConsent />
<ConsentAwareAnalytics />
```

Remove any existing unconditional `<GoogleAnalytics>` call.

### 5. Create Cookie Policy Page

Write `app/cookies/page.tsx` with a minimal policy covering: essential cookies (session, CSRF), analytics cookies (GA4, 2-year expiry), how to manage cookies per browser. Link back to the privacy policy.

### 6. Server-Side Consent Check Helper

Write `lib/consent/server.ts`:

```ts
import { cookies } from 'next/headers'

export async function getServerConsentLevel(): Promise<string | null> {
  const cookieStore = await cookies()
  return cookieStore.get('cookie-consent')?.value ?? null
}
```

Use this in server components or API routes that should behave differently based on consent (e.g., skip logging personal data for users who have not consented).

## Output

- `lib/consent/index.ts` — consent utilities (client)
- `lib/consent/server.ts` — consent utilities (server)
- `components/CookieConsent.tsx` — GDPR banner component
- `components/ConsentAwareAnalytics.tsx` — conditional GA4 loader
- Updated `app/layout.tsx` — banner and analytics integration
- `app/cookies/page.tsx` — cookie policy page

## Error Handling

- `localStorage` unavailable (SSR or privacy mode) → `hasConsented()` returns `null`; banner shows on next client render
- `@next/third-parties` not installed → print `npm install @next/third-parties` and stop; do not fall back to raw script tag
- `NEXT_PUBLIC_GA4_ID` not set → `ConsentAwareAnalytics` renders nothing; log a dev-mode warning
