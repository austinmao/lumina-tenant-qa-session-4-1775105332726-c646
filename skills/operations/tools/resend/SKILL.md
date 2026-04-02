---
name: resend
description: >
  Underlying Resend API integration layer for the organization. Provides
  authenticated HTTP calls to the Resend v1 API (send, batch send, delivery
  status lookup). This is NOT a routing target — do not invoke it directly
  from agent triggers. All outbound email sends route through the
  email-newsletter skill, which calls resend internally.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - RESEND_API_KEY
        - RESEND_FROM_ADDRESS
        - RESEND_REPLY_TO
      bins:
        - curl
        - jq
    primaryEnv: RESEND_API_KEY
    routingNote: >
      NOT a routing target. Route all email tasks to email-newsletter.
      resend is a service dependency, not an agent-facing capability.
    homepage: https://resend.com/docs/api-reference/introduction
---

# Resend API Integration

## Purpose

This skill provides the raw Resend API layer for the organization's email
infrastructure. It is a service dependency used internally by other skills —
primarily `email-newsletter` — and is not a routing target in its own right.

**Routing rule:** When the operator or any agent asks to send an email, draft a
newsletter, check delivery status, or manage email campaigns, route to
`email-newsletter`. Do not route to `resend` directly.

## What This Skill Provides

- Authenticated single-email send via Resend `/emails` endpoint
- Batch send support (max 50 recipients per API call — enforced by
  `email-newsletter`)
- Delivery status lookup by Resend email ID
- Bounce and error parsing

## Required Environment Variables

Set in `.env` before any email operation:

```
RESEND_API_KEY          — Resend API key with send permissions
RESEND_FROM_ADDRESS     — "[Organization name] <info@[the configured sending domain]>" (display name required)
RESEND_REPLY_TO         — info@[the organization's domain]
```

Never use a bare email address without the display name in `RESEND_FROM_ADDRESS`.
The display name MUST always be "[Organization name]" — never the operator's personal name.
All outbound email represents the organization, not an individual.
Never change these values without the operator's explicit instruction.

## API Reference

### Send a single email

```bash
curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$RESEND_FROM_ADDRESS"'",
    "reply_to": "'"$RESEND_REPLY_TO"'",
    "to": ["recipient@example.com"],
    "subject": "Subject here",
    "html": "<p>Body here</p>"
  }' | jq .
```

Success response contains `id` (Resend email ID) — log this for every send.

### Check delivery status by ID

```bash
curl -s https://api.resend.com/emails/{email_id} \
  -H "Authorization: Bearer $RESEND_API_KEY" | jq .
```

### Error handling

- `4xx` response: stop immediately, log the full response body, notify the operator
  in #lumina-bot before any retry
- `5xx` response: stop immediately, log error, notify the operator — do not retry
  without instruction
- Network timeout: log how many sends completed before failure, notify the operator

## Skill Dependency Map

```
email-newsletter  →  uses resend  (primary consumer)
intake-coordination  →  uses resend  (via email-newsletter pattern)
participant-prep  →  uses resend  (Getting Started email, food allergy digest)
```

This skill directory exists to document the API integration contract and
environment requirements. The routing intelligence and approval gates live in
the consuming skills, not here.
