---
name: email-sequence-frameworks
description: "Design email sequence architecture for any offer using proven lifecycle patterns"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /email-sequence-frameworks
metadata:
  openclaw:
    emoji: "incoming-envelope"
    requires:
      bins: []
      env: []
---

# Email Sequence Frameworks

## Overview

Structural design patterns for building new email sequences across the
lifecycle: free offer, webinar, program, retreat, and alumni re-engagement.

**Skill relationships:** This skill provides architecture. `email-sequences`
provides tenant-specific templates. `copywriting` + `voice-calibration`
provide copy standards. Use all three together when building a new sequence.

## Core Principles

1. **One email, one job.** One primary purpose, one main CTA.
2. **Value before ask.** Lead with usefulness. Earn the right to invite.
3. **Relevance over volume.** Fewer, better emails. Segment for relevance.
4. **Clear path forward.** Every email moves the reader somewhere specific.
5. **Emotional arc first.** Map the reader's likely emotional state at each
   position. Adjust register per `voice-calibration` V5.

---

## Sequence Archetypes

### 1. Free Offer to Webinar Bridge

**Purpose:** Deliver free offer value, build relationship, optimize show-up.
**Emails:** 4-6 | **Duration:** 7-10 days
**Arc:** Gratitude -> Curiosity -> Anticipation -> Commitment

- E1 (immediate): Deliver free offer + set expectations
- E2 (day 1-2): Expand on one insight from the offer
- E3 (day 3-4): Story that seeds the webinar topic
- E4 (day 5-6): Webinar invitation with specific outcome promise
- E5 (day before): Show-up optimization: what to expect, how to prepare
- E6 (morning of): Final reminder, short and direct

**Critical:** E1 sets tone for the relationship. E4 must feel like a natural
next step, not a pivot to selling. E5 reduces anxiety with practical details.

### 2. Post-Webinar Conversion

**Purpose:** Replay access, objection handling, testimonial drip, enrollment
window management, graceful off-ramp for "not yet" people.
**Emails:** 5-8 | **Duration:** 7-14 days (aligned to enrollment window)
**Arc:** Inspiration -> Consideration -> Doubt -> Resolution -> Decision

- E1 (2-4h post-event): Replay delivery + key insight recap
- E2 (day 1): Expand on one transformation from the webinar
- E3 (day 2-3): Testimonial matched to top audience fear
- E4 (day 4-5): Objection handling (cost, timing, readiness)
- E5 (day 6): Cost of inaction — honest, not manipulative
- E6 (48h before close): Deadline + transformation recap
- E7 (final hours): Last call, one CTA only
- E8 (after close): Off-ramp into nurture, no guilt

**Critical:** E1 is typically highest-converting (see `email-sequences` Brunson
replay formula). E4 must name real objections, not strawmen. E8 preserves the
relationship for future offers.

### 3. Enrollment to Activation

**Purpose:** Welcome, orient, deliver first win, introduce community, give
permission to go at their own pace.
**Emails:** 5-7 | **Duration:** 14 days
**Arc:** Excitement -> Overwhelm -> Reassurance -> Momentum

- E1 (immediate): Welcome + logistics (what happens next)
- E2 (day 1-2): First win — one small completable action
- E3 (day 3-5): Orientation — where to find things, who to contact
- E4 (day 6-8): Community introduction — who else is here
- E5 (day 9-11): "You're not behind" permission email
- E6 (day 12-14): Preparation milestone

**Critical:** E2 (first win) is the most important onboarding email. E5
addresses the overwhelm that peaks around day 7-10 in transformation programs.

### 4. Program to Retreat Bridge

**Purpose:** Position retreat as natural deepening, not upsell. Credit/incentive
framing, alumni stories, connection call (not hard sell).
**Emails:** 4-5 | **Duration:** 21-30 days | **Spacing:** 5-7 days apart
**Arc:** Accomplishment -> Curiosity -> Longing -> Readiness

- E1 (week 1 post-program): Celebrate completion + credit/incentive reveal
- E2 (week 2): Alumni story — someone who went deeper
- E3 (week 3): What the retreat experience is actually like (specifics)
- E4 (week 3-4): Connection call invitation (not "apply now")
- E5 (week 4, optional): Gentle follow-up if no response

**Critical:** E1 frames credit as earned, not promotional. E4 uses invitation
language — the active brand voice never says "apply now" or "enroll today" in bridges.

### 5. Post-Experience Integration

**Purpose:** 30-day guided integration, community re-engagement, referral
activation at peak transformation, soft "what's next."
**Emails:** 6-8 | **Duration:** 30 days
**Arc:** Tender -> Grounded -> Expansive -> Connected

- E1 (day 1): Thank you + one integration practice for today
- E2 (day 3): Check-in question (reply-based, no CTA)
- E3 (day 7): One insight or story from the experience
- E4 (day 14): Integration resource (practice, reading, exercise)
- E5 (day 21): Community re-engagement — how to stay connected
- E6 (day 30): Reflection + referral/testimonial invitation
- E7 (day 30, optional): Soft "what's next" — upcoming offerings, no pressure

**Critical:** E1 is care, not marketing. E6 catches people at peak
transformation clarity — best timing for testimonial requests.

### 6. Re-Engagement / Sunset

**Purpose:** Re-engage lapsed subscribers or gracefully remove them.
**Emails:** 3 | **Duration:** 14 days | **Trigger:** 60-90 days no opens
**Arc:** Honest -> Respectful -> Open door

- E1 (day 0): "We noticed you've been quiet" — genuine, no guilt
- E2 (day 7): Best content piece, no pitch — remind why they subscribed
- E3 (day 14): Permission to leave + one-click to stay

