---
name: api-routes
description: "Build Next.js API routes with request validation, middleware, and error handling"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /api-routes
metadata:
  openclaw:
    emoji: "🛤️"
    requires:
      bins: ["node"]
      env: []
      os: ["darwin"]
---

# API Routes

Build Next.js App Router API routes (Route Handlers) with request validation, middleware chains, structured error handling, and consistent response shapes. This skill produces the backend endpoints that serve the frontend application and process webhook events.

## When to Use

- Creating a new API endpoint for a feature
- Adding request validation to an existing route
- Implementing middleware (authentication, rate limiting, CORS)
- Standardizing error responses across the API
- Building webhook receivers for external services (Calendly, Stripe, Resend)
- Refactoring scattered API logic into consistent patterns

## Context Loading

Before building any API route:
1. Read existing route patterns in `web/src/app/api/` to follow established conventions
2. Read the feature specification for the endpoint's requirements
3. Read `web/src/lib/` for shared utilities (auth helpers, database clients, validation schemas)
4. Identify all consumers of the endpoint (frontend components, webhook senders, cron jobs)

## Route Handler Structure

### File Location

Next.js App Router convention:
```
web/src/app/api/
  crm/
    contacts/
      route.ts          # GET (list), POST (create)
      [id]/
        route.ts        # GET (single), PATCH (update), DELETE
  schedule/
    event-types/
      route.ts          # GET
    slots/
      route.ts          # GET
    book/
      route.ts          # POST
    webhook/
      route.ts          # POST (Calendly webhook receiver)
  auth/
    connect/
      route.ts          # POST
    callback/
      route.ts          # GET
    connections/
      route.ts          # GET
      [id]/
        route.ts        # DELETE
```

### Basic Route Handler

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    // 1. Authenticate
    const session = await getSession(request)
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // 2. Parse and validate query parameters
    const searchParams = request.nextUrl.searchParams
    const page = parseInt(searchParams.get('page') ?? '1', 10)
    const limit = Math.min(parseInt(searchParams.get('limit') ?? '20', 10), 100)

    // 3. Execute business logic
    const result = await getContacts({ tenantId: session.tenantId, page, limit })

    // 4. Return structured response
    return NextResponse.json({
      data: result.items,
      pagination: { page, limit, total: result.total }
    })
  } catch (error) {
    return handleApiError(error)
  }
}
```

## Request Validation

### Schema Validation with Zod

Define validation schemas alongside route handlers:

```typescript
import { z } from 'zod'

const createContactSchema = z.object({
  email: z.string().email('Invalid email address'),
  firstName: z.string().min(1, 'First name is required').max(100),
  lastName: z.string().max(100).optional(),
  phone: z.string().regex(/^\+[1-9]\d{1,14}$/, 'Phone must be E.164 format').optional(),
  source: z.enum(['form', 'import', 'api']).default('api'),
})

type CreateContactInput = z.infer<typeof createContactSchema>
```

### Validation in the Handler

```typescript
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const validated = createContactSchema.safeParse(body)

    if (!validated.success) {
      return NextResponse.json({
        error: 'Validation failed',
        details: validated.error.flatten().fieldErrors,
      }, { status: 422 })
    }

    // Use validated.data (typed and safe)
    const contact = await createContact(validated.data)
    return NextResponse.json({ data: contact }, { status: 201 })
  } catch (error) {
    return handleApiError(error)
  }
}
```

Never skip validation. Never trust input from any source (browser, webhook, cron).

## Response Shape Convention

All API responses follow a consistent shape:

### Success Responses

```typescript
// Single item
{ data: { id, ...fields } }

// List with pagination
{ data: [...items], pagination: { page, limit, total, totalPages } }

// Action result
{ data: { id }, message: 'Contact created successfully' }
```

### Error Responses

```typescript
// Validation error (422)
{ error: 'Validation failed', details: { email: ['Invalid email address'] } }

// Auth error (401)
{ error: 'Unauthorized' }

// Forbidden (403)
{ error: 'Forbidden', message: 'Insufficient permissions' }

