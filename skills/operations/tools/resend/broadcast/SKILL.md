---
name: resend-broadcast
description: "Create and schedule Resend broadcast emails to audience segments"
version: "1.0.0"
permissions:
  filesystem: none
  network: true
triggers:
  - command: /resend-broadcast
metadata:
  openclaw:
    emoji: "📣"
    requires:
      env:
        - RESEND_API_KEY
        - RESEND_AUDIENCE_ID
      bins:
        - curl
        - jq
---

# Resend Broadcast API Integration

## Overview

This skill provides the raw Resend Broadcasts API layer for creating audience
segments, scheduling broadcast emails, and retrieving domain-level delivery
statistics. It is a service dependency — outbound broadcast sends route through
ClawWrap's `outbound.submit` handler.

**Routing rule:** When send is `true`, the broadcast operation MUST route through
`outbound.submit` with `channel: resend-broadcast`. Draft creation (`send: false`)
does not require ClawWrap.

## Required Environment Variables

Set in `.env` before any broadcast operation:

```
RESEND_API_KEY      — Resend API key with broadcast + audience permissions
RESEND_AUDIENCE_ID  — Default audience ID for segment operations
```

Never hardcode these values in agent workspace files or skill instructions.

## API Reference

### 1. Create a Segment

Create a named segment within an audience for targeted broadcast delivery.

```bash
curl -s -X POST "https://api.resend.com/audiences/$RESEND_AUDIENCE_ID/segments" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Segment Name Here"
  }' | jq .
```

Success response contains `id` (segment ID) — store this for broadcast targeting.

### 2. Add a Contact to a Segment

Associate an existing contact with a segment by email address and segment ID.

```bash
curl -s -X POST "https://api.resend.com/audiences/$RESEND_AUDIENCE_ID/contacts/{email}/segments/{segment_id}" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" | jq .
```

Replace `{email}` with the contact's email address and `{segment_id}` with the
target segment ID returned from segment creation.

### 3. Create a Broadcast (Draft or Send)

Create a broadcast email. Set `send` to `false` to save as draft, or `true` to
send immediately (or at `scheduledAt` if provided).

```bash
curl -s -X POST https://api.resend.com/broadcasts \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audienceId": "'"$RESEND_AUDIENCE_ID"'",
    "segmentId": "seg_xxxxxxxxxxxx",
    "from": "'"$RESEND_FROM_ADDRESS"'",
    "subject": "Your Subject Here",
    "html": "<p>Email body here</p>",
    "send": false
  }' | jq .
```

**With scheduling** (ISO 8601 datetime, must be in the future):

```bash
curl -s -X POST https://api.resend.com/broadcasts \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audienceId": "'"$RESEND_AUDIENCE_ID"'",
    "segmentId": "seg_xxxxxxxxxxxx",
    "from": "'"$RESEND_FROM_ADDRESS"'",
    "subject": "Your Subject Here",
    "html": "<p>Email body here</p>",
    "send": true,
    "scheduledAt": "2026-04-01T09:00:00Z"
  }' | jq .
```

Success response contains `id` (broadcast ID) — log this for every broadcast
operation.

**ClawWrap integration:** When `send` is `true`, this operation MUST route
through `outbound.submit` with `channel: resend-broadcast`. Draft creation
(`send: false`) does not require ClawWrap.

### 4. Get Domain Delivery Statistics

Retrieve aggregate delivery statistics for a sending domain.

```bash
curl -s "https://api.resend.com/domains/{domain_id}" \
  -H "Authorization: Bearer $RESEND_API_KEY" | jq '{
    sent: .sent,
    opened: .opened,
    clicked: .clicked,
    complained: .complained,
    unsubscribed: .unsubscribed
  }'
```

Replace `{domain_id}` with the Resend domain ID. Returns counters for sent,
opened, clicked, complained, and unsubscribed.

### 5. Toggle Domain Tracking

Enable or disable open tracking and click tracking on a sending domain.

```bash
curl -s -X PATCH "https://api.resend.com/domains/{domain_id}" \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "open_tracking": true,
    "click_tracking": true
  }' | jq .
```

Set `open_tracking` and `click_tracking` to `true` or `false` as needed.
Tracking changes apply to all future sends on the domain.

## Merge Tags

Resend broadcasts support merge tags for contact-level personalization.

| Tag | Purpose |
|---|---|
| `{{{FIRST_NAME\|there}}}` | Contact first name with fallback to "there" |
| `{{{LAST_NAME}}}` | Contact last name (no fallback — blank if missing) |
| `{{{RESEND_UNSUBSCRIBE_URL}}}` | Built-in one-click unsubscribe link |

**Usage example:**

```html
<p>Hi {{{FIRST_NAME|there}}},</p>
<p>Here is your weekly update.</p>
<p><a href="{{{RESEND_UNSUBSCRIBE_URL}}}">Unsubscribe</a></p>
```

Every broadcast email MUST include `{{{RESEND_UNSUBSCRIBE_URL}}}` in the footer.
Omitting the unsubscribe link violates CAN-SPAM and will degrade sender reputation.

## Error Handling

- `4xx` response: stop immediately, log the full response body, notify the
  operator in #lumina-bot before any retry
- `5xx` response: stop immediately, log error, notify the operator — do not
  retry without instruction
- Network timeout: log how many operations completed before failure, notify the
  operator
- `422` with `"segment not found"`: verify the segment ID exists within the
  audience before retrying
- `429` rate limit: back off and notify the operator — do not auto-retry
  broadcast sends

## Skill Dependency Map

```
resend-broadcast  →  uses resend  (inherits RESEND_API_KEY)
resend-broadcast  →  gated by ClawWrap outbound.submit  (when send: true)
email-newsletter  →  may trigger resend-broadcast  (for audience-targeted campaigns)
```

This skill documents the Resend Broadcasts API contract and environment
requirements. Approval gates and outbound routing enforcement live in the
ClawWrap outbound gate, not here.
