---
name: event-taxonomy
description: "Define event naming conventions, data layer design, and taxonomy documentation"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /event-taxonomy
metadata:
  openclaw:
    emoji: "🏷️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Event Taxonomy

Define event naming conventions, design the data layer schema, and produce taxonomy documentation that ensures consistent, meaningful tracking across all platforms, pages, and campaigns. This skill creates the shared language that analytics, engineering, and marketing use to talk about user behavior.

## When to Use

- Creating an event taxonomy for a new tenant website
- Adding new events for a feature launch or campaign
- Standardizing inconsistent event naming across an existing implementation
- Designing the data layer schema for a new tracking implementation
- Documenting event parameters for engineering handoff
- Auditing existing events for naming inconsistencies or gaps

## Context Loading

Before any taxonomy work:
1. Read existing event taxonomy in `docs/tracking/event-taxonomy.yaml` (if it exists)
2. Read the site architecture (page list, user flows) to identify trackable interactions
3. Read conversion goals from the campaign brief or strategic plan
4. Read existing tracking implementation in `web/src/lib/analytics/` for current state
5. Identify all analytics consumers: marketing, product, sales, executive reporting

## Naming Convention

### Event Name Format

```
object_action
```

- **Object**: the thing being interacted with (noun, singular)
- **Action**: what happened (past tense verb)

Examples:
```
form_submitted
page_viewed
video_played
booking_started
booking_completed
newsletter_subscribed
contact_created
cta_clicked
```

### Naming Rules

1. All lowercase with underscores (snake_case)
2. Object comes first, action second (noun_verb)
3. Past tense for completed actions (`form_submitted`, not `form_submit` or `submit_form`)
4. Present participle for ongoing states (`video_playing`, not `video_play`)
5. No abbreviations (`button_clicked`, not `btn_clkd`)
6. No platform-specific prefixes (`form_submitted`, not `ga4_form_submitted`)
7. Maximum 40 characters (GA4 limit)

### Prohibited Patterns

- camelCase (`formSubmitted`) -- inconsistent with analytics platform conventions
- dot notation (`form.submitted`) -- conflicts with some data layer implementations
- Verb-first (`submit_form`) -- harder to group by object in analytics tools
- Generic names (`click`, `event`, `action`) -- meaningless without context
- Platform names in events (`ga_pageview`) -- taxonomy is platform-agnostic

## Event Categories

### Lifecycle Events

Track the user's progression through the funnel:

```yaml
lifecycle_events:
  - name: page_viewed
    description: "Any page load or client-side navigation"
    auto: true  # Fired automatically by the tracking library
    parameters:
      page_location: "Full URL"
      page_title: "Document title"
      page_referrer: "Previous page URL"

  - name: session_started
    description: "New session initiated (30-min inactivity timeout)"
    auto: true
    parameters:
      session_id: "Unique session identifier"
      is_first_session: "Boolean"

  - name: lead_captured
    description: "User provided contact information"
    parameters:
      form_name: "Name of the form"
      lead_source: "How they arrived (UTM source)"
      lead_type: "inquiry | application | newsletter"

  - name: booking_started
    description: "User initiated a scheduling flow"
    parameters:
      event_type: "discovery-call | consultation | retreat"
      source_page: "Page where booking was initiated"

  - name: booking_completed
    description: "User confirmed a booking"
    parameters:
      event_type: "discovery-call | consultation | retreat"
      booking_value: "Monetary value"
      booking_currency: "USD"
```

### Engagement Events

Track meaningful interactions that indicate interest:

```yaml
engagement_events:
  - name: cta_clicked
    description: "User clicked a call-to-action element"
    parameters:
      cta_text: "Button or link text"
      cta_location: "hero | sidebar | footer | inline"
      cta_destination: "Target URL or action"

  - name: video_played
    description: "User started playing a video"
    parameters:
      video_title: "Video name"
      video_duration: "Total duration in seconds"
      video_source: "youtube | vimeo | self-hosted"

  - name: video_milestone
    description: "User reached a playback milestone"
    parameters:
      video_title: "Video name"
      milestone: "25 | 50 | 75 | 100 (percent)"

  - name: content_scrolled
    description: "User scrolled past a depth threshold"
    parameters:
      scroll_depth: "25 | 50 | 75 | 90 (percent)"
      page_location: "URL of the page"

  - name: testimonial_viewed
    description: "User viewed a testimonial or social proof element"
    parameters:
      testimonial_id: "Identifier"
      testimonial_type: "text | video | case-study"
```

### Form Events

Track form interactions at a granular level:

```yaml
form_events:
  - name: form_started
    description: "User focused on the first field of a form"
    parameters:
      form_name: "Form identifier"
      form_type: "contact | application | newsletter | booking"

  - name: form_step_completed
    description: "User completed a step in a multi-step form"
    parameters:
      form_name: "Form identifier"
      step_number: "Current step (1-indexed)"
      step_name: "Step label"

  - name: form_field_error
    description: "Validation error displayed on a form field"
    parameters:
      form_name: "Form identifier"
      field_name: "Field that errored"
      error_type: "required | format | length | custom"

  - name: form_abandoned
    description: "User left a form without submitting"
    parameters:
      form_name: "Form identifier"
      last_field: "Last field interacted with"
      fields_completed: "Count of completed fields"

  - name: form_submitted
    description: "User successfully submitted a form"
    parameters:
      form_name: "Form identifier"
      form_type: "contact | application | newsletter | booking"
      submission_id: "Unique submission identifier"
```

