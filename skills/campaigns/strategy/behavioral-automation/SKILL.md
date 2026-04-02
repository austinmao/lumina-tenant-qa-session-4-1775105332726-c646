---
name: behavioral-automation
description: "Define behavior-triggered email branching rules for campaign sequences"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /behavioral-automation
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins:
        - python3
---

# Behavioral Automation

## Overview

Define behavior-triggered email branching rules in structured YAML format for
campaign sequences. This skill produces a `behavioral-rules.yaml` file that the
Lobster pipeline consumes at the `behavioral-rules-gen` stage to activate
conditional sends based on contact behavior (opens, clicks, watch progress,
form abandonment). Use this skill when building a campaign that needs automated
follow-up branches beyond the primary broadcast sequence.

## Core Concept

Standard campaign sequences treat every contact the same. Behavioral automation
adds conditional branches: if a contact takes (or fails to take) a specific
action, they receive a tailored variant instead of — or in addition to — the
next scheduled broadcast. Each branch is defined as a trigger with a condition,
an action, a delay, and suppression rules that prevent over-sending.

---

## Behavioral Triggers

### 1. Open-but-No-Click

A contact opened the email but did not click the CTA. This indicates interest
without commitment — the message landed but the ask was unclear or the friction
was too high.

```yaml
- name: open-no-click
  condition: opened == true AND clicked == false
  action: send_variant
  variant: simplified-single-cta
  delay: 24h
  variant_spec:
    description: >
      Simplified variant with a single, prominent CTA. Remove secondary links,
      navigation elements, and competing asks. Lead with the same value
      proposition but reframe the CTA copy to reduce perceived commitment.
    subject_line_approach: "Different angle on same topic — curiosity or benefit framing"
    max_links: 1
  suppression:
    - contact_converted == true
    - last_behavioral_email < 48h
```

**When to use:** Any email with a clear CTA where open rate is healthy but
CTOR is below 10%.

### 2. Click-but-No-Register

A contact clicked through to the registration or landing page but did not
complete the form. This signals high intent blocked by an objection — price,
timing, logistics, or uncertainty.

```yaml
- name: click-no-register
  condition: clicked == true AND registered == false
  action: send_variant
  variant: objection-handling
  delay: 48h
  variant_spec:
    description: >
      Objection-handling variant. Lead with the most common objection for this
      offer (sourced from sales conversations or FAQ data). Include one
      testimonial from someone who had the same hesitation. Close with a
      low-friction invitation: "Have questions? Reply to this email."
    structure:
      - acknowledge_hesitation
      - address_top_objection
      - social_proof_testimonial
      - soft_cta_reply
    max_length_words: 350
  suppression:
    - contact_converted == true
    - last_behavioral_email < 48h
```

**When to use:** Any campaign driving to a registration form, application, or
booking page.

### 3. Replay Watch >50%

A contact watched more than half the replay but did not book or register. This
is the strongest intent signal short of conversion — they invested significant
time but stopped before committing.

```yaml
- name: replay-watch-50
  condition: replay_watch_pct > 50 AND booked == false
  action: enroll_sequence
  sequence: post-webinar-close
  segment_tag: watched-replay
  delay: 24h
  variant_spec:
    description: >
      Enroll in the post-webinar close sequence with the "watched-replay"
      segment tag. This segment receives a tailored version that references
      their replay engagement: "I noticed you watched the recording..." The
      close sequence handles urgency and deadline messaging.
    sequence_length: 3-5 emails
    references_replay: true
  suppression:
    - contact_converted == true
    - last_behavioral_email < 48h
    - already_in_sequence == post-webinar-close
```

**When to use:** Any campaign with a webinar replay or recorded presentation
as a conversion asset.

### 4. Abandoned Application

A contact started a registration form, application, or intake questionnaire
but did not submit it. This indicates readiness blocked by friction,
overwhelm, or a practical interruption.

```yaml
- name: abandoned-application
  condition: form_started == true AND form_submitted == false
  action: send_variant
  variant: reassurance-return
  delay: 24h
  variant_spec:
    description: >
      Reassurance email. Lead with "You are not behind" framing — normalize
      pausing, acknowledge that starting is the hardest part. Do NOT list what
      they missed or create urgency. Include a direct link back to the form
      with their progress preserved (if the form platform supports draft
      saving). Close with a support offer.
    tone: warm, patient, zero-pressure
    structure:
      - normalize_pausing
      - acknowledge_courage_of_starting
      - direct_link_to_resume
      - support_offer_reply
    max_length_words: 250
  suppression:
    - contact_converted == true
    - last_behavioral_email < 48h
    - form_submitted == true
```

**When to use:** Any multi-step form, application, or intake process.

---

## Suppression Rules

Suppression prevents behavioral triggers from degrading the contact experience.
Every trigger inherits these global suppression rules in addition to any
trigger-specific suppressions.

### Global Suppressions (apply to ALL triggers)

