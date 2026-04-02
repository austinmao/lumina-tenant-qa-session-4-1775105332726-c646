---
name: api-client-integration
description: "Integrate client-side code with Attio, Calendly, or Composio APIs"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /api-client-integration
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: ["node"]
      env: []
      os: ["darwin"]
---

# API Client Integration

Build client-side integrations with Attio (CRM), Calendly (scheduling), and Composio (OAuth) APIs. This skill produces the frontend code that connects UI components to backend API routes that proxy these services. Client-side code never calls third-party APIs directly -- it calls internal API routes that handle authentication and proxying.

## When to Use

- Connecting a form submission to Attio CRM (create contact, update deal)
- Embedding Calendly scheduling into a page
- Implementing OAuth login flows via Composio
- Building UI components that display data from these services (contact info, upcoming events, auth status)
- Handling webhook-triggered UI updates from these services

## Context Loading

Before any integration work:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `tenants/<tenant>/config.yaml` for tenant-specific API configuration
3. Read existing API route implementations in `web/src/app/api/` to understand available endpoints
4. Read the page specification that requires the integration
5. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Architecture Principle: Proxy Pattern

Client-side code NEVER holds API keys or calls third-party APIs directly.

```
Browser -> Internal API Route (/api/crm/contact) -> Attio API
Browser -> Internal API Route (/api/schedule/slots) -> Calendly API
Browser -> Internal API Route (/api/auth/connect)   -> Composio OAuth
```

The internal API route handles:
- Authentication (API keys from server-side env vars)
- Request validation and transformation
- Rate limiting
- Error normalization

The client-side code handles:
- UI state management
- Optimistic updates
- Error display
- Loading states

## Attio CRM Integration

### Creating Contacts from Forms

After form submission, the server action or API route creates the Attio contact. The client-side flow:

1. User submits a form (contact, application, signup)
2. Server action validates input, calls Attio API to create/update the person record
3. Server action returns `{ success: true, contactId: string }` or `{ success: false, errors: {...} }`
4. Client shows success confirmation or error state

### Displaying CRM Data

For authenticated admin views that show CRM data:
- Fetch from `/api/crm/contacts` or `/api/crm/deals` (internal proxy route)
- Use SWR or React Query for client-side caching and revalidation
- Show loading skeletons while data loads
- Handle empty states ("No contacts found")
- Never expose Attio record IDs in public-facing URLs

### Attio Data Shapes

Common fields to map:
- Person: email, first name, last name, phone, company, tags
- Deal: name, stage, value, close date, associated contacts
- Note: content, associated record, created date

Map Attio field IDs to human-readable names in a configuration file, not inline in components.

## Calendly Integration

### Embed Widget

The Calendly inline widget is the simplest integration:

```tsx
// CalendlyEmbed.tsx
'use client'
import { useEffect } from 'react'

export function CalendlyEmbed({ url, prefill }: { url: string, prefill?: CalendlyPrefill }) {
  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://assets.calendly.com/assets/external/widget.js'
    script.async = true
    document.body.appendChild(script)
    return () => { document.body.removeChild(script) }
  }, [])

  return (
    <div
      className="calendly-inline-widget"
      data-url={`${url}?${buildPrefillParams(prefill)}`}
      style={{ minWidth: 320, height: 700 }}
    />
  )
}
```

### Custom Scheduling UI

For branded scheduling experiences that do not use the Calendly embed:
1. Fetch available event types from `/api/schedule/event-types`
2. Fetch available time slots from `/api/schedule/slots?event_type=<id>&date=<date>`
3. Display a custom date picker and time slot grid
4. On selection, POST to `/api/schedule/book` with the chosen slot and invitee details
5. Show confirmation with calendar add links (Google, Outlook, iCal)

### Calendly Webhook Handling

Calendly webhooks (invitee.created, invitee.canceled) hit the backend API route. The client-side sees the result indirectly:
- After booking, poll `/api/schedule/status?booking_id=<id>` or use server-sent events
- Show booking confirmation, cancellation, or rescheduling status
- Update any CRM-linked displays (the backend syncs Calendly events to Attio)

## Composio OAuth Integration

### Login Flow

1. User clicks "Connect with [Provider]" button
2. Client redirects to `/api/auth/connect?provider=<provider>` (internal route)
3. Backend generates the OAuth authorization URL via Composio and redirects the browser
4. User completes OAuth on the provider's site
5. Provider redirects back to `/api/auth/callback` with the authorization code
6. Backend exchanges the code for tokens via Composio, stores the connection
7. Backend redirects to the success page with a session cookie

### Connection Status

Display connected accounts and their status:
- Fetch from `/api/auth/connections` (returns connected providers, scopes, expiry)
- Show connected/disconnected status per provider
- Provide disconnect and reconnect actions
- Show scope warnings if the connection has fewer scopes than required

### Supported Providers

Composio supports multiple OAuth providers. Common ones for Lumina OS:
- Google (Calendar, Drive, Gmail)
- Slack
- Zoom
- HubSpot
- Stripe

The client-side code is provider-agnostic -- it uses the same UI pattern for all providers. Provider-specific logic lives in the backend API routes.

## Client-Side Data Fetching Patterns

### SWR Pattern

```tsx
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => {
  if (!r.ok) throw new Error('Fetch failed')
  return r.json()
})

function ContactList() {
  const { data, error, isLoading } = useSWR('/api/crm/contacts', fetcher)

  if (isLoading) return <ContactListSkeleton />
  if (error) return <ErrorState message="Unable to load contacts" onRetry={() => mutate('/api/crm/contacts')} />
  if (!data?.contacts?.length) return <EmptyState message="No contacts yet" />

  return <ul>{data.contacts.map(c => <ContactRow key={c.id} contact={c} />)}</ul>
}
```

### Optimistic Updates

For actions like creating a contact or booking a slot:
1. Immediately update the local UI state (optimistic)
2. Send the mutation to the API
3. On success: confirm the optimistic update
4. On failure: revert the optimistic update and show an error

### Error Handling

All API calls must handle:
- Network errors (offline, timeout) -- show "Connection lost. Retrying..."
- 401 Unauthorized -- redirect to login or show session expired message
- 403 Forbidden -- show "You don't have permission" message
- 404 Not Found -- show "Resource not found" message
- 422 Validation Error -- map field errors to the form
- 429 Rate Limited -- show "Please wait" with countdown
- 500 Server Error -- show generic error with retry option

Never show raw API error messages to users. Log them for debugging; display user-friendly text.

## Output Format

- Client components in `web/src/components/integrations/`
- Type definitions in `web/src/types/`
- Custom hooks in `web/src/hooks/`
- Integration configuration in `web/src/config/integrations.ts`

## Boundaries

- Never store API keys, tokens, or secrets in client-side code
- Never call third-party APIs directly from client-side code -- always proxy through internal API routes
- Never expose internal record IDs (Attio, Calendly) in public URLs
- Never build payment integrations -- defer to specialized payment skills

## Dependencies

- `api-routes` -- backend API route implementation that this skill's client code calls
- `form-building` -- forms that trigger CRM and scheduling integrations
- `composio-oauth` -- backend OAuth flow that this skill's login UI initiates
- `calendly-integration` -- backend Calendly API handling
- `attio-crm` -- backend Attio API handling

## State Tracking

- `integrations` -- keyed by integration name: status (connected/disconnected), last synced, error count
- `apiEndpoints` -- keyed by endpoint path: method, purpose, connected integration
