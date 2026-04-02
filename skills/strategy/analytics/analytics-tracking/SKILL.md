---
name: analytics-tracking
description: >
  Set up GA4 tracking, event taxonomy, UTM strategy, and GEO measurement for
  marketing funnels. Use when the operator asks to configure analytics, create a
  tracking plan, define event naming, set up conversion tracking, build UTM
  conventions, audit existing GA4 setup, or measure AI search referral traffic.
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /analytics-tracking
metadata:
  openclaw:
    emoji: "chart"
    requires:
      bins: []
      env: []
---

# Analytics Tracking

## Overview

Set up and maintain analytics tracking for the organization's education-to-experience
funnels (free offer, webinar, paid program, retreat). This skill produces event
taxonomies, GA4 configuration guidance, GTM implementation patterns, UTM naming
conventions, GEO measurement plans, and tracking plan documents.

## Core Principle

**Track for decisions, not data.** Every event must answer a specific question.
Before adding any event, state the question it answers and the action you will
take when the number changes. If you cannot name both, do not track it.

---

## Event Naming Convention

Use **object_action** format. Lowercase. Underscores only. No spaces or special
characters.

```
quiz_started
webinar_registered
enrollment_completed
referral_shared
```

Rules:
- Object first, then past-tense verb: `call_booked`, not `booked_call`
- Context goes in event parameters, not the event name
- Be specific enough to distinguish: `guide_downloaded` not `download_clicked`
- Document every event before implementation

---

## the organization Event Taxonomy

Organized by funnel stage. Each event includes required parameters.

### DISCOVER Stage

| Event | Parameters | Question It Answers |
|-------|-----------|---------------------|
| `page_viewed` | `content_type` (hub, comparison, blog, guide), `page_path` | Which content types attract visitors? |
| `organic_landed` | `landing_page`, `search_query` (if available) | What organic searches lead people to us? |
| `ai_search_referred` | `ai_engine` (perplexity, chatgpt, google_ai_overview), `landing_page` | How much traffic comes from AI search engines? |
| `scroll_depth_reached` | `percent` (25, 50, 75, 100), `page_path` | Are visitors reading our content or bouncing early? |

### ENGAGE Stage

| Event | Parameters | Question It Answers |
|-------|-----------|---------------------|
| `quiz_started` | `quiz_name` | Are visitors engaging with our assessment tools? |
| `quiz_completed` | `quiz_name`, `result_segment` | What segments do our prospects fall into? |
| `guide_downloaded` | `guide_name`, `page_path` | Which lead magnets convert best? |
| `webinar_registered` | `webinar_slug`, `source` | What drives webinar signups? |
| `webinar_attended` | `webinar_slug`, `duration_minutes` | What share of registrants actually show up? |
| `webinar_replay_viewed` | `webinar_slug` | How many watch the replay vs live? |
| `webinar_replay_duration` | `webinar_slug`, `seconds_watched`, `percent_watched` | How far into the replay do viewers get? |

### CONVERT Stage

| Event | Parameters | Question It Answers |
|-------|-----------|---------------------|
| `enrollment_started` | `program_name` | Where in the enrollment form do people drop off? |
| `enrollment_completed` | `program_name`, `value` | What is our enrollment conversion rate by program? |
| `call_booked` | `call_type` | Are prospects booking discovery calls? |
| `call_completed` | `call_type`, `outcome` | What share of calls lead to enrollment? |
| `application_started` | `program_name` | How many begin applications? |
| `application_submitted` | `program_name` | What is the application completion rate? |

### DEEPEN Stage

| Event | Parameters | Question It Answers |
|-------|-----------|---------------------|
| `module_completed` | `program_name`, `module_name` | Are participants completing the curriculum? |
| `retreat_confirmed` | `retreat_name`, `retreat_date` | Retreat seat fill rate tracking. |
| `survey_completed` | `survey_type` | Post-program feedback collection rate. |
| `referral_shared` | `channel` (email, social, direct) | Are participants sharing with others? |
| `referral_converted` | `referrer_id` | Which referral channels produce enrollments? |

