---
name: email-sequences
description: >
  Design and write full email sequences: soap opera welcome sequences, launch
  sequences, nurture cadences, re-engagement campaigns, and post-retreat
  integration sequences. Use this skill when asked to build or plan a
  multi-email campaign from scratch or extend an existing sequence.
version: 1.0.0
metadata:
  openclaw:
    emoji: "sequence"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env: []
      bins: []
---

# Email Sequences Skill

## Overview

Produce complete, ordered email sequences for campaigns. This
skill covers the full library of sequence types used in retreat and wellness
marketing. All output is copy-ready for the operator's review. No sequences are sent
directly from this skill — all sends route through the email-newsletter skill
with the operator's explicit approval.

## Sequence Types and Structure

### Soap Opera Welcome Sequence (5 emails)

Triggered on new subscriber opt-in. Full copy required for all five emails.

Email 1 — Lead magnet delivery + cliffhanger
- Subject: deliver the promised resource in subject line copy
- Body: 2 to 3 sentences of gratitude-free delivery ("Here it is: [link]"), one
  sentence of genuine value framing, then open loop: "Tomorrow I'll share the
  one thing that changed how I think about [topic]."
- CTA: access the lead magnet
- PS: reinforces the cliffhanger for readers who scroll

Email 2 — Backstory / drama
- Subject: personal and specific ("The retreat I almost didn't go to")
- Body: first-person narrative of the origin story; include a real conflict or
  low point; do not resolve cleanly — end with the reader wanting to know what
  happened next
- CTA: reply-based ("Hit reply — have you ever felt this way?")
- No direct pitch

Email 3 — Epiphany / aha moment
- Subject: the insight, framed as a reframe ("What I got wrong about healing")
- Body: resolve the story from Email 2; name the insight or turning point
  explicitly; bridge it to the reader's own experience
- CTA: soft — one resource, one question, or a link to learn more