```yaml
global_suppression:
  # Converted contacts are excluded from all behavioral triggers
  - rule: contact_converted == true
    description: >
      A contact who has completed the desired action (booked a call,
      registered, purchased) is excluded from every behavioral trigger.
      Conversion status is checked at fire time, not at condition-match time.

  # Maximum 1 behavioral email per 48h per contact
  - rule: last_behavioral_email < 48h
    description: >
      No contact receives more than one behavioral email within a rolling
      48-hour window. If multiple triggers qualify simultaneously, the
      highest-priority trigger fires and others are suppressed until the
      window clears. Priority order: abandoned-application > replay-watch-50
      > click-no-register > open-no-click.

  # Respect Beacon cadence rules
  - rule: last_any_email < 3h
    description: >
      Behavioral triggers respect Beacon's cadence rules. No behavioral
      email fires within 3 hours of a scheduled broadcast. The trigger is
      delayed (not cancelled) until the cadence window opens.
```

### Suppression Precedence

When a contact qualifies for multiple behavioral triggers simultaneously:

1. Check global suppressions first — if any global rule matches, suppress
2. Check trigger-specific suppressions — if any trigger rule matches, suppress
3. If multiple triggers pass suppression, fire only the highest-priority one
4. Suppressed triggers are not queued — they are discarded. If the behavior
   persists, the trigger will re-evaluate on the next cycle.

### Priority Order

```yaml
trigger_priority:
  1: abandoned-application    # Strongest intent signal — form interaction
  2: replay-watch-50          # High intent — significant time investment
  3: click-no-register        # Medium intent — page visit without completion
  4: open-no-click            # Low intent — passive engagement
```

---

## Timing Constraints

### Delay Semantics

- All `delay` values are **minimum delays**. The actual send time may be later
  if cadence rules require spacing.
- Delays are measured from the moment the behavioral event is detected, not
  from the original email send time.
- Behavioral triggers fire AFTER the delay window elapses. During the delay,
  the system checks whether the contact has taken the desired action. If they
  have, the trigger is suppressed.

### Delay Window Cancellation

```yaml
delay_cancellation:
  rule: >
    If a contact takes the desired action during the delay window, suppress
    the trigger entirely. Do not send the behavioral variant.
  examples:
    - trigger: open-no-click
      cancelled_by: contact clicks any link in the original email
    - trigger: click-no-register
      cancelled_by: contact completes registration
    - trigger: replay-watch-50
      cancelled_by: contact books a call or registers
    - trigger: abandoned-application
      cancelled_by: contact submits the form
```

### Cadence Interaction

```yaml
cadence_rules:
  min_gap_broadcast: 3h
  description: >
    If a broadcast email is scheduled within 3 hours before or after the
    behavioral trigger's fire time, the behavioral trigger is delayed until
    the cadence window opens. The broadcast always takes priority.
  max_delay_extension: 12h
  description_overflow: >
    If cadence rules push a behavioral trigger more than 12 hours past its
    intended fire time, discard the trigger. The moment has passed — sending
    late would feel disconnected from the behavior.
```

---

## Output Format

This skill writes a `behavioral-rules.yaml` file to the campaign run directory:

```
memory/campaign-runs/<slug>/<pipeline_id>/inputs/behavioral-rules.yaml
```

### Output Schema

```yaml
# behavioral-rules.yaml
version: "1.0"
campaign_slug: "<slug>"
pipeline_id: "<pipeline_id>"
generated_at: "YYYY-MM-DDTHH:MM:SSZ"

global_suppression:
  - rule: contact_converted == true
  - rule: last_behavioral_email < 48h
  - rule: last_any_email < 3h

trigger_priority:
  1: abandoned-application
  2: replay-watch-50
  3: click-no-register
  4: open-no-click

triggers:
  - name: open-no-click
    condition: opened == true AND clicked == false
    action: send_variant
    variant: simplified-single-cta
    delay: 24h
    suppression:
      - contact_converted == true
      - last_behavioral_email < 48h

  - name: click-no-register
    condition: clicked == true AND registered == false
    action: send_variant
    variant: objection-handling
    delay: 48h
    suppression:
      - contact_converted == true
      - last_behavioral_email < 48h

  - name: replay-watch-50
    condition: replay_watch_pct > 50 AND booked == false
    action: enroll_sequence
    sequence: post-webinar-close
    segment_tag: watched-replay
    delay: 24h
    suppression:
      - contact_converted == true
      - last_behavioral_email < 48h
      - already_in_sequence == post-webinar-close

  - name: abandoned-application
    condition: form_started == true AND form_submitted == false
    action: send_variant
    variant: reassurance-return
    delay: 24h
    suppression:
      - contact_converted == true
      - last_behavioral_email < 48h
      - form_submitted == true
```

---

## Lobster Pipeline Integration

### Stage: `behavioral-rules-gen`

This skill is invoked during the `behavioral-rules-gen` stage of a Lobster
campaign workflow. The stage sits between sequence design and asset generation:

```
... → sequence-design → behavioral-rules-gen → asset-generation → ...
```

**Input from previous stage:** The sequence design stage provides the campaign
slug, pipeline ID, sequence structure (how many emails, what order), and the
primary CTA for each email. The behavioral-automation skill uses this to
determine which triggers are relevant — not every campaign needs all four
triggers.