---

## GA4 Setup Guidance

### Core Configuration

1. Create one web data stream for [the organization's domain]
2. Enable Enhanced Measurement (page_view, scroll, outbound_click, site_search, file_download)
3. Set data retention to 14 months (maximum for free GA4)
4. Enable Google Signals for cross-device (only if consent is collected)
5. Link Google Ads account if running paid campaigns

### Custom Dimensions

Create these in Admin > Custom Definitions:

| Dimension Name | Scope | Parameter Name | Purpose |
|---------------|-------|---------------|---------|
| Content Type | Event | `content_type` | Segment page_viewed by hub/blog/guide/comparison |
| Quiz Result Segment | Event | `result_segment` | Segment quiz completions by outcome |
| AI Engine | Event | `ai_engine` | Identify which AI search engines refer traffic |
| Program Name | Event | `program_name` | Segment conversion events by program |
| Webinar Slug | Event | `webinar_slug` | Tie engagement events to specific webinars |

### Conversion Events

Mark these events as conversions in GA4 Admin > Events:

- `quiz_completed` — lead qualification signal
- `webinar_registered` — top-of-funnel conversion
- `enrollment_completed` — revenue event (set value parameter)
- `call_booked` — sales pipeline entry
- `application_submitted` — program pipeline entry
- `referral_converted` — viral loop signal

Set counting to "Once per session" for all except `enrollment_completed` (count every occurrence).

---

## GTM Implementation Patterns

### Container Structure

Organize GTM with folders by funnel stage:

- **Folder: Discover** — tags/triggers for page_viewed, organic_landed, ai_search_referred
- **Folder: Engage** — tags/triggers for quiz, guide, webinar events
- **Folder: Convert** — tags/triggers for enrollment, call, application events
- **Folder: Deepen** — tags/triggers for module, retreat, survey, referral events

### Tag/Trigger/Variable Pattern

For each custom event:

1. **Data Layer push** — site code pushes event to dataLayer
   ```javascript
   dataLayer.push({
     'event': 'webinar_registered',
     'webinar_slug': 'have-a-good-trip',
     'source': 'homepage_hero'
   });
   ```
2. **Custom Event trigger** — GTM trigger listens for the event name
3. **GA4 Event tag** — fires on that trigger, maps data layer variables to GA4 parameters

### Naming Convention for GTM

- Tags: `GA4 - [event_name]` (e.g., `GA4 - webinar_registered`)
- Triggers: `CE - [event_name]` (e.g., `CE - webinar_registered`)
- Variables: `DLV - [variable_name]` (e.g., `DLV - webinar_slug`)

Always use Preview Mode to validate before publishing. Add version notes on every publish.

---

## UTM Naming Conventions

### Parameter Definitions

| Parameter | Rule | Examples |
|-----------|------|---------|
| `utm_source` | Platform or sender name, lowercase | `google`, `facebook`, `instagram`, `newsletter`, `perplexity` |
| `utm_medium` | Channel type, lowercase | `cpc`, `email`, `social`, `organic_social`, `referral`, `ai_search` |
| `utm_campaign` | Campaign identifier: `YYYY-MM_description` | `2026-03_spring-retreat`, `2026-04_webinar-launch` |
| `utm_content` | Creative or placement variant | `hero_cta`, `sidebar_banner`, `email_header_link` |
| `utm_term` | Paid search keyword (paid only) | `psychedelic+retreat`, `healing+ceremony` |

### Rules

- All lowercase, always
- Use hyphens within words, underscores between fields
- Campaign names always start with `YYYY-MM_`
- Never reuse campaign names across different campaigns
- Document every UTM combination in a shared spreadsheet before use

### Examples

```
# Newsletter link to webinar registration
?utm_source=newsletter&utm_medium=email&utm_campaign=2026-03_spring-retreat&utm_content=header_cta

# Instagram bio link
?utm_source=instagram&utm_medium=organic_social&utm_campaign=2026-03_spring-retreat&utm_content=bio_link

# Google Ads
?utm_source=google&utm_medium=cpc&utm_campaign=2026-03_spring-retreat&utm_term=healing+retreat

# AI search referral (manual tagging for content you control)
?utm_source=perplexity&utm_medium=ai_search&utm_campaign=2026-03_geo-content
```

---

## GEO-Specific Tracking

### Why This Matters

Generative Engine Optimization (GEO) is a priority for the organization. AI search engines
(Perplexity, ChatGPT Browse, Google AI Overviews) increasingly refer traffic.
Measuring this traffic separately from traditional organic is essential to understand
whether GEO efforts are working.

### Identifying AI Search Referrers

Detect AI engine referrals by matching the `document.referrer` string. Known patterns:

| AI Engine | Referrer String Contains | `ai_engine` Value |
|-----------|-------------------------|-------------------|
| Perplexity | `perplexity.ai` | `perplexity` |
| ChatGPT Browse | `chatgpt.com` or `chat.openai.com` | `chatgpt` |
| Google AI Overview | Referrer is `google.com` BUT landing page has no standard search query param; often arrives with `utm_source=google` and no `utm_term` | `google_ai_overview` |
| Bing Copilot | `bing.com` with `/chat` in referrer path | `bing_copilot` |
| Claude | `claude.ai` | `claude` |

Implementation approach:
1. In GTM, create a Custom JavaScript Variable that reads `document.referrer`
2. Use a Lookup Table variable to map referrer patterns to `ai_engine` values
3. Fire `ai_search_referred` event when an AI referrer is detected on landing
4. Pass the `ai_engine` value and `landing_page` as event parameters

### AI Search Share Trend Metric

Track this monthly: **AI Search Share = (sessions from AI search referrers / total organic sessions) x 100**

- Pull from GA4 Explore: filter sessions where `ai_engine` is not empty, compare to total organic
- Chart month-over-month to see GEO impact trending up or down
- If AI search share is growing, GEO content strategy is working
- If flat or declining, review content structure (FAQ schema, citation-friendly formatting, entity clarity)

### UTM Convention for AI-Referred Traffic

When linking from content you control that is likely to be cited by AI engines:
- `utm_medium=ai_search` (distinct from `organic` or `cpc`)
- `utm_source` = the engine name when known, or `ai_generic` as fallback

---

## Attribution Model

### Multi-Touch with First + Last Emphasis

the organization's consideration cycle is long (weeks to months). A prospect may:
1. Discover via AI search or blog post (first touch)
2. Attend a webinar (middle touch)
3. Download a guide (middle touch)
4. Book a call weeks later (last touch)
5. Enroll after the call

**First touch** reveals what channels bring people in. **Last touch** reveals what
triggers the conversion decision. **Middle touches** build trust and are critical
but inherently hard to attribute precisely.

### Practical Guidance

- Use GA4's default data-driven attribution for Google Ads reporting
- For internal analysis, pull first-touch and last-touch reports separately
- Do not over-invest in complex multi-touch attribution modeling at current scale
- Focus on: "What channels bring qualified people in?" and "What triggers the final conversion?"
- Accept that middle-touch attribution will be imprecise; measure engagement depth (webinar attendance rate, replay watch duration, guide downloads) as proxy signals

---

## Privacy Rules

the organization operates in the psychedelic healing space. Strict privacy boundaries apply.

- **No medical data in analytics events.** Never track health conditions, diagnoses, medication use, or treatment details as event parameters.
- **No PII in GA4.** No names, email addresses, phone numbers, or physical addresses in event parameters or custom dimensions. Use opaque user IDs only.
- **No substance-related behavioral data.** Do not create events or parameters that could reveal an individual's substance use history or intentions.
- **Quiz answers stay aggregate.** Track `result_segment` (the outcome category), never individual question answers.
- **Consent before tracking.** Implement cookie consent banner. Fire GA4 tags only after consent is granted. Use GA4 Consent Mode for modeling unconsented sessions.
- **Data retention.** Set GA4 retention to 14 months maximum. Do not export raw user-level data to external systems without legal review.

---

## Debugging Approach

### Before Launch

1. Enable GA4 DebugView (`?debug_mode=true` or GA Debugger Chrome extension)
2. Use GTM Preview Mode to verify each tag fires on its intended trigger
3. Check that all event parameters populate with correct values (not undefined or empty)
4. Confirm conversion events register in GA4 Admin > Events > marked as conversion
5. Validate UTM parameters parse correctly in GA4 Traffic Acquisition report

### Validation Checklist

- [ ] Every taxonomy event fires on the correct user action
- [ ] All parameters populate with expected values (check DebugView)
- [ ] No duplicate events (check for multiple GTM containers or double-firing triggers)
- [ ] AI search referrer detection works for Perplexity, ChatGPT, Google AI Overview
- [ ] Consent mode blocks tags until user grants consent
- [ ] No PII appears in any event parameter
- [ ] Events work on both desktop and mobile

### Common Issues

- **Event not appearing in GA4**: Tag paused in GTM, trigger misconfigured, or GTM container not loaded on the page
- **Parameter showing as "(not set)"**: Data layer variable name mismatch between push and GTM variable config
- **Duplicate events**: Multiple GTM containers on the same page, or trigger firing on both Click and DOM Ready
- **AI referrer not detected**: Referrer string pattern changed; update the Lookup Table variable

---

## Tracking Plan Template

When creating or auditing a tracking plan, produce a document in this format:

```
# the organization Tracking Plan

## Meta
- GA4 Property: [property ID]
- GTM Container: [container ID]
- Last updated: [date]
- Owner: [name]

## Event Taxonomy
[Table: Event Name | Stage | Parameters | Trigger | Conversion? | Question Answered]

## Custom Dimensions
[Table: Name | Scope | Parameter | Purpose]

## Conversion Events
[Table: Event | Counting Method | Linked to Ads?]

## UTM Conventions
[Source/medium/campaign naming rules with examples]

## GEO Measurement
- AI referrer detection method
- AI search share baseline: [current %]
- Monthly trend: [chart or table]

## Privacy Boundaries
- Events excluded for privacy: [list]
- Consent implementation: [method]

## Debugging Notes
- DebugView access: [who has it]
- GTM Preview: [last validated date]
```

---

## Steps

1. **Assess current state**: Ask what tracking exists today (GA4 property? GTM container? Any custom events?). Identify gaps against the taxonomy above.
2. **Define priority events**: Select events from the taxonomy based on the current funnel stage being built or optimized. Do not implement all events at once — start with the stage that needs measurement most.
3. **Produce tracking plan**: Generate a tracking plan document using the template above, filling in all sections relevant to the selected events.
4. **Specify GTM implementation**: For each event, write the exact data layer push, trigger configuration, and GA4 Event tag setup. Use the naming conventions defined above.
5. **Define UTM conventions**: If not already established, produce the UTM naming guide with examples for all active channels.
6. **Set up GEO measurement**: Configure AI search referrer detection per the GEO section. Establish the AI search share baseline.
7. **Validate**: Walk through the debugging checklist. Confirm no PII or prohibited data in any event.
8. **Document**: Deliver the complete tracking plan to the operator for review.

## Output

Deliver one of:
- A **tracking plan document** (using the template above) when setting up or auditing analytics
- A **GTM implementation spec** (data layer pushes + tag/trigger/variable configs) when implementing events
- A **UTM guide** (naming conventions + channel examples) when establishing UTM strategy
- A **GEO measurement report** (AI search share trend + referrer detection status) when reviewing GEO performance

Always state which events were added or changed, and confirm that no privacy rules were violated.

## Error Handling

- If GA4 property ID is unknown: ask the operator before proceeding
- If GTM container access is unavailable: produce the tracking plan and data layer specs; flag that GTM implementation requires container access
- If a requested event would capture PII or medical data: refuse, explain the privacy rule, and suggest an aggregate alternative
- If AI referrer patterns have changed (new engines or updated domains): note the gap and recommend updating the GTM Lookup Table variable