// Not found (404)
{ error: 'Not found', message: 'Contact not found' }

// Server error (500)
{ error: 'Internal server error' }
// Never expose stack traces or internal error details in production
```

## Middleware Patterns

### Authentication Middleware

```typescript
async function requireAuth(request: NextRequest): Promise<Session | NextResponse> {
  const session = await getSession(request)
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  return session
}
```

Call at the top of every protected route. Return early if auth fails.

### Rate Limiting

Implement per-route rate limiting using an in-memory store or Redis:

```typescript
async function rateLimit(request: NextRequest, config: { limit: number, window: number }) {
  const ip = request.headers.get('x-forwarded-for') ?? 'unknown'
  const key = `rate:${request.nextUrl.pathname}:${ip}`
  // Check and increment counter
  // Return 429 if limit exceeded
}
```

Default limits:
- Public endpoints (contact form, newsletter signup): 10 requests/minute per IP
- Authenticated endpoints: 60 requests/minute per user
- Webhook receivers: 100 requests/minute per source IP

### CORS

For routes consumed by external clients:
```typescript
export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': getAllowedOrigin(request),
      'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      'Access-Control-Max-Age': '86400',
    },
  })
}
```

Never use `Access-Control-Allow-Origin: *` on authenticated endpoints.

## Webhook Receivers

### Webhook Handler Pattern

```typescript
export async function POST(request: NextRequest) {
  // 1. Verify signature FIRST (before parsing body)
  const signature = request.headers.get('x-webhook-signature')
  const rawBody = await request.text()

  if (!verifyWebhookSignature(rawBody, signature, process.env.WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 403 })
  }

  // 2. Parse body after verification
  const payload = JSON.parse(rawBody)

  // 3. Idempotency check
  const eventId = payload.event_id
  if (await isEventProcessed(eventId)) {
    return NextResponse.json({ status: 'already processed' }, { status: 200 })
  }

  // 4. Process the event
  await processWebhookEvent(payload)

  // 5. Mark as processed
  await markEventProcessed(eventId)

  // 6. Return 200 quickly (process heavy work async)
  return NextResponse.json({ status: 'received' }, { status: 200 })
}
```

### Webhook Security Rules
- Always verify the webhook signature before processing the body
- Use constant-time comparison for signature verification
- Return 200 quickly to prevent webhook sender timeouts
- Queue heavy processing for async execution
- Log all webhook events for debugging and audit

## Error Handling

### Centralized Error Handler

```typescript
function handleApiError(error: unknown): NextResponse {
  if (error instanceof z.ZodError) {
    return NextResponse.json({
      error: 'Validation failed',
      details: error.flatten().fieldErrors,
    }, { status: 422 })
  }

  if (error instanceof NotFoundError) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }

  if (error instanceof ForbiddenError) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  // Log the full error server-side
  console.error('API error:', error)

  // Return generic message to client
  return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
}
```

Never expose internal error messages, stack traces, or database error details in API responses.

## Testing Convention

Every API route gets a corresponding test file:
- Route: `web/src/app/api/crm/contacts/route.ts`
- Test: `web/src/tests/api/crm/contacts.test.ts`

Test each route for:
- Happy path (valid input, expected output)
- Validation errors (invalid input, 422 response)
- Authentication (missing/invalid auth, 401 response)
- Not found (valid auth, missing resource, 404 response)
- Rate limiting (exceed limit, 429 response)

## Boundaries

- Never expose internal database IDs in public-facing APIs -- use UUIDs
- Never skip request validation, even on internal routes
- Never return raw database errors to clients
- Never process webhook payloads without signature verification
- Never hardcode API keys in route handlers -- use environment variables

## Dependencies

- `postgres-supabase` -- database queries from route handlers
- `composio-oauth` -- OAuth callback routes
- `calendly-integration` -- scheduling webhook and API routes
- `form-building` -- server actions that complement API routes
- `api-client-integration` -- frontend code that consumes these routes

## State Tracking

- `routes` -- keyed by path: methods, auth required, rate limit, validation schema, test coverage
- `webhooks` -- keyed by source: endpoint path, signature verification method, events handled
