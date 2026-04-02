---
name: review-campaign
description: "Review, audit, or update an existing campaign in the DB"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /review-campaign
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      env: ["CAMPAIGN_API_KEY"]
      bins: ["curl", "jq"]
---

# Review Campaign Skill

Trigger: `/review-campaign [campaign-id-or-title]`

## What This Skill Does

Retrieves an existing campaign from the DB, audits all assets against the current brand and copy standards, identifies gaps, and stages proposed updates for approval before PATCHing.

## Orchestration Sequence

**Step 1 — Fetch campaign**
```bash
curl -s -H "Authorization: Bearer ${CAMPAIGN_API_KEY}" \
  https://admin.[the organization's domain]/api/campaigns/${CAMPAIGN_ID} | jq '.'
```
Record: campaign title, type, status, asset inventory (categories + slugs present).

**Step 2 — Identify gaps**

Compare fetched assets against expected asset set for the campaign type:

| Campaign Type | Expected Assets |
|---|---|
| webinar | email_transactional (r-e1 through r-e8/r-e6b), email_marketing (L-E1 through L-E5), website (landing page), sms_broadcast |
| retreat | email_marketing, website, sms_broadcast |
| workshop | email_marketing, website |
| newsletter | email_newsletter |

List each missing slug explicitly: "Missing: r-e3-day-before (email_transactional)"

**Step 3 — Brand + copy audit**

For each existing asset with content:
- Run content through `marketing/brand-standards` skill check
- Flag: off-brand language, missing CTAs, incorrect tone, outdated dates/capacity

**Step 4 — Draft updates**

For each gap or flagged asset:
- Generate revised copy (delegate to Quill/Lumina for full assets; generate directly for SMS/thank-you)
- For missing assets, generate full content per asset type
- Stage all proposed changes in `memory/campaigns/review-YYYY-MM-DD-[slug].md`

**Step 5 — Post preview to Slack**

Post to `#lumina-bot`:
```
CAMPAIGN REVIEW: [Title] (ID: [id])

GAPS ([n] missing):
• [asset_slug] — [category] — proposed content attached

REVISIONS ([n] flagged):
• [asset_slug] — issue: [description] — revision attached

[Approve All] [Edit] [Cancel]
```

**Step 6 — On approval: PATCH each updated asset**
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer ${CAMPAIGN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"asset_category":"[cat]","asset_slug":"[slug]","content":"[content]","label":"[label]","subject":"[subject]"}' \
  https://admin.[the organization's domain]/api/campaigns/${CAMPAIGN_ID}/assets | jq '.'
```

**Step 7 — For new assets (not existing slugs): POST**
```bash
curl -s -X POST \
  -H "Authorization: Bearer ${CAMPAIGN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"asset_category":"[cat]","asset_slug":"[slug]","label":"[label]","content":"[content]","subject":"[subject]","sequence_order":[n]}' \
  https://admin.[the organization's domain]/api/campaigns/${CAMPAIGN_ID}/assets | jq '.'
```

**Step 8 — Verify**
```bash
curl -s -H "Authorization: Bearer ${CAMPAIGN_API_KEY}" \
  https://admin.[the organization's domain]/api/campaigns/${CAMPAIGN_ID} | jq '.assets | keys'
```
Confirm all expected slugs present.

**Step 9 — Audit log**
Write review summary to `memory/logs/api-submits/YYYY-MM-DD.md`:
- Campaign ID + title
- Assets reviewed, gaps filled, revisions made
- Approval timestamp

## Campaign Type Correction

If the campaign's `campaign_type` is wrong (e.g., "retreat" when it should be "webinar"),
notify the operator. The type field requires direct DB update — the API only updates status:
```
CAMPAIGN_TYPE MISMATCH: Campaign ID [n] has type=[current] but should be type=[expected].
Requires: psql UPDATE campaigns SET campaign_type='webinar'::campaign_type WHERE id=[n];
```

## Boundaries

- I do not PATCH assets without explicit the operator approval for that session
- I do not delete assets — only add or update via new version
- I do not update campaign status — only assets
- I report gaps but do not auto-fill without approval
