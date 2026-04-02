---
name: offer-api
description: Use when creating or refining an offer record (price, guarantee, bonuses) via the API before an anchored campaign can be created
version: "2.0.0"
author: "your-org"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /create-offer
metadata:
  openclaw:
    emoji: "💸"
    requires:
      bins: ["bash", "curl"]
      env: ["CAMPAIGN_API_KEY", "CAMPAIGN_API_ENDPOINT"]
      os: ["darwin"]
---

# Offer API

This skill produces an `offers` record, not a campaign.

Use it when the operator has the commercial offer concept but no structured `offer_id` yet.

## Collect

Ask for:

```text
1. title
2. slug
3. description
4. actual_price
5. anchor_price (optional)
6. guarantee_type (optional)
7. urgency_type (optional)
8. urgency_deadline (optional)
9. order_form_url or checkout_url (optional)
10. bonuses (optional)
```

## Create

POST the offer:

```bash
curl -s -X POST "$CAMPAIGN_API_ENDPOINT/api/offers" \
  -H "Authorization: Bearer $CAMPAIGN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<title>",
    "slug": "<slug>",
    "description": "<description>",
    "actual_price": 997,
    "anchor_price": 1997,
    "guarantee_type": "<guarantee_type_or_none>",
    "urgency_type": "<urgency_type_or_null>",
    "urgency_deadline": "<urgency_deadline_or_null>",
    "order_form_url": "<order_form_url_or_null>",
    "checkout_url": "<checkout_url_or_null>",
    "bonuses": []
  }'
```

## Verify

- Capture `offer.id`
- Confirm detail loads through `GET /api/offers/<offer_id>`
- Hand off the resulting `offer_id` to `campaign-api`

## Test Mode Audit

In `test_mode=true`, always append an audit record to
`memory/logs/api-submits/YYYY-MM-DD.md` even if the external API call is skipped,
mocked, or blocked by missing credentials.

Record this shape:

```text
[TIMESTAMP] offer_api
offer_id: <returned id or off_test_<slug>>
slug: <slug>
actual_price: <actual_price>
approval_status: draft
test_mode: true
```

Use the real `offer.id` when the API returns one. Otherwise write the fallback id
derived from the slug so the audit trail remains deterministic in test mode.

## Guardrails

- Reuse an existing `offer_id` when the offer already exists.
- Keep bonuses ordered deliberately; they render in `sort_order`.
