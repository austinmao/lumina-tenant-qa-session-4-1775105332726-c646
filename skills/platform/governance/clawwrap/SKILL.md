---
name: clawwrap
description: "Route outbound sends through ClawWrap gate / add targets / check policy"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /clawwrap
metadata:
  openclaw:
    emoji: "\U0001F6E1"
    requires:
      bins: ["python3"]
      env: []
      os: ["darwin", "linux"]
---

# ClawWrap Outbound Gate

Route every agent-initiated outbound send (email, WhatsApp, Slack, Mailchimp) through the ClawWrap gate. The gate validates the TARGET, not the permission to send. Human approval (Constitution Principle I) remains the calling skill's responsibility.

## 1. Submit an Outbound Send

Call `outbound.submit` with semantic intent. Never resolve targets directly.

**Shared route** (context_key + audience + channel):
```yaml
outbound.submit:
  route_mode: shared
  context_key: awaken-apr-2026        # lookup key in targets.yaml
  audience: staff                      # audience within that context
  channel: whatsapp                    # whatsapp | email | slack | mailchimp
  message: "Staff meeting at 3pm"
  requested_by: post-call-whatsapp     # calling skill name
  dry_run: false                       # true = resolve + verify only, no send
```

**Direct route** (recipient_ref via resolver adapter):
```yaml
outbound.submit:
  route_mode: direct
  recipient_ref: "airtable:contacts/rec123"   # or retreat_guru:registrations/456
  channel: email
  message: "Your registration is confirmed"
  requested_by: intake-coordination
```

**Pipeline**: resolve -> verify -> dispatch -> audit.
1. **Resolve** -- target from `targets.yaml` (shared) or adapter resolver (direct)
2. **Verify** -- 6 policy checks against `outbound-policy.yaml` + gateway config
3. **Dispatch** -- channel handler (`email.send`, `slack.post`, `dm.send_text`, `mailchimp.send_campaign`)
4. **Audit** -- structured verdict appended to `memory/logs/outbound/YYYY-MM-DD.yaml`

Fail-closed: any failed check denies the send and audits the denial.

## 2. Add a New Target

1. Add entry to `targets.yaml` (tenant-scoped: `tenants/<id>/config/targets.yaml`):
   ```yaml
   targets:
     heal-jun-2026:
       staff:
         whatsapp:
           target: "120363...@g.us"
           verify: { title: "Heal Jun 2026 Staff" }
         email:
           target: staff-heal@[the organization's domain]
   audience_labels:
     heal-jun-2026:
       staff: "Heal Jun 2026 -- staff only"
   ```
2. Allowlist in `outbound-policy.yaml` under `allowlists.shared.<channel>`:
   ```yaml
   - heal-jun-2026.staff
   ```
3. Dry-run validate: submit with `dry_run: true`, confirm `allowed: true`.

For dynamically created targets (e.g., new WhatsApp group), use `fill_empty_target` to atomically write into an existing null slot in targets.yaml.

## 3. Check Policy

Submit with `dry_run: true` to verify a route without sending:
```yaml
outbound.submit:
  route_mode: shared
  context_key: awaken-apr-2026
  audience: participant
  channel: whatsapp
  message: "policy check"
  requested_by: preflight-check
  dry_run: true
```

`allowed: true` means all 6 checks pass: `target_exists`, `target_in_gate_allowlist`, `audience_matches`, `live_identity_matches`, `channel_enabled`, `target_passes_gateway_constraints`.

## 4. View Audit Trail

Read `memory/logs/outbound/YYYY-MM-DD.yaml`. Each entry is a serialized `GateVerdict` with fields: `allowed`, `request_id`, `target`, `audience_label`, `channel`, `requested_by`, `checks[]` (name + passed + detail), `denied_by`, `reason`, `timestamp`, `send_result`.

## 5. Key Rules

- SOUL.md and SKILL.md must **never** contain hardcoded JIDs, email addresses, or channel IDs
- Skills express semantic intent (`context_key` + `audience` + `channel`) -- the gate resolves addresses
- The gate validates the target but does **not** replace Constitution Principle I (the operator's per-session approval)
- Fail-closed: unknown targets, unlisted audiences, and disabled channels are denied
- Multi-tenant: set `COMPOSIO_USER_ID` to route to `tenants/<id>/config/` instead of `clawwrap/config/`
- Supported channels: `email`, `whatsapp`, `slack`, `mailchimp` (live); `imessage`, `sms`, `telegram` (planned)
- Audit logging is best-effort -- write failures do not block sends
