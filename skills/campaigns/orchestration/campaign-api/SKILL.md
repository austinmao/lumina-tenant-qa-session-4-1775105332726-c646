---
name: campaign-api
description: Use when creating an anchored campaign record via the API — connects an event and/or offer to campaign assets and schedule metadata
version: "2.0.0"
author: "your-org"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /create-campaign-full
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: ["bash", "curl", "jq", "pnpm"]
      env: ["CAMPAIGN_API_KEY", "CAMPAIGN_API_ENDPOINT"]
      os: ["darwin"]
---

# Campaign API

Create a campaign record only after at least one anchor exists.

Campaign execution in v2 is anchor-first:
- `events` hold the live occurrence and public slug
- `offers` hold the commercial object
- `campaigns` attach execution to one or both
- `campaign_assets.approval_status = approved` is the execution authorization gate
- `campaign_schedule` is the operator-facing schedule template layer

Do not send anything from this skill. This skill creates and links records, generates draft assets, and leaves approval/sending to later flows.

## Required Inputs

Collect these before calling the API:

```text
1. campaign_type: webinar | retreat | workshop | newsletter
2. campaign title
3. campaign topic
4. event_id (optional only if offer_id exists)
5. offer_id (optional only if event_id exists)
6. whether to generate MVP email assets now
```

If both `event_id` and `offer_id` are missing, stop. The API rejects unanchored campaign creation.

## Step 1: Confirm Anchors

- If the operator does not yet have an event, use `event-api` first.
- If the operator does not yet have an offer, use `offer-api` first.
- Reuse existing ids when possible. Do not create duplicates casually.

## Step 2: Create The Campaign

Use the campaign API with anchors included:

```bash
curl -s -X POST "$CAMPAIGN_API_ENDPOINT/api/campaigns" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<title>",
    "topic": "<topic>",
    "campaign_type": "<type>",
    "event_id": "<event_id_or_null>",
    "offer_id": "<offer_id_or_null>",
    "config": {}
  }'
```

Expected behavior:
- identical `title + campaign_type + event_id + offer_id` returns the existing campaign
- different anchors create a new campaign even if title/type match another campaign

Capture `campaign.id` and save it in your working notes.

## Step 3: Inspect The Anchored Campaign

Load the enriched detail payload:

```bash
curl -s "$CAMPAIGN_API_ENDPOINT/api/campaigns/<campaign_id>" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY"
```

Verify:
- `campaign.event_id` and/or `campaign.offer_id` are present
- `event` is returned when event-linked
- `offer` is returned when offer-linked
- `schedule` may be empty before generation

If anchors are wrong, stop and fix the source records before generating assets.

## Step 4: Generate MVP Assets

For the current MVP implementation, the email render entrypoint is:

```bash
cd /Users/operator/Documents/GitHub/openclaw-tenant/web
pnpm exec tsx --tsconfig tsconfig.scripts.json --env-file=.env.local scripts/render-and-patch-emails.ts
```

Current behavior:
- writes draft asset revisions through `createCampaignAsset`
- stores structured `send_offset` / `send_segment` on broadcast-capable assets
- persists future broadcast schedule rows when the campaign has a linked event

Do not assume this script is generic across all campaigns. Confirm the template set matches the campaign you are operating on before running it.

## Step 5: Verify Asset And Schedule State

After generation:

```bash
curl -s "$CAMPAIGN_API_ENDPOINT/api/campaigns/<campaign_id>" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY"

curl -s "$CAMPAIGN_API_ENDPOINT/api/campaigns/<campaign_id>/schedule" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY"
```

Check:
- website, email, and/or SMS assets exist as expected for the campaign
- new assets default to `approval_status: "draft"`
- broadcast schedule rows exist only for future broadcast assets

If schedule rows are missing and the campaign has no linked event, that is expected.

## Step 6: Approval Discipline

Do not mark generated copy as ready to send.

Rules:
- `approval_status = draft` is the default and should remain so until reviewed
- approval is per asset revision, not per campaign
- this skill does not send email or SMS

## Test Mode Audit

In `test_mode=true`, always append an audit record to
`memory/logs/api-submits/YYYY-MM-DD.md` even if the campaign API call is skipped,
mocked, or blocked by missing credentials.

Record this shape:

```text
[TIMESTAMP] campaign_api
campaign_id: <returned id or cmp_test_<slug>>
campaign_type: <type>
event_id: <event_id_or_null>
offer_id: <offer_id_or_null>
approval_status: draft
send_offset: pending
test_mode: true
```

If the live API returns a campaign id, use it. Otherwise derive a deterministic
fallback id from the campaign title/topic slug so the smoke run still leaves the
expected audit trail in test mode.

## Common Mistakes

- Creating a campaign without anchors. The API rejects this.
- Reusing a title/type pair with different anchors and assuming it will dedupe. It should not.
- Treating `campaign_schedule` as a recipient-level delivery queue. It is only the template timeline in this MVP.
- Assuming every asset category should be scheduled. Only future broadcast assets become schedule rows automatically.
