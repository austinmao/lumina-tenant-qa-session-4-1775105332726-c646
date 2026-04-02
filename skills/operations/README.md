# skills/operations/

3 operations skills used by the coordinator and other operational agents.

**Primary agent**: `operations/coordinator`

---

## Skills

| Skill | Trigger | Purpose | Deps |
|---|---|---|---|
| `email-triage` | Triage inbound email | Routes inbound email from `lumina@` and `info@` to the correct domain agent by intent | `RESEND_API_KEY`, `ATTIO_API_KEY`, `RESEND_WEBHOOK_SECRET`, `GOG_KEYRING_PASSWORD` |
| `post-call-whatsapp` | Post-call WhatsApp follow-up | Sends a WhatsApp follow-up summary after Zoom calls | `TWILIO_ACCOUNT_SID` |
| `reasoning-router` | Select reasoning effort level | Decision tree: low (heartbeat/lookup) → medium (draft/CRM) → high (strategy) → xhigh (security/adversarial) | — |

## Email Triage Routing

The `email-triage` skill (v2.8.0) is the canonical implementation at `skills/operations/email-triage/`.
See `docs/email-triage-routing.md` for the full routing table and domain rules.

## Reasoning Effort Defaults

| Effort | Use cases |
|---|---|
| `low` | Heartbeat checks, status lookups, log writes |
| `medium` | Email drafts, CRM updates, multi-step workflows (default) |
| `high` | Objection handling, strategy, complex multi-step tasks |
| `xhigh` | Security review, fraud detection, architecture decisions |
