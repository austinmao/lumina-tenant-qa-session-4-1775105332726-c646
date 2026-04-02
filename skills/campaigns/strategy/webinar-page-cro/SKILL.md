---
name: webinar-page-cro
description: "Optimize webinar registration and replay pages for higher conversion"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /webinar-page-cro
metadata:
  openclaw:
    emoji: "📊"
---

# Webinar Page CRO

## Overview

Analyze and optimize webinar registration pages and replay pages for higher
conversion. Provides webinar-specific component patterns, layout guidance,
A/B test hypotheses, and ethics-compliant urgency and social proof strategies.
Use this skill when building or auditing a webinar registration page, a webinar
replay page, or any landing page anchored to a live or recorded event.

## Steps

1. **Identify the page variant**: Registration (pre-event) or Replay (post-event).
2. **Audit each component** from the Component Reference below against the page.
3. **Check mobile-first layout order** against the recommended sequence.
4. **Verify ethics compliance**: All urgency and social proof must pass the
   marketing-psychology Ethics Layer and the page-cro Layer 3 CTA rules.
5. **Generate A/B test hypotheses** tailored to the page variant.
6. **Compile recommendations** into the output format below.

## Output

### Page Assessment
- Page variant (registration / replay), event date, current state summary
- Component checklist: present / missing / needs improvement per component

### Quick Wins
Easy changes with immediate impact. Each item: what to change, why, specific copy or layout fix.

### High-Impact Changes
Larger changes requiring design or engineering effort.

### A/B Test Hypotheses
2-3 testable hypotheses from the Experiment Ideas section below, scoped to this page.

### Component Scorecard
Rate each of the 7 components: present and compliant / present but needs work / missing.

---

## Component Reference

### 1. Countdown Timer

**Purpose**: Create genuine urgency by showing the real time remaining until the
live event or until replay expiry.

**Registration page**: Displays `days : hours : minutes : seconds` counting down
to `event_date`. When the countdown reaches zero, replace the timer with a static
message: "Event started — join now" (if the event is live) or "Event has ended"
(if past). Never show a negative countdown.

**Replay page**: Counts down to `expiresAt` from the replay-config. When the
countdown reaches zero, replace with "This replay has expired" and hide or disable
the CTA. Cross-reference the `replay-page` skill for the client-side countdown
component pattern (`ReplayCountdown.tsx`).

**Wireframe placement**: Directly below the hero headline on registration pages.
Directly above the video embed on replay pages.

**Implementation notes**:
- Use a Client Component (`"use client"`) with `setInterval` updating every second.
- Accept `targetDate` as an ISO 8601 string prop from the Server Component.
- Server-side: check expiry before render. If `event_date` or `expiresAt` is past
  at request time, render the degraded state directly — do not rely solely on the
  client timer.
- Accessible: use `aria-live="polite"` on the timer container so screen readers
  announce updates without excessive interruption.
- Never use a countdown timer on an evergreen offer that has no real expiration.
  This is a prohibited pattern per the marketing-psychology Ethics Layer.

---

### 2. Social Proof Counter

**Purpose**: Show that other people have committed, reducing the visitor's
perceived risk of registering.

**Display options** (choose one based on available data):
- **Live count**: "347 people registered" — updated from a real data source
  (database query, API, or registration platform count).
- **Static threshold**: "200+ registered" — a truthful floor number that does not
  update in real time. Use when a live count feed is unavailable.

**Rules** (non-negotiable):
- NEVER fabricate or inflate the number. If 12 people have registered, display
  "12 people registered" or omit the counter entirely. Fake social proof is a
  prohibited pattern per the marketing-psychology Ethics Layer.
- NEVER show a counter below a credibility threshold that could backfire (e.g.,
  "3 people registered" may signal low interest). If the count is below 50,
  consider omitting the counter and relying on other trust signals instead.
- Source must be verifiable: registration database, Zoom registrant count, or
  event platform API. A hardcoded number that never changes is fabrication.

**Wireframe placement**: Below the countdown timer on registration pages. Not
typically used on replay pages (use "X people attended" post-event if the number
is available and truthful).