### Commerce Events

Track purchase-related actions (aligned with GA4 ecommerce schema):

```yaml
commerce_events:
  - name: item_viewed
    description: "User viewed a product or offer"
    parameters:
      item_name: "Product/offer name"
      item_id: "Product/offer identifier"
      item_category: "retreat | course | workshop"
      price: "Price in USD"

  - name: checkout_started
    description: "User initiated checkout"
    parameters:
      items: "Array of items"
      value: "Total value"
      currency: "USD"

  - name: purchase_completed
    description: "Transaction confirmed"
    parameters:
      transaction_id: "Unique transaction ID"
      value: "Total value"
      currency: "USD"
      items: "Array of items"
      payment_method: "card | transfer | other"
```

## Parameter Standards

### Global Parameters

These parameters are sent with every event:

```yaml
global_parameters:
  - name: tenant_id
    type: string
    description: "Tenant identifier for multi-tenant reporting"
    example: "acme-corp"

  - name: user_type
    type: string
    description: "User classification"
    values: ["anonymous", "lead", "customer", "alumni"]

  - name: page_section
    type: string
    description: "Section of the page where the event occurred"
    values: ["hero", "body", "sidebar", "footer", "modal"]

  - name: device_type
    type: string
    description: "Device category"
    values: ["desktop", "tablet", "mobile"]
    auto: true
```

### Parameter Naming Rules

1. All lowercase with underscores (snake_case)
2. Descriptive names (`form_name`, not `fn`)
3. Consistent types: strings for categories, numbers for quantities, booleans for flags
4. No PII: never include email, phone, full name, or IP address
5. Enum values documented for every parameter with a fixed set of options

### Parameter Types

| Type | Convention | Example |
|---|---|---|
| String | Lowercase, hyphenated values | `"discovery-call"` |
| Number | Raw number, no formatting | `29.99` |
| Boolean | true/false (not 0/1) | `true` |
| Array | Array of objects | `[{ item_name: "...", price: 99 }]` |
| Currency | Separate value and currency fields | `value: 99.00, currency: "USD"` |

## Taxonomy Document Format

The canonical taxonomy lives in a YAML file:

```yaml
# docs/tracking/event-taxonomy.yaml
version: "1.0.0"
last_updated: "2026-03-17"
owner: "Analytics Engineer"

naming_convention:
  format: "object_action"
  case: "snake_case"
  max_length: 40

global_parameters:
  - { name: tenant_id, type: string, required: true }
  - { name: user_type, type: string, required: false }
  - { name: page_section, type: string, required: false }

events:
  - name: form_submitted
    category: form
    description: "User successfully submitted a form"
    platforms: [ga4, meta, google_ads]
    parameters:
      - { name: form_name, type: string, required: true, example: "contact-form" }
      - { name: form_type, type: string, required: true, values: ["contact", "application", "newsletter"] }
    implementation_notes: "Fire after server-side validation confirms success, not on client-side submit"
```

## Audit Workflow

### Checking Existing Events

1. Export all events from GA4 (Admin > Events)
2. Compare against the taxonomy document
3. Flag events that do not match the naming convention
4. Flag events missing required parameters
5. Flag undocumented events (in GA4 but not in taxonomy)
6. Flag documented-but-unimplemented events (in taxonomy but never fired)

### Audit Report Format

```markdown
## Event Taxonomy Audit — [Date]

### Summary
- Documented events: [n]
- Implemented events: [n]
- Undocumented (in platform, not in taxonomy): [list]
- Unimplemented (in taxonomy, not in platform): [list]
- Naming violations: [list with corrections]
- Missing parameters: [list]

### Recommendations
1. [Add/remove/rename specific events]
2. [Fix parameter issues]
3. [Update taxonomy document]
```

## Error Handling

- Naming conflict (two events with the same name but different meanings): rename the more specific one with a qualifying prefix (`form_submitted` vs `quiz_form_submitted`)
- Parameter type mismatch (string sent where number expected): fix at the source, log for debugging
- Event volume anomaly (sudden spike or drop): investigate tracking code changes, consent changes, or traffic changes before modifying the taxonomy

## Boundaries

- Never include PII in event names or parameters
- Never create events without documenting them in the taxonomy
- Never rename events in production without a migration plan (rename breaks historical data)
- Never create duplicate events that track the same action with different names

## Dependencies

- `conversion-tracking` -- implements the events defined in this taxonomy
- `attribution-modeling` -- consumes events for journey and attribution analysis
- `analytics-tracking` -- GA4 configuration that references this taxonomy
- `api-routes` -- server-side events triggered by API route handlers

## State Tracking

- `taxonomy` -- version, last updated, event count, parameter count
- `events` -- keyed by event name: category, platforms, implementation status, last fired
- `audits` -- keyed by audit date: violations found, resolutions applied
