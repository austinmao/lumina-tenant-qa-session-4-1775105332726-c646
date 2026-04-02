---
name: post-webinar-close
description: "Generate a 5-7 email close sequence for webinar viewers who didn't book"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /post-webinar-close
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins:
        - python3
---

# Post-Webinar Close Sequence

Generate a 5-7 email close sequence targeting the "watched but didn't book"
segment. Based on the Post-Webinar Conversion archetype (E1-E8) from
`email-frameworks/SKILL.md`.

## When to Use

After a webinar replay has been sent and the replay window is open. This
sequence targets registrants who:
- Watched the replay (or attended live) but didn't book a connection call
- Engaged with webinar content but didn't take the next step

## Sequence Architecture

Arc: **Inspiration → Consideration → Doubt → Resolution → Decision**

### E1 — Replay + Key Insight (2-4h post-event)

Already sent by `replay-email-send` in the post-webinar-event pipeline.
This skill generates E2-E8.

### E2 — Expand One Transformation (Day 1)

- **Emotional job**: Belief — "This is real and possible for me"
- **Content**: Pick the most resonant transformation from the webinar. Expand
  with one specific detail the audience hasn't heard. No pitch.
- **CTA**: Soft — "If this resonated, I'll be sharing more this week"

### E3 — Testimonial Match (Day 2-3)

- **Emotional job**: Trust — "Someone like me did this"
- **Content**: Alumni testimonial matched to the top audience fear identified
  in webinar Q&A. Use the the brand's five-stage transformation story arc.
- **CTA**: Soft — "She'll be answering questions on our next call"
- **Note**: `[ALUMNI CONSENT REQUIRED]` — do not fabricate testimonials

### E4 — Objection Handling (Day 4-5)

- **Emotional job**: Resolution — "My concerns are valid and addressed"
- **Content**: Name the real objections (cost, timing, readiness, "is this
  right for me"). Address each directly. Never use strawmen.
- **CTA**: Medium — "Book a free connection call to talk through your questions"
- **Framework**: FAQ format works well. 3-4 objections max per email.

### E5 — Cost of Inaction (Day 6)

- **Emotional job**: Honest urgency — "What happens if I don't decide"
- **Content**: What does another year of the same pattern look like? Frame
  honestly, not manipulatively. Acknowledge that timing matters.
- **CTA**: Medium — "If the timing feels right, book a call this week"
- **Constraint**: NEVER use shame, fear amplification, or pain exploitation.
  State the cost factually.

### E6 — Deadline + Transformation Recap (48h before close)

- **Emotional job**: Clarity — "I know what I'm deciding and when"
- **Content**: Recap the 3 key shifts from the webinar. State the enrollment
  deadline plainly. No fake urgency — only real deadlines.
- **CTA**: Direct — "Book your connection call before [date]"
- **Constraint**: Only state deadlines that are real. If there's no deadline,
  use "spots are filling" only if confirmed by operator.

### E7 — Last Call (Final hours)

- **Emotional job**: Decision — "It's time to choose"
- **Content**: Short. One CTA only. Restate what they're choosing between.
  Acknowledge that "not yet" is a valid choice.
- **CTA**: Direct — "Book now" or "Reply with questions"

### E8 — Off-Ramp (After close)

- **Emotional job**: Respect — "This relationship continues regardless"
- **Content**: Thank them for their time. Route non-buyers to the nurture
  sequence. No guilt, no "you missed out."
- **CTA**: Soft — "We'll keep sharing. Hit reply anytime."
- **Purpose**: Preserve the relationship for future offers.

## Output

The skill produces two artifacts in the campaign run directory:

### 1. Sequence Brief (`close-sequence-brief.yaml`)

```yaml
campaign_slug: have-a-good-trip-v2
pipeline_id: e2e-smoke-059
segment: watched-replay-no-book
enrollment_window_days: 7
emails:
  - id: close-e2
    day: 1
    emotional_target: belief
    subject_draft: "The one thing most people miss about set and setting"
    cta_type: soft
  - id: close-e3
    day: 3
    emotional_target: trust
    subject_draft: "She came in skeptical. Here's what changed."
    cta_type: soft
    requires_alumni_consent: true
  # ... E4-E8
```

### 2. Copy Deck (`close-copy-deck.md`)

Full draft copy for each email following `copywriting` and
`voice-calibration` standards. Handed to Forge (email-engineer) for HTML
rendering.

## Lobster Integration

New stages in `post-webinar-event.lobster` after `replay-email-send`:

```yaml
- id: close-sequence-gen
  command: scripts/lobster-close-sequence.sh ${pipeline_id}
  condition: $approval.approved

- id: close-email-html
  command: scripts/lobster-forge-parallel-v3.sh ${pipeline_id} close
  condition: $approval.approved
```

## Behavioral Integration

When `behavioral-automation` rules are active, this sequence is triggered
by the `replay-50-watch` behavioral trigger instead of being sent to all
registrants. The segment narrows from "all registrants" to "watched >50%
replay but didn't book."

## Related Skills

- `email-frameworks` — Post-Webinar Conversion archetype (E1-E8)
- `email-sequences` — Brunson replay formula for E1
- `voice-calibration` — Register calibration for all copy
- `copywriting` — CTA language, subject line patterns
- `behavioral-automation` — Segment refinement via behavioral triggers