Email 4 — Hidden benefits + objection handling
- Subject: address the top objection directly ("'I'm not spiritual enough for a
  retreat' — let me address that")
- Body: name 3 objections; reframe each one in 2 to 3 sentences; use SIPI proof
  after each reframe (Say It, Prove It Immediately with a specific testimonial)
- CTA: first direct offer mention; link to retreat or application page

Email 5 — Genuine urgency + CTA
- Subject: real scarcity or real deadline (must be factually accurate)
- Body: state what closes or changes and when; name the transformation they will
  miss; one primary CTA with no competing links
- Do not fabricate urgency — if no real deadline exists, use a proof-led or
  connection-led CTA instead

### Launch Sequence

Four-phase structure. Produce all emails for each phase.

Phase 1 — Pre-launch (2 weeks before cart open, 3 to 4 emails)
- Content-only: no direct pitch
- Topics: behind-the-scenes, transformation stories from past guests, related
  insight content that seeds the retreat's core promise
- Goal: raise awareness of the pain point the retreat solves

Phase 2 — Announcement (72 to 48 hours before cart opens, 1 to 2 emails)
- "You're Invited" framing: reader-centric, not feature-centric
- Name the dates, capacity, and one specific outcome the reader will leave with
- Include a clear next step, usually `Book a Connection Call`

Phase 3 — Launch Day (cart open, minimum 3 emails)
- Morning (8 to 9am): story-driven; anchor on transformation
- Afternoon (12 to 2pm): proof-driven; SIPI testimonials from past guests
- Evening (8 to 9pm): urgency-driven; registration count, spots remaining (real
  numbers only, if materially relevant
- Plus 2 SMS (coordinate with sms-campaigns skill)

Phase 4 — Close (final 48 hours, 3 emails minimum)
- 48 hours out: name the deadline clearly; recap the transformation
- 24 hours out: if relevant, share real spots remaining; otherwise reinforce fit,
  trust, and the next clear step
- 2 to 4 hours out: final call; one sentence of proof; one CTA only

### Nurture Sequence

Ongoing cadence for engaged non-buyers. 2 to 3 emails per week.
Content-to-pitch ratio: give, give, give, ask.
Give emails: insight, framework, story, resource — no CTA required.
Ask emails: one clear offer, one CTA, and an honest reason to act now.

Structure each nurture email:
1. Open with reader's felt experience (hero framing)
2. Deliver one concrete value item (insight, framework, or story)
3. Optional: soft CTA ("If this resonates, here's what I'm offering this month")

### Re-engagement Sequence (lapsed subscribers)

For contacts with no open in 60 to 90 days. Three-email sunset path:

Email 1 (day 0): "Are we still a fit?" — honest, no guilt, ask if they want
to stay on the list; one clear re-engagement CTA
Email 2 (day 7): final value-give email — best content piece, no pitch; remind
them what they subscribed for
Email 3 (day 14): sunset notice — "I'm removing you from this list Friday so I
only send to people who want to hear from me. Click here to stay." After this
email, remove non-responders from active list.

### Post-Retreat Integration Sequence (30 days)

Triggered the day after a retreat concludes. Supports integration of the
retreat experience and maintains relationship toward next offer.

Day 1: Thank you + one integration practice to do today
Day 3: Check-in question (reply-based)
Day 7: Story of one insight from the retreat (community-building)
Day 14: Resource for integration practice
Day 21: Soft introduction to next offer or upcoming retreat
Day 30: Anniversary reflection + invitation to share story (referral or
testimonial request)

### Live Event Broadcast Sequence (4 emails)

For webinars, live workshops, or single-event broadcasts. This is a standalone
sequence — not a product launch. Use the Launch Sequence for multi-week
cart-open/close campaigns.

Email 1 — Invitation (7 days before event, Thursday 9am MT)
- Goal: registrations from warm audience
- Subject: lead with transformation or tension, not event name (under 50 chars)
- Preview: new detail or open loop, 85-100 chars
- Body: hero-framed opening (reader's struggle), event as the path through it,
  3-5 bullets of what the reader will experience or leave with
- CTA pattern: 3 CTAs (above bullets, after bullets, P.S. text link)
- Header logo: links to event registration page, not homepage
- ONE primary destination URL for all links

Email 2 — Value deepener (4-5 days before, Sunday 9am MT)
- Goal: convert fence-sitters with a specific insight from the training
- Suppress: already-registered contacts (they get a separate confirmation)
- Subject: curiosity gap or personal tone — no urgency yet
- Body: one specific insight, framework, or story that seeds the event topic
- CTA pattern: 3 CTAs, softer copy ("See what we're exploring")

Email 3 — Urgency / last call (day before or morning of event, 9am MT)
- Goal: last-minute registrations
- Subject: short, direct ("Tomorrow at noon" or "Today at noon: joining us?")
- Body: SHORT — 3-5 sentences max, plain text feel, no heavy formatting
- CTA pattern: 3 CTAs, direct copy ("Save your seat")
- Suppress: registered attendees

Email 4 — Replay delivery (same day, within 2-4h of event end)
- Framework: Russell Brunson's Soap Opera Sequence replay structure, adapted to
  the active brand voice. Declare at draft top: "Applying Russell Brunson replay email
  framework (Soap Opera Sequence, Email 4)."
- Goal: highest-converting email in the sequence — do not skip
- Segment: ALL registrants (live attendees + no-shows); personalize opening line
  with `attendedLive` split (handle at render/send time, not list segmentation)
- Subject: under 50 chars, leads with transformation or revelation — NOT the
  event name. Curiosity gap preferred.
  Good: "What we uncovered today" / "Something shifted today"
  Bad: "Have a Good Trip replay is ready" (describes; does not compel)
  Produce 5 subject line variants before recommending final.
- Preview text: 85-100 chars, new tension or specific detail NOT in the subject.
  Never: "The replay is inside." / "Watch the recording here."
- Body structure (Brunson replay formula, adapted to the active brand):
  1. HOOK (2-3 sentences): Name what changed or was revealed. For live
     attendees: lead with the emotional shift in the room. For no-shows: name
     the one thing they missed without shaming — create FOMO through specificity.
  2. BRIDGE (1-2 sentences): Connect the session's core insight to the reader's
     own situation using "you" language. Emotional handoff, not summary.
  3. REPLAY CTA (primary button): "Watch the Replay →" at the replay URL.
     State genuine expiry date as scarcity. Never fabricate.
  4. VALUE STACK RECAP (3-5 bullets): Outcome-framed, not topic-framed.
     Lead each bullet with the transformation, not the method.
     Example: "Why most first-timers over-prepare — and the one shift that
     changes everything" not "Module 3: preparation overview."
  5. OFFER BRIDGE (2-3 sentences): Soft, story-based. No direct pitch language.
     Name the retreat's transformation in one sentence, then: "If that's where
     you want to go, the next step is a 30-minute connection call." Never
     "apply now" or "enroll" — too transactional for the active brand voice.
  6. SECONDARY CTA (offer button): "Book a Connection Call →" → connection
     call URL. This is the ONLY sales CTA. No third button.
  7. SIGN-OFF: Short, personal, italic. Operator name only.
  8. P.S. (high-performing): One line. Restate replay expiry + one curiosity
     hook about a specific moment: "P.S. If one thing was worth 10x your time
     today, it was [moment]. Replay expires [date]."
- No free guide / PDF references unless the asset exists and URL is confirmed.
- No fabricated scarcity. Use only real spot counts and real dates provided by the operator.
- Run through humanizer skill before presenting to the operator.
- CTA rule: primary replay button + secondary connection call button only.
  Never three buttons in a follow-up email.

Timing reference (historical performance):
- Sunday 9-10am MT: highest engagement (40-47% open rates)
- Thursday 9-10am MT: best weekday window for initial invites
- Monday-Thursday mid-week: lowest engagement (13-20% open rates)

## Steps

1. Confirm with the operator: which sequence type, which offer, which segment
2. Confirm any real deadlines, real capacity numbers, or approved offers to use
   (never fabricate)
3. Draft all emails in the sequence in order — subject line + preview text +
   full body + CTA for each
4. Apply personalization tokens in curly-brace format: {first_name},
   {retreat_name}, {retreat_date}, {city}
5. After each email, annotate: framework applied, A/B test recommendation for
   subject line, compliance notes
6. Save draft to memory/drafts/YYYY-MM-DD-sequence-[slug].md
7. Present to the operator for review; do not route to email-newsletter skill until
   the operator gives explicit per-email or per-sequence approval

## Output Format

For each sequence, deliver:
- Sequence overview table (email #, send timing, subject line, goal)
- Full copy for each email in numbered sections
- Annotation block per email
- Approval gate reminder at the end of the full sequence

## Error Handling

- If the operator provides a deadline that has already passed: flag immediately, ask
  for the correct deadline before drafting urgency copy
- If capacity numbers are unknown: ask before writing any copy that references
  spots available — never fabricate
- If the segment is not yet defined: ask the operator to confirm before drafting —
  segment mismatch is the most common cause of low-performing sequences

## Technical Rendering

This skill produces copy drafts only. Drafts are not sent from this skill.
When the operator approves a sequence and it is ready to send as branded HTML email,
use the shared render pipeline:

```
templates/email/render.ts
```

### How to invoke the dispatcher

Pass a JSON payload on stdin with a required `templateName` field:

```bash
RESEND_API_KEY="$RESEND_API_KEY" \
RESEND_TRANSACTIONAL_FROM="$RESEND_TRANSACTIONAL_FROM" \
RESEND_TRANSACTIONAL_REPLY_TO="$RESEND_TRANSACTIONAL_REPLY_TO" \
  npx tsx templates/email/render.ts < /tmp/send-input.json
```

### templateName registry

| Sequence / email type | `templateName` value | Template file |
|---|---|---|
| Retreat Getting Started (onboarding) | `"retreat-getting-started"` | `templates/email/onboarding/RetreatGettingStarted.tsx` |
| Soap Opera Welcome Email | _not yet created_ | needs `templates/email/marketing/WelcomeSequence.tsx` |
| Launch sequence emails | _not yet created_ | needs `templates/email/marketing/LaunchEmail.tsx` |
| Post-retreat integration sequence | _not yet created_ | needs `templates/email/marketing/PostRetreatIntegration.tsx` |
| Re-engagement / sunset emails | _not yet created_ | needs `templates/email/marketing/ReEngagement.tsx` |

### If no template exists yet

Before a sequence can be sent as branded HTML, its template must be created in
`templates/email/marketing/` and registered in `templates/email/render.ts`.

Follow the "Adding a New Template" procedure in the `email-design-system` skill.
That skill contains the full design token reference, React Email structural rules,
and the new-template checklist that must be completed before any first live send.

Do not send raw HTML constructed outside the render pipeline. Do not bypass the
`email-design-system` skill's token constraints when building new templates.

---

## Compliance Notes

- CAN-SPAM: every commercial email must include physical mailing address and
  unsubscribe mechanism; flag if either is missing from the template
- Double opt-in: confirm that new subscribers are double-opted-in before any
  promotional email is added to a sequence
- Sunset after 90 days of inactivity without re-engagement response