**Critical:** E1 never says "we miss you!" (needy). E3 sets a real removal
date. Remove non-responders after deadline.

---

## Timing Frameworks

**Spacing:** Early sequence 1-2 days apart. Mid-sequence 2-4 days. Late/nurture
5-7 days. Urgency windows (close, event day): daily for 48-72h max.

**Recommended send times:** Sunday 9-10am MT highest (40-47% opens). Thursday
9-10am MT best weekday. Monday-Thursday mid-week lowest (13-20%). Avoid Friday
PM and Saturday.

---

## Subject Line Patterns

Target 40-60 characters. Test one pattern per A/B.

| Pattern | Example |
|---------|---------|
| Curiosity gap | "The one thing I got wrong about healing" |
| Specificity | "What happened on day 3 of the retreat" |
| Question | "Have you ever felt too broken to start?" |
| Personal | "I wasn't going to send this" |
| Story hook | "She almost cancelled the morning of" |

**Preview text:** 85-140 chars. Complement subject — never repeat it.

---

## Personalization Strategy

**Baseline:** First name with fallback ("there" or "friend").

| Data point | Usage |
|------------|-------|
| Quiz result | Tailor core problem statement in E1-E2 |
| Webinar attendance | Split opening line in replay email |
| Engagement level | Adjust subject line aggressiveness |
| Program completed | Reference specific program in bridge |
| Retreat location | Reference shared experience in integration |

**Rule:** Personalization must feel like attention, not surveillance.

## Segmentation Logic

| Segment | Definition | Implication |
|---------|------------|-------------|
| Attended live | Watched in real-time | Lead with shared experience |
| Registered, didn't attend | Signed up, missed it | Lead with replay, no shaming |
| Opened, didn't click | Engaged but not acting | Simplify CTA, reduce friction |
| Clicked, didn't convert | Interested but hesitant | Address objections directly |
| Completed program | Finished program | Bridge to retreat, alumni tone |
| Stalled in onboarding | Started, stopped | "You're not behind" email |
| Lapsed 60+ days | No opens 60-90 days | Re-engagement / sunset path |

**Exit conditions (define for every sequence):**
- Positive: Took the target action (enrolled, registered, booked call)
- Negative: Completed sequence without acting -> route to nurture
- Sunset: No engagement after re-engagement -> remove from active list

---

## Testing Methodology

**Ranked by impact:** (1) Subject lines, (2) Send time, (3) Sequence length,
(4) Content order, (5) CTA copy.

**Rules:** One variable per test. Minimum 100 recipients per variant. Wait for
full sequence completion before judging. Document results.

| Metric | Benchmark | Action if below |
|--------|-----------|-----------------|
| Open rate | 25-45% | Test subjects, check deliverability |
| Click rate | 3-8% | Simplify CTA, check value prop |
| Unsubscribe | Under 0.5%/email | Check frequency, relevance |
| Sequence completion | 60%+ reach final | Check timing, engagement drops |

---

## Email Audit Checklist

### Deliverability
- [ ] Verified sender domain
- [ ] Subject under 60 chars
- [ ] Preview text set (not auto-generated)
- [ ] Plain text fallback exists
- [ ] Images have alt text
- [ ] Total size under 100KB

### Mobile
- [ ] Single-column or responsive layout
- [ ] CTA tap target minimum 44x44px
- [ ] Body font minimum 14px
- [ ] Tested in mobile preview

### Content
- [ ] One primary CTA per email
- [ ] CTA text is action + outcome (not "Click Here")
- [ ] Opening line earns the second line
- [ ] Personalization tokens have fallbacks
- [ ] No broken merge tags
- [ ] Claims backed by proof

### Compliance
- [ ] Physical mailing address included
- [ ] Unsubscribe link present and functional
- [ ] No fabricated urgency or false scarcity
- [ ] Deadlines and capacity verified as factual

### Sequence Integrity
- [ ] Entry trigger defined and tested
- [ ] Exit conditions defined (positive, negative, sunset)
- [ ] Emotional arc reviewed across all emails
- [ ] Suppression rules set (don't email converters)

---

## Steps

1. Confirm offer and audience segment with the operator.
2. Select archetype (or chain multiple with explicit handoff points).
3. Map emotional arc for this specific audience.
4. Draft sequence table: email #, timing, role, emotional target, subject
   direction, CTA.
5. For each email: subject (with A/B variant), preview text, body outline
   (hook/context/value/CTA/sign-off), personalization, segment conditions.
6. Run audit checklist against each email.
7. Note which emails need templates in `email-design-system`.
8. Present architecture to the operator before copy is written in `email-sequences`.

## Output Format

```
Sequence: [Name]
Archetype: [1-6]
Offer: [What this supports]
Trigger: [Entry condition]
Emails: [Count] | Duration: [Days]
Arc: [State] -> [State] -> [State] -> [State]
Exit: Positive=[action] | Negative=[route] | Sunset=[days]

E1: [Name]
  Timing: [When] | Emotional target: [State]
  Subject: [Draft] | A/B: [Variant]
  Preview: [Text]
  Outline: [Hook -> Context -> Value -> CTA]
  CTA: [Button text] -> [Destination]
  Segment: [Conditions]

[Repeat per email]

Audit: [Pass / issues]
Templates needed: [List]
```

## Error Handling

- If offer does not fit any archetype: ask the operator to describe the customer
  journey, then adapt the closest archetype or propose a hybrid.
- If audience segment is undefined: ask before drafting.
- If deadlines or capacity are needed but not provided: flag immediately.
  Never fabricate urgency or scarcity.
- If sequence exceeds 10 emails: split into two chained sequences with an
  explicit handoff point.
