---
name: ab-test-execution
description: "Execute A/B test splits via MailChimp variate campaigns or Resend segment splits"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /ab-test-execution
metadata:
  openclaw:
    emoji: "🧪"
    requires:
      env:
        - MAILCHIMP_API_KEY
      bins:
        - curl
        - jq
        - python3
---

# A/B Test Execution

Bridges `ab-test-setup` (hypothesis design) to MailChimp/Resend (campaign
execution). Creates split campaigns, monitors results, declares winners,
and sends the winning variant to the remaining audience.

## When to Use

After `ab-test-setup` has produced a test plan with:
- Hypothesis (what you're testing)
- Variants (A vs B content)
- Metric (open_rate, click_rate, or revenue)
- Sample size and wait time

## Operations

### 1. Create Split — MailChimp Variate Campaign

Uses MailChimp's native variate (A/B) campaign type:

```yaml
# MailChimp Variate Campaign — API contract
# See mailchimp/SKILL.md A/B Testing section for executable patterns
endpoint: POST /3.0/campaigns
auth: Basic (derived from $MAILCHIMP_API_KEY)
body:
  type: variate
  recipients:
    list_id: $MAILCHIMP_LIST_ID
  variate_settings:
    winner_criteria: opens    # or clicks, total_revenue
    wait_time: 240            # minutes before declaring winner
    test_size: 20             # % of list for test
    subject_lines:
      - "Variant A subject line"
      - "Variant B subject line"
  settings:
    from_name: "Your Brand"
    reply_to: "info@example.org"
response:
  campaign_id: resp.id
```

### 2. Create Split — Resend Manual Segment

Resend has no native A/B support. The skill manually creates two equal-size
sub-segments:

```yaml
# Resend Manual Split — API contract
# See resend-broadcast/SKILL.md for executable patterns

# Step 1: Create two equal-size segments
- POST /segments { name: "{campaign_slug}-variant-a" } → seg_a_id
- POST /segments { name: "{campaign_slug}-variant-b" } → seg_b_id

# Step 2: Split contacts (round-robin by email hash)
# Assign 50% of audience contacts to each segment via:
# POST /contacts/{email}/segments/{seg_a_id}
# POST /contacts/{email}/segments/{seg_b_id}

# Step 3: Create two broadcast drafts with different subjects
- POST /broadcasts { segmentId: seg_a_id, subject: "Variant A", html: html_a, send: false }
- POST /broadcasts { segmentId: seg_b_id, subject: "Variant B", html: html_b, send: false }
```

### 3. Monitor Results

**MailChimp**: Poll variate campaign report:

```bash
curl -s "https://${DC}.api.mailchimp.com/3.0/reports/${CAMPAIGN_ID}" \
  -H "Authorization: Basic ${AUTH}" \
  | jq '{
    variant_a: .ab_split.a,
    variant_b: .ab_split.b,
    winner: .ab_split.winning_campaign_id
  }'
```

**Resend**: Compare domain-level stats between the two segments. Since Resend
doesn't provide per-broadcast analytics (only domain-level), this comparison
is approximate.

### 4. Declare Winner

Apply decision criteria from `ab-test-setup`:
- 90%+ confidence: strong signal → send winner to remaining
- 80-90%: directional signal → recommend winner, operator confirms
- <80%: inconclusive → operator decides

### 5. Send Winner to Remaining

**ClawWrap required.** The winning variant is sent to the remaining audience
(80% of list for MailChimp auto-winner, or the un-tested segment for Resend)
via `outbound.submit`:

```
outbound.submit(
    context_key="acme-webinar",
    audience="full-list",
    channel="mailchimp",
    payload={
        "subject": winning_subject,
        "html": winning_html,
        "campaign_id": winning_campaign_id
    }
)
```

## Pipeline State

The skill writes A/B test state to the pipeline:

```yaml
ab_test:
  enabled: true
  type: subject_line
  provider: mailchimp
  campaign_id: "abc123"
  variant_a_id: "var_a_id"
  variant_b_id: "var_b_id"
  metric: open_rate
  test_size: 20
  wait_time_minutes: 240
  status: monitoring  # created | monitoring | decided | sent
  winner: null        # "a" or "b" after decision
  results:
    variant_a: { opens: 0, clicks: 0 }
    variant_b: { opens: 0, clicks: 0 }
```

## Lobster Integration

Replaces `mailchimp-upload` when A/B is enabled:

```yaml
# In campaign-webinar.lobster:
- id: ab-test-create
  command: scripts/lobster-ab-test-create.sh ${pipeline_id}
  condition: $approval.approved && ${ab_test_enabled}

# In post-webinar-event.lobster (or via heartbeat):
- id: ab-test-monitor
  command: scripts/lobster-ab-test-monitor.sh ${pipeline_id}
```

## Related Skills

- `ab-test-setup` — hypothesis design, sample size calculation, analysis framework
- `mailchimp` v1.1.0 — variate campaign API patterns (lines 1071-1127)
- `resend-broadcast` — segment creation for manual splits
- `campaign-calendar` — conflict detection for split sends
- `campaign-analytics` — post-test performance reporting
