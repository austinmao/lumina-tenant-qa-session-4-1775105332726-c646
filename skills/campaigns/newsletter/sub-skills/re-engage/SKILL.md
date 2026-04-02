---
name: newsletter-re-engage
description: "Use when running the re-engagement sequence for inactive newsletter subscribers"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /newsletter-re-engage
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      env:
        - RESEND_API_KEY
        - DATABASE_URL
        - RESEND_TRANSACTIONAL_FROM
        - RESEND_TRANSACTIONAL_REPLY_TO
        - SLACK_BOT_TOKEN
      bins:
        - bash
        - curl
        - jq
---

# Newsletter Re-Engage Sub-Skill

## Overview

Post-send cleanup step: identifies subscribers with no opens in the last 90 days
(approximately 12 consecutive issues) and sends a 3-email re-engagement sequence.
Called automatically by the deliver sub-skill after each newsletter send.
Can also be triggered manually via `/newsletter-re-engage`.

## Trigger Condition

A subscriber qualifies for re-engagement when they have zero open events in the
last 12 consecutive sends (approximately 90 days).

## Detection Query

Use `public.relay_contacts` as the live contact source. Do not assume a legacy
`newsletter_subscribers` table exists.

```sql
SELECT email, first_name
FROM relay_contacts
WHERE email IS NOT NULL
  AND consent_status = 'opted_in'
  AND (
    last_engaged_at IS NULL
    OR last_engaged_at < NOW() - INTERVAL '90 days'
  );
```

Run this query after every newsletter send. If 0 rows returned: log "0 subscribers
qualify for re-engagement", still write `memory/logs/suppressions/YYYY-MM-DD.md`,
and exit cleanly.

## 3-Email Sequence

Send emails sequentially per subscriber, not as a batch blast.
Each email uses the standard Resend single-send API call.

### Email 1 — Day 0: "Are we still a fit?"

Subject formula: F4 (Personal/Conversational)
Subject examples: "still want to hear from us?" / "honest question"
Character limit: 40 chars max.

Body (80-100 words):
- Open by acknowledging they haven't been opening the newsletter — no guilt, no passive aggression
- Offer a clear, simple choice: stay or go
- Tone: Ram Dass register — fellow pilgrim checking in, not a company performing concern
- One CTA: "Stay on the list →" linked to a one-click preference confirmation URL

```bash
curl -s -X POST https://api.resend.com/emails \
  -H "Authorization: Bearer $RESEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "'"$RESEND_TRANSACTIONAL_FROM"'",
    "reply_to": "'"$RESEND_TRANSACTIONAL_REPLY_TO"'",
    "to": ["{{email}}"],
    "subject": "still want to hear from us?",
    "html": "{{rendered_body}}"
  }' | jq '{id, to: .to[0]}'
```

Log delivery ID. Set a tracking note in the suppression log for this subscriber.

### Email 2 — Day 7: Best-of value delivery

Send only to subscribers from Email 1 who have NOT clicked the confirmation link.

Subject: the subject line with the highest open rate from the last 12 sends
(query `memory/logs/analytics-summary.md` or Postgres campaign_assets for best performer).
Use the Formula 1 or Formula 4 subject line from that issue.

Body (150-200 words):
- Reprint the best-performing Teaching section from the last 12 sends (highest open rate issue)
- No pitch, no CTA to a retreat or call
- One CTA only: "Read more →" linking to an organization blog post
- Tone: pure value, no transaction

Set a tracking note in the suppression log for this subscriber.

### Email 3 — Day 14: Sunset notice

Send only to subscribers from Email 2 who have NOT opened or clicked.

Subject: "removing you from this list on [specific date]"
The date must be exactly 48 hours from the send time of Email 3.

Body (2 sentences maximum):
- State the exact removal date
- Provide a one-click "Keep me subscribed" link

Example:
> "We'll remove you from the Sunday Service list on [Day, Month DD] unless you'd like to stay.
> [Keep me subscribed →]"

Set the planned sunset date in the suppression log for this subscriber.

## Suppression Actions (after Email 3 + 48h)

Run this step as a scheduled cleanup, or manually via `/newsletter-re-engage --suppress`:

1. Query subscribers past their sunset date who did not click the "Keep me subscribed" link:

```sql
SELECT email FROM relay_contacts
WHERE email IS NOT NULL
  AND consent_status = 'opted_in'
  AND (
    last_engaged_at IS NULL
    OR last_engaged_at < NOW() - INTERVAL '90 days'
  );
```

2. For each returned subscriber:
   - Set `consent_status = 'suppressed'` and `lead_stage = 'suppressed'` in Postgres
   - Remove from Resend audience / apply suppress tag via Resend contacts API
   - DO NOT delete the contact record from Attio — CRM history must be preserved

3. Log all sunset actions to `memory/logs/suppressions/YYYY-MM-DD.md`:

```
# Suppression Log — YYYY-MM-DD
Total suppressed this run: [N]
Addresses: [list]
Reason: re-engagement sequence exhausted — no response to 3-email sequence
Attio: retained (not deleted)
Resend: suppressed
```

4. Notify the operator in #lumina-bot:
   "Re-engagement cleanup: [N] subscribers sunset after no response to 3-email sequence."

## Error Handling

- `DATABASE_URL` missing: stop, notify the operator
- `RESEND_API_KEY` missing: stop, notify the operator
- Detection query returns error: log error, notify the operator, skip re-engage run
- Email 1 Resend call fails (4xx/5xx): log failure for that subscriber, continue to next; notify the operator
- Suppression Postgres update fails: log affected addresses to suppression log; notify the operator for manual resolution
- Resend audience API call fails for suppression: log error; the operator must suppress manually in Resend dashboard
- If the live contact schema is present but yields zero opted-in contacts, write a zero-action suppression log and exit cleanly
