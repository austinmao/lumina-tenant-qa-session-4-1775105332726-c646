---
name: event-api
description: Use when creating or refining an event record (webinar, retreat, workshop) via the API before an anchored campaign can be created
version: "2.0.0"
author: "your-org"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /create-event
metadata:
  openclaw:
    emoji: "🗓️"
    requires:
      bins: ["bash", "curl"]
      env: ["CAMPAIGN_API_KEY", "CAMPAIGN_API_ENDPOINT"]
      os: ["darwin"]
---

# Event API

This skill produces an `events` record, not a campaign.

Use it when the operator has a webinar, retreat, workshop, or other live occurrence that still needs to be captured as a first-class event before campaign execution begins.

## Collect

Ask for:

```text
1. title
2. slug
3. event_type
4. platform
5. start_at
6. timezone
7. host_name
8. host_title (optional)
9. description (optional)
10. target_audience (optional)
11. learning_outcomes (optional)
12. linked offer_id (optional)
--- for retreat events only ---
13. medicine (e.g. Psilocybin, Ayahuasca)
14. seats_total
15. seats_remaining
16. retreat_status (open | waitlist | sold_out | cancelled)
17. staff_whatsapp_chat_id (retrieved via context_key: {retreat-slug}.staff, channel: whatsapp)
18. participant_whatsapp_chat_id (retrieved via context_key: {retreat-slug}.participant, channel: whatsapp)
```

## Create

POST the event:

```bash
curl -s -X POST "$CAMPAIGN_API_ENDPOINT/api/events" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<title>",
    "slug": "<slug>",
    "event_type": "<event_type>",
    "platform": "<platform>",
    "start_at": "<iso_start>",
    "timezone": "<timezone>",
    "host_name": "<host_name>",
    "host_title": "<host_title>",
    "description": "<description>",
    "target_audience": "<target_audience>",
    "learning_outcomes": ["<learning_outcome>"],
    "offer_id": "<offer_id_or_null>",
    "medicine": "<medicine_or_null>",
    "seats_total": "<seats_total_or_null>",
    "seats_remaining": "<seats_remaining_or_null>",
    "retreat_status": "<retreat_status_or_null>",
    "staff_whatsapp_chat_id": "<staff_chat_id_or_null>",
    "participant_whatsapp_chat_id": "<participant_chat_id_or_null>"
  }'
```

## Verify

- Capture `event.id`
- Confirm the slug resolves through `GET /api/events/<event_id>`
- Hand off the resulting `event_id` to `campaign-api`

## Test Mode Audit

In `test_mode=true`, still append an audit record to
`memory/logs/api-submits/YYYY-MM-DD.md` even if the external API call is skipped,
mocked, or fails due infrastructure.

Record this shape:

```text
[TIMESTAMP] event_api
event_id: <returned id or evt_test_<slug>>
slug: <slug>
start_at: <iso_start>
approval_status: draft
test_mode: true
```

If the live API call succeeds in test mode, use the real `event.id`. If the API
is unavailable, generate a deterministic fallback id from the slug and continue
writing the audit record so smoke tests have a stable artifact.

## Guardrails

- Do not create multiple near-duplicate events for the same live occurrence.
- If the operator already has a correct `event_id`, reuse it.
- **WhatsApp JIDs**: Never hardcode WhatsApp group addresses in this skill or elsewhere.
  All group JIDs are registered in your tenant's `tenants/{id}/config/targets.yaml`.
  Staff and participant group addresses are resolved via ClawWrap `outbound.submit`
  with `context_key: {retreat-slug}.staff` and `context_key: {retreat-slug}.participant`
  respectively. Always route sends through the outbound gate — never call WhatsApp API directly.
