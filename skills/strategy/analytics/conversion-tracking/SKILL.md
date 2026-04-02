---
name: conversion-tracking
description: "Set up cross-platform conversion pixels, event configuration, and conversion funnels"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /conversion-tracking
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["node"]
      env: ["GA_MEASUREMENT_ID"]
      os: ["darwin"]
---

# Conversion Tracking

Set up cross-platform conversion pixels, configure conversion events, and build conversion funnels across Google Analytics 4, Meta Pixel, Google Ads, and custom tracking. This skill ensures every meaningful user action is measured accurately, attributed correctly, and reported consistently.

## When to Use

- Setting up conversion tracking for a new tenant website
- Adding conversion pixels for a new advertising platform (Meta, Google Ads)
- Configuring custom conversion events for specific user actions
- Building conversion funnels to measure drop-off between steps
- Debugging tracking issues (missing events, duplicate events, wrong values)
- Auditing existing tracking for completeness and accuracy

## Context Loading

Before any tracking setup:
1. Read `tenants/<tenant>/config.yaml` for tracking IDs (GA4 measurement ID, Meta Pixel ID)
2. Read `<brand_root>/brand-guide.md` for conversion goals and KPIs
3. Read the event taxonomy document (`docs/tracking/event-taxonomy.yaml` or equivalent)
4. Read existing tracking implementation in `web/src/lib/analytics/`
5. Verify `$GA_MEASUREMENT_ID` is set

## Tracking Architecture

### Data Layer Pattern

All tracking flows through a centralized data layer, not direct platform calls.

```
User Action → Data Layer Event → Platform Adapters → GA4 / Meta / Google Ads
```

The data layer provides:
- Single source of truth for event data
- Platform-agnostic event definitions
- Easy addition of new tracking platforms without changing application code
- Consistent event naming across all platforms

### Implementation

```typescript
// web/src/lib/analytics/data-layer.ts
type TrackingEvent = {
  event: string
  category: string
  action: string
  label?: string
  value?: number
  custom?: Record<string, string | number | boolean>
}

function trackEvent(event: TrackingEvent) {
  // Push to data layer
  window.dataLayer?.push(event)

  // Notify all registered adapters
  adapters.forEach(adapter => adapter.track(event))
}
```

### Platform Adapters

Each tracking platform gets its own adapter:

```typescript
// GA4 Adapter
function ga4Track(event: TrackingEvent) {
  window.gtag?.('event', event.action, {
    event_category: event.category,
    event_label: event.label,
    value: event.value,
    ...event.custom,
  })
}

// Meta Pixel Adapter
function metaTrack(event: TrackingEvent) {
  const metaEventName = mapToMetaEvent(event.action)
  if (metaEventName) {
    window.fbq?.('track', metaEventName, {
      content_name: event.label,
      value: event.value,
      currency: 'USD',
    })
  }
}
```

## Pixel Installation

### Google Analytics 4

Install via Google Tag Manager (recommended) or directly:

```typescript
// Direct installation (Next.js App Router)
// web/src/app/layout.tsx
import Script from 'next/script'

<Script
  src={`https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`}
  strategy="afterInteractive"
/>
<Script id="gtag-init" strategy="afterInteractive">
  {`
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '${GA_MEASUREMENT_ID}', {
      send_page_view: true,
      cookie_flags: 'SameSite=None;Secure',
    });
  `}
</Script>
```

### Meta Pixel

```typescript
// Meta Pixel installation
<Script id="meta-pixel" strategy="afterInteractive">
  {`
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '${META_PIXEL_ID}');
    fbq('track', 'PageView');
  `}
</Script>
```

### Google Ads

```typescript
// Google Ads conversion tracking
gtag('config', GOOGLE_ADS_ID)

// On conversion event
gtag('event', 'conversion', {
  send_to: `${GOOGLE_ADS_ID}/${CONVERSION_LABEL}`,
  value: conversionValue,
  currency: 'USD',
})
```

## Conversion Events

### Standard Events

Define conversions for the core funnel:

| Funnel Stage | Event Name | GA4 Event | Meta Event | Trigger |
|---|---|---|---|---|
| Page View | `page_view` | `page_view` (auto) | `PageView` (auto) | Page load |
| Content View | `view_content` | `view_item` | `ViewContent` | Key page viewed |
| Lead Capture | `lead_captured` | `generate_lead` | `Lead` | Form submission |
| Booking Started | `booking_started` | `begin_checkout` | `InitiateCheckout` | Calendly opened |
| Booking Completed | `booking_completed` | `purchase` | `Schedule` | Booking confirmed |
| Application Submitted | `application_submitted` | `generate_lead` | `CompleteRegistration` | Application form |

