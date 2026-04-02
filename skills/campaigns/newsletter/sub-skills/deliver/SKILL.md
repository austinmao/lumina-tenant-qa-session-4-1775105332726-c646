---
name: newsletter-deliver
description: "Use when rendering and sending an approved newsletter, then logging to Postgres and Attio"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /newsletter-deliver
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      env:
        - MAILCHIMP_API_KEY
        - DATABASE_URL
        - SLACK_BOT_TOKEN
      bins:
        - bash
        - node
        - npx
---

# Newsletter Deliver Sub-Skill

## Overview

Step 4 of the newsletter pipeline. Runs only after gate PASSED and the operator has
explicitly approved in Slack. Renders the email template, routes the send via
`outbound.submit` to the ClawWrap mailchimp channel, creates Postgres campaign records,
logs to Attio, and notifies the operator.

## MANDATORY: Tool Call Enforcement

Before starting work:
1. `read` the handoff contract at the path provided in the task
2. Verify `binding.no_mailchimp_send` — if true, push HTML to Mailchimp campaign content but do NOT trigger send

Execution:
3. `read` the approved draft file at `prior_work.approved_draft`
4. `exec` render.ts with renderOnly mode:
   cd /Users/luminamao/Documents/Github/openclaw/templates/email && echo '{"templateName":"sunday-service-newsletter","participants":[{"firstName":"Preview","email":"preview@test.com"}],"dryRun":true,"renderOnly":true,...}' | npx tsx render.ts
5. `exec` push HTML to Mailchimp campaign via Python script or curl

After completing work:
6. `write` the send report to the artifact_path
7. The ContextEngine plugin runs verification assertions automatically

## Pre-Send Checklist (verify all before any API call)

- [ ] Draft file contains `gate_status: PASSED` at the top
- [ ] the operator's Slack approval message is confirmed in this session (timestamp recorded)
- [ ] Segment sub-skill has run: `memory/drafts/YYYY-MM-DD-[type]-segment.md` exists
- [ ] Suppression list is current (segment sub-skill output, not older than 30 minutes)

If any checklist item is not met: stop, notify the operator with the specific blocking item.

When the segment file declares a `TEST MODE override`, route all recipients to
`lumina.qa@agentmail.to` and continue writing the normal send report.
In `test_mode=true`, the send report is still required even when the external
delivery call is simulated or blocked by sandbox credentials.

## Render

Load `render-react-email-assets` for the canonical orchestration render contract.
For newsletter templates, the current concrete adapter remains `templates/email/render.ts`
until the registry path is fully migrated onto the shared renderer.

Call `templates/email/render.ts` via `node`/`npx tsx`:

```bash
echo '{
  "templateName": "sunday-service-newsletter",
  "participants": [BATCH],
  "headline": "{{headline}}",
  "openingReflection": "{{opening}}",
  "teachingHeading": "{{teachingH}}",
  "teachingBody": "{{teachingBody}}",
  "events": <events_array>,
  "ctaText": "{{ctaText}}",
  "ctaUrl": "{{ctaUrl}}",
  "unsubscribeUrl": "{{unsubUrl}}",
  "issueDate": "{{YYYY-MM-DD}}"
}' | npx tsx templates/email/render.ts
```

Substitute `templateName` with the correct template for the newsletter type (from type registry in parent skill).

Pull all `{{placeholder}}` values from the approved draft file. Do not compose inline — always use the saved draft as source of truth.

If render fails: stop, notify the operator with the render error output.

## Send via Outbound Gate

After rendering, submit to ClawWrap:

```
outbound.submit:
  route_mode: shared
  context_key: newsletter
  audience: full-list
  channel: mailchimp
  message: "[subject line from approved draft]"
  requested_by: newsletter-deliver
  payload:
    subject: "[subject line]"
    html: "[rendered HTML from render.ts]"
    plain_text: "[plain text fallback]"
    from_name: "[configured sender name]"
    from_email: "[configured sending address]"
    reply_to: "[configured reply-to address]"
```