**Output to next stage:** The `behavioral-rules.yaml` file is consumed by the
asset generation stage, which produces the variant copy for each triggered
branch. The variant specs in the rules file guide copywriters (human or agent)
on tone, structure, and length for each variant.

### Trigger Selection Logic

Not every campaign activates all four triggers. Selection depends on campaign
type:

| Campaign type | Triggers to activate |
|---|---|
| Webinar + replay | open-no-click, click-no-register, replay-watch-50 |
| Retreat launch (no webinar) | open-no-click, click-no-register, abandoned-application |
| Program enrollment | open-no-click, click-no-register, abandoned-application |
| Newsletter / nurture | open-no-click only |
| Webinar + application | All four |

### Lobster Step Configuration

```yaml
# In the Lobster workflow YAML
- step: behavioral-rules-gen
  skill: /behavioral-automation
  inputs:
    campaign_slug: "{{campaign_slug}}"
    pipeline_id: "{{pipeline_id}}"
    campaign_type: "{{campaign_type}}"
    sequence_emails: "{{sequence_design.emails}}"
  outputs:
    behavioral_rules: "memory/campaign-runs/{{campaign_slug}}/{{pipeline_id}}/inputs/behavioral-rules.yaml"
```

---

## Data Sources

Behavioral triggers depend on engagement data from external platforms. The
skill does not fetch this data directly (`network: false`) — it defines the
rules that the campaign execution engine evaluates at runtime using data from
these sources.

### Email Engagement (opens, clicks)

| Source | Data provided | Access method |
|---|---|---|
| Resend webhook events | `email.opened`, `email.clicked`, `email.bounced` | Webhook → Vercel API route |
| MailChimp Reports API | Open rate, click rate, CTOR per campaign | `GET /reports/{campaign_id}/email-activity` |
| Resend Audiences API | Contact-level engagement history | `GET /audiences/{id}/contacts` |

### Registration / Form Completion

| Source | Data provided | Access method |
|---|---|---|
| Typeform Responses API | Form started (partial), form submitted (complete) | `GET /forms/{form_id}/responses` |
| Vercel Postgres | Registration records, booking status | Direct query on `campaigns` table |
| Attio CRM | Contact stage, deal status, conversion flags | Attio REST API v2 |

### Replay / Watch Progress

| Source | Data provided | Access method |
|---|---|---|
| Mux Data API | Watch percentage, engagement score | `GET /data/v1/video-views` |
| Zoom Reports API | Webinar attendee duration, replay views | `GET /report/webinars/{id}/participants` |
| Custom tracking pixel | Page-level replay engagement (fallback) | Vercel API route event ingestion |

### Data Freshness

- Email engagement data: available within 1-5 minutes of event (webhook-based)
- Form completion data: available within 1 minute (webhook or polling)
- Replay watch data: available within 15-60 minutes (batch API, not real-time)
- Behavioral triggers should not fire on stale data. If the engagement event
  is older than the trigger delay, re-check the current state before sending.

---

## Steps

1. **Identify campaign type** — determine which behavioral triggers are
   relevant using the trigger selection table above.
2. **Gather campaign context** — collect the campaign slug, pipeline ID,
   sequence structure, and primary CTA for each email from the operator or
   from the previous Lobster stage output.
3. **Select applicable triggers** — include only the triggers that match the
   campaign type. Do not include triggers for behaviors that cannot occur
   (e.g., replay-watch-50 for a campaign with no replay).
4. **Customize variant specs** — adjust the variant descriptions based on the
   specific offer, audience, and tone. Use the `variant_spec` section to
   provide enough detail for the copywriter to produce the variant without
   additional context.
5. **Validate suppression rules** — confirm that global suppressions are
   present and that trigger-specific suppressions cover all edge cases
   (e.g., form_submitted == true for abandoned-application).
6. **Write output file** — produce `behavioral-rules.yaml` to the campaign
   run directory at the path specified in the output format section.
7. **Log the generation** — note in the pipeline state which triggers were
   activated and which were excluded, with reasoning.

## Output

Deliver `behavioral-rules.yaml` at:
`memory/campaign-runs/<slug>/<pipeline_id>/inputs/behavioral-rules.yaml`

The file follows the output schema defined above. Include a comment header
with the generation timestamp and the skill version.

## Error Handling

- If campaign type is not provided or not recognized: ask the operator to
  specify the campaign type from the supported list before proceeding.
- If the campaign has no CTA (pure nurture/value email): only activate
  the open-no-click trigger. Log the reasoning.
- If the pipeline directory does not exist: create it with `mkdir -p` before
  writing the output file.
- If a previous `behavioral-rules.yaml` exists at the output path: back up
  the existing file to `behavioral-rules.yaml.bak` before overwriting.
  Log the backup path.

---

## Related Skills

- **campaign-strategy** (`skills/campaigns/strategy/campaign-strategy`): Defines segmentation and launch calendar; behavioral triggers layer on top of the campaign plan.
- **email-frameworks** (`skills/campaigns/email/email-frameworks`): Provides sequence architecture patterns that behavioral branches extend.
- **email-sequences** (`skills/campaigns/email/email-sequences`): Produces the variant copy for each behavioral branch defined here.