### Custom Events

For business-specific actions not covered by standard events:

```typescript
trackEvent({
  event: 'custom_event',
  category: 'engagement',
  action: 'video_watched',
  label: 'retreat-overview-video',
  value: 1,
  custom: {
    video_duration: 180,
    video_completion: 75,
  },
})
```

### Event Parameters

Every event should include:
- `page_location`: the URL where the event occurred
- `page_title`: the page title
- `tenant_id`: the tenant identifier (for multi-tenant reporting)
- `user_type`: anonymous, lead, customer, alumni (if known)

Do not include PII (names, emails, phone numbers) in event parameters. Use hashed identifiers if cross-device tracking is needed.

## Conversion Funnel Configuration

### GA4 Funnel Exploration

Configure funnels in GA4 Explorations:
1. Define funnel steps (ordered sequence of events)
2. Set open or closed funnel (can users enter mid-funnel?)
3. Add segments for comparison (mobile vs desktop, new vs returning)
4. Configure time constraints (how long between steps?)

### Funnel Monitoring

Set up automated alerts for:
- Conversion rate drops > 20% from baseline (indicates tracking breakage or UX issue)
- Funnel step with > 80% drop-off (indicates friction point)
- Zero conversions for 24+ hours (indicates tracking failure)

## Consent Management

### Cookie Consent

Before firing any tracking pixels:
1. Check if the user has consented to analytics cookies
2. If no consent: load only essential cookies (no tracking pixels)
3. If consent granted: initialize tracking pixels and fire buffered events
4. If consent withdrawn: clear tracking cookies and stop firing events

### Implementation Pattern

```typescript
function initializeTracking(consent: ConsentState) {
  if (consent.analytics) {
    initGA4()
    initMetaPixel()
    // Fire any buffered events from before consent was granted
    flushEventBuffer()
  }

  if (consent.marketing) {
    initGoogleAds()
    // Enable remarketing audiences
  }
}
```

### Privacy Compliance

- GDPR (EU): explicit opt-in required before any tracking
- CCPA (California): opt-out model (track by default, honor "Do Not Sell" requests)
- Document the consent categories and which pixels fall under each
- Log consent events for audit: `consent_granted`, `consent_withdrawn`

## Debugging and Validation

### Pre-Launch Checklist

Before deploying tracking to production:
- [ ] All pixels fire on page load (verify in browser dev tools Network tab)
- [ ] Custom events fire on the correct user actions (verify in real-time reports)
- [ ] Event parameters contain expected values (no undefined, no PII)
- [ ] Conversion values are correct (currency, amount)
- [ ] Consent management blocks pixels when consent is not given
- [ ] No duplicate events (one event per action, not multiple)
- [ ] Funnel steps fire in the correct order
- [ ] Cross-domain tracking works (if multiple domains)

### Debugging Tools

| Tool | Purpose |
|---|---|
| GA4 DebugView | Real-time event validation |
| Meta Pixel Helper (browser extension) | Verify Meta Pixel events |
| Google Tag Assistant | Validate Google tag implementation |
| Browser Network tab | Inspect all tracking requests |
| GTM Preview Mode | Debug Tag Manager triggers |

### Common Issues

- **Events not appearing**: check that the pixel is initialized, consent is granted, and the event name matches the GA4/Meta expected format
- **Duplicate events**: check for multiple pixel installations (e.g., direct + GTM), React strict mode in development (double-fires)
- **Wrong conversion values**: verify currency code, value field type (number not string), decimal precision
- **Cross-domain tracking breaks**: verify linked domains in GA4 settings, check referral exclusion list

## Error Handling

- Pixel fails to load (ad blocker): degrade gracefully. Never break the user experience because tracking failed. Use `try-catch` around all tracking calls.
- Consent service unavailable: default to no tracking (fail-closed for privacy)
- Event buffer overflow: cap the buffer at 50 events. If consent is never granted in the session, discard the buffer.

## Boundaries

- Never include PII (names, emails, phone numbers) in tracking events
- Never fire tracking pixels without user consent (GDPR/CCPA compliance)
- Never modify tracking configuration in production without testing in staging first
- Never use tracking data to identify individual users without their knowledge

## Dependencies

- `event-taxonomy` -- event naming conventions that this skill implements
- `attribution-modeling` -- attribution logic that consumes conversion data
- `analytics-tracking` -- GA4 setup and configuration
- `gtm-implementation` -- Tag Manager configuration for pixel management

## State Tracking

- `pixels` -- keyed by platform: pixel ID, installation method, consent category, status
- `events` -- keyed by event name: platforms fired, parameters, validation status
- `funnels` -- keyed by funnel name: steps, baseline conversion rate, alert thresholds
