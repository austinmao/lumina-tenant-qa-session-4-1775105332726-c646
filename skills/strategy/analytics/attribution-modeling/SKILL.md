---
name: attribution-modeling
description: "Build multi-touch attribution models and allocate credit across marketing channels"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /attribution-modeling
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Attribution Modeling

Build multi-touch attribution models to allocate conversion credit across marketing channels, analyze the customer journey, and produce actionable channel performance reports. This skill helps answer the question: "Which marketing touchpoints are actually driving conversions?"

## When to Use

- Setting up attribution logic for a new tenant or campaign
- Evaluating which channels deserve budget allocation
- Analyzing the customer journey from first touch to conversion
- Comparing attribution models to understand channel contribution
- Creating attribution reports for campaign performance review
- Troubleshooting attribution discrepancies between platforms

## Context Loading

Before any attribution work:
1. Read `tenants/<tenant>/config.yaml` for active marketing channels
2. Read the event taxonomy document for conversion event definitions
3. Read campaign configuration for active UTM parameters and channel mapping
4. Read existing attribution reports in `memory/logs/analytics/` for historical baselines
5. Identify all touchpoint sources: organic search, paid search, social, email, SMS, direct, referral

## Attribution Models

### Last-Touch Attribution

```
100% credit → last touchpoint before conversion
```

**When to use**: simple reporting, short sales cycles, single-channel campaigns
**Limitation**: ignores all awareness and consideration touchpoints
**Best for**: direct response campaigns where the last click is genuinely the driver

### First-Touch Attribution

```
100% credit → first touchpoint in the journey
```

**When to use**: measuring awareness channel effectiveness
**Limitation**: ignores nurture and conversion touchpoints
**Best for**: understanding which channels are best at attracting new audiences

### Linear Attribution

```
Equal credit → every touchpoint in the journey
```

**When to use**: balanced view of the full funnel
**Limitation**: treats a casual blog visit the same as a booking page visit
**Best for**: early-stage attribution when you do not yet know which touchpoints matter most

### Time-Decay Attribution

```
More credit → touchpoints closer to conversion
Decay function: exponential with configurable half-life
```

**When to use**: longer sales cycles where recent interactions are more influential
**Configuration**: half-life of 7 days (default) -- touchpoints 7 days before conversion get 50% weight, 14 days gets 25%, etc.
**Best for**: high-consideration purchases (retreats, courses, services)

### Position-Based (U-Shaped) Attribution

```
40% credit → first touchpoint
40% credit → last touchpoint
20% credit → divided among middle touchpoints
```

**When to use**: valuing both awareness and conversion while acknowledging the middle funnel
**Best for**: multi-channel campaigns with distinct awareness and conversion phases

### Data-Driven Attribution

```
Statistical model assigns credit based on observed conversion patterns
```

**Requirements**: sufficient data volume (minimum 300 conversions per month recommended)
**Implementation**: compare paths that convert vs paths that do not -- touchpoints that appear disproportionately in converting paths get more credit
**Best for**: mature tracking setups with high data volume

## Channel Definitions

### Channel Mapping

Map incoming traffic to channels using UTM parameters and referrer data:

| Channel | UTM Source/Medium | Referrer Pattern |
|---|---|---|
| Organic Search | (not set) / organic | google.com, bing.com, duckduckgo.com |
| Paid Search | google / cpc, bing / cpc | (UTM-based, not referrer) |
| Social Organic | instagram / social, linkedin / social | instagram.com, linkedin.com |
| Social Paid | meta / paid-social, linkedin / paid-social | (UTM-based) |
| Email | resend / email, newsletter / email | (UTM-based) |
| SMS | twilio / sms | (UTM-based) |
| Direct | (direct) / (none) | No referrer |
| Referral | partner-name / referral | partner-domain.com |

### Channel Grouping Rules

1. UTM parameters take precedence over referrer data
2. If UTM is present but malformed, log the issue and fall back to referrer
3. Direct traffic with a landing page deep in the site is likely misattributed -- check for tracking gaps
4. Self-referrals (the site referring to itself) indicate cross-domain tracking issues

## Customer Journey Analysis

### Journey Reconstruction

Build the customer journey from touchpoint data:

```
Journey: [First Touch] → [Touchpoint 2] → ... → [Conversion]
Example: Organic Search (blog post) → Email (newsletter) → Direct (pricing page) → Paid Social (retargeting ad) → Direct (booking page) → Conversion
```

For each journey, capture:
- Touchpoints (channel, specific source, landing page)
- Timestamps (days between touchpoints, total journey duration)
- Engagement depth per touchpoint (page views, time on site)

### Journey Metrics

| Metric | Definition | Why It Matters |
|---|---|---|
| Average touchpoints to conversion | Mean number of touches before converting | Channel planning complexity |
| Average journey duration | Days from first touch to conversion | Sales cycle length |
| Most common first touch | Channel that initiates the most journeys | Awareness channel |
| Most common last touch | Channel that closes the most journeys | Conversion channel |
| Most common path | The journey sequence that appears most often | Optimize the proven path |
| Assisted conversions | Conversions where a channel appeared but was not last touch | Channel contribution beyond direct |