**Mailchimp List ID**: The list ID is resolved by ClawWrap from `targets.yaml` via
`outbound.submit` with `context_key: newsletter.full-list, channel: mailchimp`.
Never hardcode list IDs in this skill — all Mailchimp list addresses are registered
in your tenant's `config/targets.yaml`.

The ClawWrap mailchimp handler creates the campaign, sets content, runs send-checklist,
and triggers send. If any step fails, the gate returns a denied verdict — do not retry.
Notify the operator with the gate verdict details.

On success, extract `mailchimp_campaign_id` from the gate verdict's `send_result` for
the send report and analytics sub-skill.

## Test Mode Simulation Rule

If `test_mode=true` and the delivery attempt is blocked by auth, missing credentials,
or any other non-content infrastructure issue:
- do not treat that as a production send
- do not write Postgres or Attio records
- still write `memory/logs/sends/YYYY-MM-DD-[type].md` as a staged send report
- include the failure detail explicitly

Use this shape:

```
# Send Report — [Newsletter Type] — YYYY-MM-DD

delivery_mode: test_simulated
delivery_channel: mailchimp
mailchimp_campaign_id: null
audience_list_id: "[resolved by ClawWrap from targets.yaml via context_key: newsletter.full-list]"
total_recipients: [N]
batches: 0
failures: 1 — [error detail]
operator_approval: simulated via command context
target: lumina.qa@agentmail.to
tokens_used: [estimate if available]
```

This staged report is the required smoke artifact for test mode when outbound gate
infrastructure is unavailable.

## Post-Send Steps

### 1. Create Postgres Campaign Record

```bash
psql "$DATABASE_URL" -c \
  "INSERT INTO campaigns (campaign_type, status, slug, sent_at)
   VALUES ('newsletter', 'published', '[type]-YYYY-MM-DD', NOW())
   RETURNING id;"
```

Save the returned campaign `id` for the asset record.

### 2. Create Campaign Asset Record

```bash
psql "$DATABASE_URL" -c \
  "INSERT INTO campaign_assets (campaign_id, category, slug, created_at)
   VALUES ([campaign_id], 'email_newsletter', '[type]-YYYY-MM-DD', NOW());"
```

### 3. Log to Attio

Invoke `resend/log-to-attio` skill with the send summary. This step is mandatory —
the Attio CRM must reflect every outbound send.

If Attio logging fails: note the failure in the send log; notify the operator; do not
block completion on Attio — the primary send is already done.

### 4. Write Send Report

Write to `memory/logs/sends/YYYY-MM-DD-[type].md`:

```
# Send Report — [Newsletter Type] — YYYY-MM-DD

delivery_channel: mailchimp
mailchimp_campaign_id: [campaign_id from gate verdict]
audience_list_id: "[resolved by ClawWrap from targets.yaml via context_key: newsletter.full-list, channel: mailchimp]"
send_checklist_passed: true
operator_approval: [Slack message timestamp]
tokens_used: [estimate if available]
```

### 5. Trigger Re-Engage Sub-Skill

After send log is written: invoke `newsletter/sub-skills/re-engage` as a cleanup step.
This identifies inactive subscribers (0 opens in 90 days) and starts the re-engagement sequence.

### 6. Notify the operator

Post to #lumina-bot:

```
[Type] newsletter sent via Mailchimp.
Campaign ID: [mailchimp_campaign_id]
Send checklist: passed
Open/click tracking available in 48h — run /newsletter-analytics after then.
```

## Error Handling

- Gate not passed: refuse to send, notify the operator — the gate must pass before deliver runs
- the operator approval not confirmed in session: refuse to send, ask the operator to confirm in Slack
- Segment file older than 30 minutes: re-run segment sub-skill before sending
- Render failure: stop, notify the operator with error
- Outbound gate denied verdict: do not retry, notify the operator with verdict details
- In test mode, outbound gate auth or credential failures must still produce the staged send report described above
- Postgres insert fails: log error, notify the operator — record must be created manually