**Implementation notes**:
- For live counts, poll the data source on a reasonable interval (every 60 seconds,
  not every second) or use server-side rendering with a cache TTL.
- Display format: "{count} people registered" with a subtle people icon. No
  animation or flashy counter effects — trust comes from the number, not the
  presentation.
- If using a static threshold, update it manually as the count grows (e.g., update
  from "100+" to "200+" when the count crosses 200).

---

### 3. Speaker Bio Block

**Purpose**: Transfer authority from the speaker to the event, giving the visitor
a reason to trust that this webinar will deliver on its promise.

**Contents**:
- Speaker photo (headshot, not a logo or illustration; real person, not stock)
- Full name and primary credential or title
- 2-3 sentence bio focused on what qualifies this person to teach this topic.
  Lead with the credential most relevant to the webinar topic, not the most
  impressive credential overall.

**Wireframe placement**: Below the hero section, above the agenda teaser. On
mobile, the photo stacks above the name and bio text (never side-by-side on
small screens).

**Implementation notes**:
- Photo: minimum 200x200px, optimized (WebP with JPEG fallback), `loading="lazy"`
  since this component is below the fold.
- Keep the bio tight. Three sentences maximum. Every word must justify the
  speaker's authority on this specific topic.
- If there are multiple speakers, list each with the same format. Order by
  relevance to the webinar topic, not seniority.

---

### 4. Agenda Teaser

**Purpose**: Give the visitor enough information to decide whether this webinar
is worth their time, without revealing so much that they feel they do not need
to attend.

**Format**: 3-5 bullet points, each following the pattern:
"You'll learn: [specific, tangible outcome]"

**Rules**:
- Each bullet names a takeaway, not a topic. "You'll learn: The 3-question
  framework for evaluating readiness" not "We'll discuss readiness."
- Do not list the full webinar outline. The agenda teaser is a conversion tool,
  not a syllabus. Reveal enough to spark curiosity, withhold enough to require
  attendance.
- Use parallel structure across all bullets (each starts with "You'll learn:" or
  a consistent verb phrase).

**Wireframe placement**: Below the speaker bio, above the FAQ section. On
registration pages, this often appears as a distinct card or section with a
subtle background color for visual separation.

**Implementation notes**:
- Use a semantic `<ul>` with custom bullet styling (checkmarks or arrows, not
  default disc bullets).
- Keep each bullet to one line on desktop (two lines maximum on mobile).
- If the webinar has a downloadable resource or bonus, mention it as the final
  bullet: "You'll receive: [resource name] — sent to your inbox after the session."

---

### 5. FAQ Section

**Purpose**: Pre-answer the six most common objections that prevent registration.
Each answer should reduce friction, not create new questions.

**Standard questions and guidance**:

1. **"Is this free?"**
   Answer directly: "Yes, this is a free live session. No credit card required."
   If there is a paid upsell at the end, be transparent: "This is a free session.
   At the end, we will share how to go deeper with [paid offer] — no pressure."

2. **"Will there be a replay?"**
   Answer honestly based on the actual plan. If yes: "Yes, a replay will be
   available for [X days] after the live session." If no: "This session is live
   only — no replay will be available." Never promise a replay and then use its
   absence as fake urgency.

3. **"What if I can't attend live?"**
   If a replay exists: "Register anyway — we will send you the recording." If no
   replay: "We recommend attending live. If your schedule changes, we will notify
   you about future sessions." Never use "Register and we'll send the replay" as
   bait if no replay is planned.

4. **"Is this a sales pitch?"**
   Be honest. If the webinar includes a pitch: "We will share valuable [topic]
   insights for [duration]. At the end, we will introduce [offer] for those who
   want to go further. The session stands on its own — you will leave with
   actionable takeaways regardless." If no pitch: "This is a pure educational
   session. No sales pitch."

5. **"Who is this for?"**
   Name the target audience specifically. "This session is designed for [avatar
   description] who are [current state] and want [desired outcome]." Include a
   "This is NOT for you if..." qualifier to increase trust and self-selection.