### Assisted vs Direct Conversions

A channel's true value is: direct conversions + assist value.

```
Assist ratio = Assisted conversions / Direct (last-touch) conversions

High assist ratio (>1): channel is a strong assister (awareness/nurture role)
Low assist ratio (<0.5): channel is a strong closer (conversion role)
Balanced (~1): channel contributes evenly
```

## Report Format

### Channel Performance Report

```markdown
## Attribution Report — [Period]

### Model: [Attribution Model Used]

| Channel | Attributed Conversions | Revenue Credit | Cost | ROAS | Assist Ratio |
|---|---|---|---|---|---|
| Organic Search | [n] | $[amount] | $[cost] | [ratio] | [ratio] |
| Paid Social | [n] | $[amount] | $[cost] | [ratio] | [ratio] |
| Email | [n] | $[amount] | $[cost] | [ratio] | [ratio] |
| SMS | [n] | $[amount] | $[cost] | [ratio] | [ratio] |
| Direct | [n] | $[amount] | $0 | N/A | [ratio] |

### Model Comparison

| Channel | Last Touch | First Touch | Linear | Time Decay | Position Based |
|---|---|---|---|---|---|
| Organic Search | [n] | [n] | [n] | [n] | [n] |
| Paid Social | [n] | [n] | [n] | [n] | [n] |
| ... | ... | ... | ... | ... | ... |

### Key Insights
1. [Insight about which channels are over/under-valued by last-touch]
2. [Insight about journey patterns]
3. [Recommendation for budget allocation]

### Journey Summary
- Average touchpoints: [n]
- Average journey duration: [n] days
- Most common first touch: [channel]
- Most common conversion path: [path]
```

## Implementation Approach

### Data Collection

Attribution requires clean touchpoint data:
1. **UTM discipline**: every paid link must have utm_source, utm_medium, utm_campaign
2. **First-party cookies**: store the first touch UTM parameters in a first-party cookie
3. **Session stitching**: connect anonymous sessions to identified users on conversion
4. **Cross-device**: use hashed email or user ID for cross-device journey reconstruction

### Storage

Store touchpoint data in a structured table:

```sql
CREATE TABLE touchpoints (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  visitor_id TEXT NOT NULL,          -- first-party cookie ID
  user_id UUID,                       -- set on conversion/identification
  channel TEXT NOT NULL,
  source TEXT,
  medium TEXT,
  campaign TEXT,
  landing_page TEXT,
  timestamp TIMESTAMPTZ NOT NULL,
  session_duration INTEGER,
  page_views INTEGER,
  converted BOOLEAN DEFAULT false,
  conversion_value NUMERIC(12,2)
);
```

### Attribution Calculation

Run attribution calculations on a schedule (daily) or on-demand:
1. Query all touchpoints for users who converted in the period
2. Group touchpoints into journeys (ordered by timestamp)
3. Apply the selected attribution model to allocate credit
4. Aggregate credit by channel for reporting

## Common Pitfalls

- **Attribution window too short**: if the journey takes 30 days but the window is 7 days, most touchpoints are missed. Set the window to 1.5x the average journey duration.
- **Ignoring view-through conversions**: users who saw but did not click an ad may still convert later. Consider view-through attribution for display and video campaigns (typically 1-day window).
- **Direct traffic overcount**: much "direct" traffic is actually misattributed (dark social, email clients that strip referrers, bookmarks). Look for patterns in direct traffic landing pages.
- **Platform disagreement**: Google and Meta will each claim credit for the same conversion. Use a single source of truth (your own attribution system) and compare.
- **Sample size**: do not make attribution conclusions from fewer than 100 conversions. Signal is too noisy.

## Error Handling

- Missing UTM parameters on paid traffic: flag the campaign for UTM correction, attribute as "untagged paid" to preserve channel visibility
- Cookie blocked by browser: fall back to server-side session tracking where possible
- Journey data gaps (missing touchpoints): note the gap in the report, do not fabricate touchpoints
- Platform API data discrepancy: use your first-party data as the source of truth, note the discrepancy

## Boundaries

- Never fabricate attribution data or fill gaps with assumptions
- Never use attribution to prove a predetermined conclusion -- present all models and let the data speak
- Never include PII in attribution reports (aggregate data only)
- Never change attribution models mid-campaign without documenting the reason and restating historical baselines

## Dependencies

- `conversion-tracking` -- conversion events that feed the attribution model
- `event-taxonomy` -- event naming conventions for consistent data
- `analytics-tracking` -- GA4 configuration and data collection
- `dashboard-building` -- visualization of attribution reports

## State Tracking

- `models` -- keyed by model name: configuration, last run, conversion count, date range
- `channels` -- keyed by channel name: attributed conversions, revenue, cost, ROAS, assist ratio
- `journeys` -- summary statistics: average length, average duration, common paths
