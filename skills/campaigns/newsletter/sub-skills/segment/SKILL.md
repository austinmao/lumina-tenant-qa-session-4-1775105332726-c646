---
name: newsletter-segment
description: "Use when resolving subscriber journey stages and the suppression list before a newsletter send"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /newsletter-segment
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      env:
        - DATABASE_URL
      bins:
        - bash
        - psql
---

## Channel-Specific Behavior

When the newsletter delivery channel is `mailchimp`, this sub-skill is **skipped**.
Mailchimp owns the subscriber audience (`list_id: 9b70ef06f1`). The deliver sub-skill's
pre-send checklist does not require a segment file for mailchimp sends.

This sub-skill runs only when the delivery channel is `email` (future Resend migration).

# Newsletter Segment Sub-Skill

## Overview

Step 0.5 of the newsletter pipeline (runs before brief). Queries Postgres to
resolve each subscriber's journey stage and builds the suppression exclusion list.
Outputs a segment config that the brief and deliver sub-skills consume.

Call this sub-skill at the start of every newsletter run, before assembling the brief.

## Stage Detection

Primary source of truth in the current stack is `public.relay_contacts`.
Do not assume a legacy `newsletter_subscribers` table exists.

Query the contact table for `lead_stage` and `consent_status`:

```bash
psql "$DATABASE_URL" -t -A -F'|' -c \
  "SELECT email, first_name, lead_stage, consent_status, last_engaged_at
   FROM relay_contacts
   WHERE email IS NOT NULL
   ORDER BY lead_stage, email;"
```

Assign each subscriber to exactly one newsletter stage using this mapping:
- `signed_up`, `messaged`, `replied`, `engaged`, `nurture`, or NULL `lead_stage` -> Inquiry
- `qualified`, `high_intent`, `handoff` -> Applied
- `converted` -> Alumni
- `suppressed` -> do not include in send list; count under suppression instead

Only `consent_status = 'opted_in'` contacts belong in the final send list.
Treat `pending` and `suppressed` contacts as excluded from delivery.

## Per-Stage Resolution

### Inquiry

Subscribed but no application submitted.

- Opening angle: curiosity and invitation; open in universal human experience, not organization-specific context
- Teaching angle: consciousness expansion, science-spirit bridge — do not assume retreat context
- CTA copy: "Book a Connection Call"
- CTA destination: `/book`
- What's Happening filter: surface webinars and free events; deprioritize paid retreat listings
- Merge tokens available: `{{first_name}}`

### Applied

Application submitted; retreat not yet booked.

- Opening angle: threshold — acknowledge the courage of saying yes to the process
- Teaching angle: preparation, what to expect, integration science — assume active consideration
- CTA copy: "Continue Your Journey" or "See Your Next Step"
- CTA destination: scheduling link or approval-gated status page if one exists in the brief context
- What's Happening filter: surface the specific upcoming retreat they applied to if known; fall back to all upcoming retreats
- Merge tokens available: `{{first_name}}`

### Alumni

Has attended at least one retreat.

- Opening angle: integration and continued becoming; address as a community member who already knows
- Teaching angle: deeper context assumed; may reference ceremony experience obliquely (not explicitly)
- CTA copy: "Join Us Again" or "Explore Upcoming Retreats"
- CTA destination: upcoming retreat listing page; referral program URL if referral program is active
- What's Happening filter: surface reunion events, advanced programs, and alumni community moments first
- Merge tokens available: `{{first_name}}`

## Suppression Check

Before finalizing the send list, query for all suppressed addresses:

```bash
psql "$DATABASE_URL" -t -A -F'|' -c \
  "SELECT email, consent_status, lead_stage
   FROM relay_contacts
   WHERE email IS NOT NULL
     AND (consent_status = 'suppressed' OR lead_stage = 'suppressed');"
```

Exclude every returned address from the send list. Do not send to suppressed contacts under any circumstances.

Log the exclusion count:
```
Suppression exclusions: [N] addresses removed from send list
  - consent_status=suppressed: [n]
  - lead_stage=suppressed: [n]
```

## Output

Write the resolved segment config to the content brief location:
`memory/drafts/YYYY-MM-DD-[newsletter-type]-segment.md`

```
# Segment Config — [Type] — YYYY-MM-DD

## Send List Counts
- Inquiry: [N] subscribers
- Applied: [N] subscribers
- Alumni: [N] subscribers
- Total active: [N]
- Suppressed (excluded): [N]
- Final send list: [N]

## Per-Stage Overrides
[Table of CTA copy, CTA URL, and merge tokens per stage]

## Suppression Log
[counts by status type]
```

Confirm: "Segment config saved. Final send list: [N] subscribers across [N_stages] stages."

## Test Mode Fallback

In `test_mode=true`, never fail the whole step solely because the live audience
schema is incomplete, the query returns zero opted-in rows, or the relay table
lacks enough context for all three stages.

Instead:
- still write `memory/drafts/YYYY-MM-DD-[newsletter-type]-segment.md`
- include explicit notes about what was unavailable
- if there are zero eligible opted-in contacts, set `Final send list: 1 (TEST MODE override)`
- note that all routing is forced to `lumina.qa@agentmail.to`

Use this fallback shape when needed:

```
# Segment Config — [Type] — YYYY-MM-DD

## Send List Counts
- Inquiry: unknown or [N]
- Applied: unknown or [N]
- Alumni: unknown or [N]
- Total active: unknown or [N]
- Suppressed (excluded): unknown or [N]
- Final send list: 1 (TEST MODE override)

## Per-Stage Overrides
- TEST MODE override active: all recipient routing forced to `lumina.qa@agentmail.to`
- Live stage-based CTA overrides not fully applied in this run due source-data limitations

## Suppression Log
- TEST MODE: live suppression query unavailable or no eligible contacts returned
```

## Error Handling

- `DATABASE_URL` missing: stop, notify the operator — cannot segment without database access
- `psql` binary not found: stop, notify the operator
- Query returns 0 active subscribers:
  - in test mode: write the fallback segment config and continue
  - outside test mode: stop, notify the operator — do not proceed to brief or send
- Postgres connection refused: stop, notify the operator with connection error detail
- `lead_stage` is NULL for a contact: assign to Inquiry and log the count
- `relation "newsletter_subscribers" does not exist` or any other legacy-schema mismatch:
  - switch to `relay_contacts`
  - if the relay query still cannot produce a usable live send list and test mode is enabled, write the fallback segment config instead of stopping