6. **"How long is the session?"**
   State the duration directly: "[X] minutes of content, plus [Y] minutes of
   live Q&A." If the session length is variable, give a range.

**Wireframe placement**: Below the agenda teaser, above the final CTA.

**Implementation notes**:
- Use an accordion pattern (collapsed by default, expand on click) to keep the
  page clean. Each question is a toggle header.
- Ensure the accordion is keyboard-accessible (`<details>/<summary>` or proper
  ARIA roles with `aria-expanded`).
- FAQ content should be indexable by search engines — do not hide it behind
  JavaScript that prevents crawling.

---

### 6. Urgency Elements

**Purpose**: Motivate timely action using genuine constraints.

**Permitted urgency patterns** (use only when factually true):
- **Real seat limits**: "This session is limited to [X] live participants for
  interactive Q&A." Only use if there is an actual technical or intentional cap.
  State the real number.
- **Real time-to-event countdown**: The countdown timer (Component 1) already
  communicates this. Do not add additional urgency text ("Hurry!", "Time is
  running out!") — the countdown speaks for itself.
- **Real replay expiry**: "The replay will be available for 72 hours after the
  live session." Only state this if the replay genuinely expires.
- **Real early-bird pricing or bonuses**: "Register before [date] to receive
  [bonus]." Only if the bonus or pricing genuinely expires on that date.

**Prohibited urgency patterns** (never use, regardless of effectiveness):
- Fake countdown timers on evergreen offers
- Fabricated seat limits ("Only 5 spots left!" when capacity is unlimited)
- Countdown timers that reset on page refresh
- "Last chance" language when the offer will recur
- Animated or flashing urgency banners
- Guilt-based urgency ("Don't miss out" or "You'll regret not joining")

**Wireframe placement**: Urgency elements appear inline with or adjacent to the
countdown timer and CTA, not as separate banner sections. Subtlety builds trust;
desperation erodes it.

**Implementation notes**:
- If using a seat-limit counter, it must reflect a live data source (same rules
  as social proof counter). A hardcoded "seats remaining" number that never
  changes is fabrication.
- Pair urgency with reassurance: "12 seats remaining — reserve yours" alongside
  "No commitment required. Cancel anytime before the session."

---

### 7. Replay Page Variant

**Purpose**: Convert replay viewers into the next step (apply, book a call,
register for the next event) while the content is fresh.

**Layout** (extends replay-page skill patterns):
- **Video embed above the fold**: The visitor is here for the recording. Do not
  obstruct with hero text, countdown banners, or interstitials before the video.
  Use the `ReplayCountdown.tsx` pattern from the `replay-page` skill.
- **Countdown to expiry**: Below the video, show time remaining until the replay
  expires. Degrades to "This replay has expired" at zero, disabling the video and
  CTA.
- **Key takeaways**: If a transcript or summary is available, render 3-5 key
  points as a bulleted list below the video. These serve skimmers who will not
  watch the full recording. Source from `summary.key_points` in the replay config.
- **CTA below video**: Prominent, full-width on mobile. Use approved CTA language
  from page-cro Layer 3: "Book a Connection Call," "Join the Next Session," or
  "Begin Here." Never use rejected CTA patterns ("Sign Up," "Buy Now," "Claim
  Your Spot").
- **Testimonials from live attendees** (optional): If available, add 1-2 short
  quotes from live session attendees below the CTA. Same rules as page-cro
  Layer 5 — real testimonials only, with name and context.

**Implementation notes**:
- Read `web/data/replay-config.json` for `url`, `expiresAt`, `summary`, and
  `transcript_vtt_path` fields.
- Server-side expiry check: if `expiresAt` is past at request time, return a 410
  response with `robots: noindex` metadata.
- Do not gate the replay behind a form if the viewer already registered for the
  live event. Gating replays that were promised as free erodes trust.
- Mobile: video player must be responsive (`aspect-video` container). CTA must
  be visible without scrolling past the video on standard mobile viewports.

---

## Mobile-First Layout Order

On mobile devices (and as the default responsive layout), stack components in
this order. This sequence prioritizes the visitor's decision flow: what is this,
when is it, what will I learn, who else is going, who is speaking, what if I have
questions, how do I register.

### Registration Page

1. **Hero** — Headline (opens in the reader's world per page-cro Layer 2), one-sentence value statement, event date and time
2. **Countdown timer** — Time remaining until the live event
3. **Agenda teaser** — 3-5 "You'll learn" bullets
4. **Social proof counter** — "X people registered" (if count meets credibility threshold)
5. **Speaker bio** — Photo, name, credentials, 2-3 sentence bio
6. **FAQ section** — 6 pre-answered objections in accordion format
7. **CTA** — Primary registration button with approved language, repeated from hero

### Replay Page

1. **Video embed** — Recording player, full width, no obstructions
2. **Countdown to expiry** — Time remaining until replay expires
3. **Key takeaways** — 3-5 bullet points from transcript or summary
4. **CTA** — "Book a Connection Call" or next-step action
5. **Testimonials** — 1-2 attendee quotes (if available)

---

## A/B Test Hypotheses

### Hypothesis 1: Agenda Teaser Above vs. Below Social Proof

**Test**: On the registration page, swap the position of the agenda teaser
(Component 4) and the social proof counter (Component 2) in the mobile layout.

**Rationale**: Some visitors are motivated by what they will learn (content-first
decision); others are motivated by what peers are doing (social-first decision).
The default layout assumes content-first. Testing social proof earlier may lift
conversion for audiences with high social sensitivity.

**Expected outcome**: If the audience skews toward community-oriented seekers
(avatars who value belonging), social proof above agenda may lift registration
rate by 5-15%. If the audience is more analytically driven, the default order
should win.

### Hypothesis 2: FAQ Collapsed vs. Expanded by Default

**Test**: Show the FAQ section with all answers expanded (visible without
clicking) vs. the default collapsed accordion.

**Rationale**: Collapsed FAQs reduce visual clutter but require interaction.
Expanded FAQs surface objection answers passively, which may reduce friction for
visitors who would not click to expand. The tradeoff is page length.

**Expected outcome**: Expanded FAQs may improve registration rate for first-time
visitors (who have more objections) while having no effect on return visitors.
Test with a segment split if possible.

### Hypothesis 3: Countdown Timer With vs. Without Seat Count

**Test**: Display the countdown timer alone vs. the countdown timer paired with
a live seat-remaining count (only if a real seat limit exists).

**Rationale**: Combining two urgency signals (time + scarcity) may amplify
conversion, but could also feel pressuring if both are prominent. The
marketing-psychology Ethics Layer permits both signals only when both are
factually true.

**Expected outcome**: Combined signals may lift conversion 3-8% for events with
genuine capacity constraints. If the seat limit is artificial, this test must not
be run — fabricated scarcity is a prohibited pattern.

---

## Error Handling

- If page variant (registration vs. replay) is not specified, ask before proceeding.
- If `event_date` or `expiresAt` is missing, flag it as a blocking issue — the
  countdown timer cannot function without a target date.
- If social proof data source is unavailable, recommend omitting the counter
  rather than using a fabricated number.
- If the page uses rejected CTA language (per page-cro Layer 3), flag immediately
  and provide approved alternatives.
- If the page contains a countdown timer on an offer with no real expiration,
  flag as an ethics violation and recommend removal.

---

## Related Skills

- `page-cro` — General 7-layer CRO framework for all page types; this skill extends the webinar registration and replay page-type guidance with component-level detail
- `replay-page` — Build the replay page from Zoom recording config; this skill provides CRO guidance for optimizing that page after generation
- `marketing-psychology` — Ethics Layer for urgency, scarcity, and social proof; all urgency and social proof patterns in this skill must comply with the marketing-psychology "Use With Care" and "Never Use" tiers
- `form-cro` — Registration form field optimization; use alongside this skill when the registration page includes an embedded form
- `voice-calibration` — CTA language validation and headline register checks
