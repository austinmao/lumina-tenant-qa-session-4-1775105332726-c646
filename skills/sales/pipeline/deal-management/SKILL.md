---
name: deal-management
description: >
  Create, update, and manage Attio CRM deals for the organization's sales
  pipeline. Use this skill when a post-call Fireflies sync fires (create deal),
  when a deal stage changes (update stage), or when you need to log touchpoints,
  objections, or next actions to a deal record.
version: 1.0.0
permissions:
  filesystem: none
  network: true
metadata:
  openclaw:
    emoji: "deal"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env:
        - ATTIO_API_KEY
      bins: []
---

# Deal Management Skill

## Purpose

All Attio CRM deal operations for the organization's sales pipeline. This skill
covers deal creation, stage transitions, note logging, and rep assignment.

## Deal Schema

When creating a deal in Attio, populate these fields:

| Field | Value | Notes |
|---|---|---|
| Name | "[Contact Name] — [Retreat Interest] — [YYYY-MM]" | e.g., "Sarah Chen — September Retreat — 2026-06" |
| Stage | "Discovery Call Completed" | Always start here after Trigger 3 |
| Amount | Estimated retreat price | Use pricing-yield agent for exact figure |
| Owner | Assigned sales rep (Ethan or Val) | From Attio contact record |
| Contact | Linked Attio contact ID | Link the deal to the existing contact |
| Source | "Discovery Call" | Or overridden by actual source |
| Fireflies URL | Link to call recording/summary | Paste in deal notes field |
| Notes | Summary of call key points | Extracted from Fireflies (see fireflies-sync skill) |

## Deal Stage Definitions

| Stage | Meaning | Who can advance |
|---|---|---|
| Discovery Call Completed | Call done; post-call follow-up sent | enrollment agent (auto) |
| Proposal Sent | Written proposal or pricing sent to lead | enrollment agent (after rep approval) |
| Negotiating | Lead is considering; objections active | enrollment agent |
| Objection Raised | Specific objection flagged for rep | enrollment agent (flags; rep resolves) |
| Closing | Rep has committed to close; deposit request pending | rep only |
| Won — Booked | Deposit received; retreat confirmed | rep (after payment confirmed) |
| Lost — Not Moving Forward | Lead declined or went cold | enrollment agent |
| Re-engagement Queue | Cold lead; queued for 90-day meaningful-event trigger | lead-nurture agent |

## Operations

### Create Deal (Trigger 3 — post-Fireflies sync)

Use the Attio v2 objects API. Deals are a custom object; the slug may be
`deals` or a workspace-specific slug — confirm with `GET /v2/objects` if
uncertain.

```
POST /v2/objects/deals/records
{
  "data": {
    "values": {
      "name": [{ "value": "[Contact Name] — [Retreat Interest] — [YYYY-MM]" }],
      "stage": [{ "value": "Discovery Call Completed" }],
      "amount": [{ "currency_value": <estimated price>, "currency_code": "USD" }],
      "owner": [{ "referenced_actor_type": "workspace-member", "referenced_actor_id": "<rep_attio_user_id>" }],
      "associated_people": [{ "target_object": "people", "target_record_id": "<contact_attio_id>" }],
      "fireflies_url": [{ "value": "<transcript_url>" }],
      "assigned_rep_email": [{ "value": "<rep_email>" }]
    }
  }
}
```

After creating: log Fireflies summary as a deal note using
`POST /v2/notes` with the returned deal record ID. Do NOT include any
health/medical data from intake forms in deal notes.

### Update Deal Stage

```
PATCH /v2/objects/deals/records/<record_id>
{
  "data": {
    "values": {
      "stage": [{ "value": "<new_stage>" }]
    }
  }
}
```

Always log the stage change reason in deal notes with timestamp and trigger type.

### Log a Touchpoint

After every outbound Resend email, use the `resend/log-to-attio` skill.
That skill writes the canonical touchpoint note to the People record (and
optionally to the deal record) and writes the local send-log and CRM-writes
audit entries. Do not duplicate that logic here.

The touchpoint note format written by `resend/log-to-attio` is:

```
[YYYY-MM-DD HH:MM UTC] Email touchpoint
From: lumina@[the configured sending domain]
To: <recipient_email>
Subject: <subject>
Channel: Resend
Resend ID: <resend_id>
Template: <template_name>
Context: <send_context>
Rep CC: <rep_email>
```

For non-Resend touchpoints (iMessage, Slack, inbound reply handling),
log directly to deal notes in this format:

```
[YYYY-MM-DD HH:MM] <Channel> touchpoint
From: lumina@[the organization's domain]
CC: <rep_email>
Type: <Auto-send | Draft — awaiting approval>
Subject/Content: <subject line or first sentence>
Next action: <what was promised or scheduled>
```

### Flag for Rep Approval

When a message requires human approval before sending:

```
[YYYY-MM-DD HH:MM] APPROVAL REQUIRED
Message type: <Objection response | Pricing proposal | Closing message>
Draft location: <memory/drafts/YYYY-MM-DD-<slug>.md>
Assigned rep: <rep_email>
Status: Awaiting approval
```

Log this to deal notes AND notify the rep via their preferred channel.

## Rules

- Never create a deal without a linked Attio contact — always confirm contact
  record exists first
- Never update deal stage to "Won — Booked" without rep confirmation of payment
- Never log medical intake data (health history, contraindications) in deal notes
- The pricing-yield agent owns amount estimates for proposals — do not override
  their estimate without rep approval
- When a deal moves to "Lost — Not Moving Forward": do NOT delete the deal;
  update the stage and schedule a re-engagement note in 90 days
