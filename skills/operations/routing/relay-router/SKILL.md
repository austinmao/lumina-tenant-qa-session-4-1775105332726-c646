---
name: relay-router
description: "Route inbound message to tenant instance via relay / check if contact belongs to a tenant"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /relay-route
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins: ["curl"]
      env: ["DATABASE_URL"]
      os: ["darwin", "linux"]
---

# Relay Router

Route inbound messages from the hub Lumina instance to the correct tenant instance via the relay channel plugin.

## When to Use

The hub's PreMessageHook invokes this skill's logic when an inbound message arrives on any real channel (WhatsApp, iMessage, Telegram). The skill determines whether the sender's phone number maps to a tenant instance and either forwards, redirects, or passes through.

## Routing Decision

1. Extract sender phone number from inbound message (E.164 format)
2. Query `hub_relay_routing` table by `phone_number`
3. **No match** → return `pass` (message handled by hub's own agents)
4. **Match + `active`** → forward to tenant's `relay_endpoint` via HTTP POST
5. **Match + `dormant`** → reply with `redirect_hint` text on originating channel
6. **Match + `disabled`** → return `pass` (treat as unknown contact)

## Relay Protocol

### Forward to Tenant (active)

```
POST {relay_endpoint}
Authorization: Bearer {LUMINA_RELAY_INBOUND_SECRET}
Content-Type: application/json

{
  "sender_phone": "+15551234567",
  "sender_name": "Jane Doe",
  "message": "Hi, I'd like to learn more",
  "channel_origin": "whatsapp",
  "message_id": "msg_abc123",
  "timestamp": "2026-03-22T14:30:00Z"
}
```

After forwarding, record the message in `hub_relay_messages` for callback correlation.

### Receive Callback from Tenant

The hub's `/lumina-relay/outbound` endpoint receives async callbacks from tenant instances. Before delivering:

1. Validate bearer token matches the tenant's outbound secret
2. Validate `tenant_id` matches the token
3. Validate `recipient_phone` matches the original `sender_phone`
4. Validate `message_id` exists and belongs to this tenant
5. Deliver reply through the originating channel (looked up from hub's own record, not the callback)

## Error Handling

- **Tenant unreachable**: Reply to sender with "I'm having trouble reaching your assistant right now. Please try again in a few minutes."
- **Timeout (no callback in 60s)**: Send "Still working on your request..." to sender
- **Hard timeout (no callback in 5min)**: Send "Sorry, please try again shortly." to sender
- **Invalid callback**: Reject with 403. Log via ClawWrap audit.

## Observability

Emit structured log events:
- `relay.routed` — message forwarded (tenant_id, latency_ms)
- `relay.dormant` — redirect reply sent
- `relay.passthrough` — no match, passed to hub agents
- `relay.callback_received` — tenant callback processed
- `relay.callback_timeout` — no callback within timeout
- `relay.error` — tenant endpoint unreachable or returned error

## Security

- Per-tenant, per-direction secrets stored in Doppler
- Hub-side naming: `LUMINA_RELAY_INBOUND_SECRET_{tenant_id}`, `LUMINA_RELAY_OUTBOUND_SECRET_{tenant_id}`
- Callback validation prevents cross-tenant abuse
- Rate limiting: per-tenant limits on both inbound relay and outbound callbacks
