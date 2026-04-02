---
name: campaign-strategy
description: >
  Plan email and SMS marketing strategy for the organization: list segmentation,
  launch calendar planning, A/B testing strategy, frequency cadence design, and
  behavioral automation trigger mapping. Use this skill when the operator asks for a
  campaign plan, segmentation design, A/B test strategy, or help deciding what
  to send to whom and when.
version: 1.0.0
metadata:
  openclaw:
    emoji: "strategy"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env: []
      bins: []
---

# Campaign Strategy Skill

## Overview

Design the strategic layer of the organization's email and SMS marketing:
who receives which messages, when, in what order, and how to test and improve
over time. This skill produces strategy documents, segmentation schemas, launch
calendars, and A/B testing plans. Copy production is handled by the copywriting
and email-sequences skills. This skill is the decision layer above them.

## Segmentation Design

Every list must be segmented on three axes simultaneously before any campaign
is sent. Sending the same message to the whole list is the most common cause of
poor campaign performance.

### Axis 1: Journey Stage

Define which stage best describes each contact's relationship with the organization:

- New subscriber: joined the list in the last 30 days; has not attended a
  retreat or booked a call
- Engaged non-buyer: on list more than 30 days, opening or clicking regularly,
  has not purchased or booked
- Past retreat guest: has attended at least one retreat; may or may not be
  on an active offer path
- Active coaching client: currently in a paid coaching relationship; messaging
  should support retention and upsell, not acquisition
- Lapsed: no email open in 60 to 90 days; route to re-engagement sequence
  before any campaign send

### Axis 2: Interest Signal

Record the interest category that best matches why this person joined the list:

- Yoga and movement
- Meditation and mindfulness
- Plant medicine and ritual work
- Somatic healing and nervous system work
- Burnout recovery and rest
- Executive and leadership transition
- Grief, loss, and life transition

Source interest signal from: opt-in form selection, lead magnet downloaded,
webinar attended, or retreat page visited.

### Axis 3: Behavior Signal

Track behavioral indicators that predict purchase intent:

- High-intent: opened 3 or more consecutive emails without clicking (reading
  but hesitating)
- Clicked retreat page but did not book
- Attended webinar but did not enroll
- Started application but did not submit
- Clicked pricing page on any offer

Contacts with behavior signals should receive targeted sequences, not standard
nurture. Their objection is specific — address it directly.

### Segment Matrix

Before any campaign: define the target segment as an intersection of all three
axes. Example:

"This campaign targets: Engaged non-buyers (stage) + burnout recovery (interest)
+ clicked retreat page but did not book (behavior). Do not send to past guests or
coaching clients."

Document the segment definition before any copy is produced.

## List Health Rules

### Per-Contact Rules
- Hard bounces: remove immediately; never retry a hard bounce
- Soft bounces: retry for maximum 3 sends; if still bouncing, suppress. A
  contact that soft-bounces on 3 consecutive sends is treated as a hard bounce.
- Unsubscribes: remove from all marketing lists within 10 business days (legal
  requirement); confirm suppression in Airtable
- TCPA opt-in records: must exist for every SMS contact; document source and
  date of consent in Airtable before any SMS is sent

### Aggregate Rate Monitoring (per-send)
After each send, check these thresholds:
- Hard bounce rate: must stay under 0.5%
- Soft bounce rate: must stay under 1.5%
- Combined bounce rate: must stay under 2.0%
- Unsubscribe rate benchmark: under 0.5% is healthy
- Unsubscribe flag at 0.5%: note in send log, review subject line and segment
- Unsubscribe alert at 0.8%: recommend pausing the campaign for list review
- If 0.8% unsub persists across 2+ sends: the segment or frequency is wrong —
  do not continue without adjusting
- If combined bounce exceeds 2.0%: PAUSE all follow-up sends, clean the list,
  diagnose cause (stale segment, bad import, domain reputation) before resuming

### Engagement-Based Suppression Tiers
- Active (opened/clicked in last 60 days): eligible for all sends
- Dormant (60-89 days no open): first touch must be a value-give or re-permission
  email — never promotional. Send promo only to those who open it, 2-3 days later.
- Cold (90-179 days no open): suppress from all promotional sends until
  re-engaged via the re-engagement sequence (see email-sequences skill)
- Dead (180+ days no open): suppress from all sends OR run a dedicated win-back
  sequence first. Do not include in any standard campaign.
- Sunset: contact completing the 3-email re-engagement sequence without response
  is removed from the active list

### Click Tracking and Link Hygiene
- ONE primary destination URL per campaign. All CTAs, inline links, and the
  header logo (during active campaigns) must point to this URL.
- Primary engagement metric: CTOR (Click-To-Open Rate) = Unique Clicks / Unique
  Opens. More meaningful than raw CTR because it measures intent among engaged
  readers.
- Historical CTOR baseline: 13.4% (Have a Good Trip Live, March 2026)
- Log CTOR alongside open rate and unsubscribe rate in every send report at
  memory/logs/sends/YYYY-MM-DD.md

## Launch Calendar Planning

When planning a launch for a retreat, program, or course:

### Timeline Back-Planning

Start from the retreat date or offer close date and work backward:

- Close date: set the actual last day to enroll or register
- Open cart: typically 7 to 14 days before close for retreats; 3 to 5 days for
  webinar-driven launches
- Announcement: 72 to 48 hours before open cart
- Pre-launch content: 2 weeks before announcement (content only, no pitch)
- List building push: 4 weeks before pre-launch (grow the list before the launch)

### Launch Calendar Output Format

Produce a dated calendar table:

| Date | Phase | Channel | Asset needed | Segment |
|---|---|---|---|---|
| [date] | Pre-launch | Email | Transformation story | All engaged |
| [date] | Pre-launch | Email | Behind-the-scenes | All engaged |
| [date] | Announcement | Email + SMS | You're Invited email + invitation SMS | All + SMS list |
| [date] | Launch Day AM | Email | Story-driven launch email | All engaged |
| [date] | Launch Day PM | Email + SMS | Proof-driven email + social proof SMS | All + SMS list |
| [date] | Launch Day Eve | Email | Urgency email (spots remaining) | Non-buyers |
| [date] | Close -48hr | Email | 48-hour deadline reminder | Non-buyers |
| [date] | Close -24hr | Email + SMS | 24-hour final call | Non-buyers + SMS |
| [date] | Close -2hr | Email | Last call (2 to 4 hrs before) | Non-buyers |

Note: past guests and active clients receive a tailored version of the
announcement and launch day emails only — not the full urgency sequence.

## A/B Testing Strategy

### Test Priority Order

Test in this sequence — never test two variables simultaneously:

1. Subject lines (highest leverage — affects open rate before anything else)
2. Offer structure (how the offer is framed: outcome-first vs. proof-first)
3. Proof format (SIPI testimonial vs. outcome statistic vs. story)
4. Send time (day of week and time of day)
5. CTA copy (button text and link placement)

### Subject Line A/B Test Protocol

Split: 15% receive version A, 15% receive version B, wait 4 hours, send version
to the winning 70%.

Success metric: open rate (not clicks — that is influenced by too many other
variables at this stage).

Minimum sample size: 200 recipients per variant to detect a 2-percentage-point
difference with 80% confidence. If list is under 400 contacts for this segment,
skip A/B and send best-judgment version.

### Structural A/B Test Protocol

Split: 50% receive version A, 50% receive version B. Send both simultaneously
to the full target segment.

Success metric: click-through rate or conversion (booking, application, purchase).

Document hypothesis before running: "I believe [version A/B] will outperform
because [reason grounded in framework]. Success condition: [metric] improves
by [X%]."

### Test Logging

After every test, record:
- Test date
- Asset type tested
- What varied (subject line wording, proof format, offer order, etc.)
- Winner and winning metric
- Margin of difference
- What this tells us about the audience

Build a running test log in memory/marketing/ab-test-log.md. Reference this
before recommending a test — never repeat a test that has already been run.

### the organization Historical Send Time Data

Use as baseline for all send time decisions. Override only with A/B test results
that show a 3+ percentage-point improvement.

| Day/Time | Open Rate | Use For |
|---|---|---|
| Sunday 9-10am MT | 40-47% | Value-deepener, reminder, high-priority sends |
| Thursday 9-10am MT | Best weekday | Initial promotional invitations, announcements |
| Monday-Thursday general | 13-20% | Avoid for initial sends; acceptable for urgency/follow-up only |

Default schedule for live event campaigns:
- Email 1 (Invitation): Thursday 9am MT, 7 days before
- Email 2 (Value deepener): Sunday 9am MT, 4-5 days before
- Email 3 (Urgency): 9am MT day before or morning of event
- Email 4 (Replay): 9am MT, 24-48 hours after event

All times Mountain Time (MT) unless the operator specifies otherwise.

## Frequency Strategy

### Standard (non-launch) Cadence

Email: 2 to 3 per week
SMS: 1 to 2 per week maximum; 0 to 1 is appropriate for most weeks

Content-to-pitch ratio: 3 value-give emails for every 1 promotional email.
Map out a rolling 4-week content calendar to maintain this ratio. If a launch
is coming, the give emails in the weeks before should seed the launch topic
(not be unrelated content).

### During-Launch Cadence

Email: daily minimum; 2 per day acceptable on cart-close day
SMS: 2 per day maximum on cart-close day; 1 per day on other launch days

After close: return to standard cadence immediately. No post-launch apology
emails or sympathy discounts.

### Suppression During Launch

Suppress these contacts from launch urgency sequences:
- Past retreat guests (send them a gratitude acknowledgment instead, not
  a closing urgency email)
- Active coaching clients
- Anyone who purchased during the launch (remove from sequence the moment
  they convert)

## Behavioral Automation Trigger Mapping

Map behavioral events to automatic sequence enrollments. This is the design
layer — implementation requires the operator's approval and the relevant email
platform's configuration.

| Trigger event | Sequence to enroll | Entry delay |
|---|---|---|
| New subscriber opt-in | Soap opera welcome sequence | Immediate |
| Clicked retreat page, no booking | Retreat consideration nurture | 1 hour |
| Attended webinar, no enrollment | Post-webinar follow-up (3 emails) | 24 hours |
| Started application, did not submit | Incomplete application nudge (2 emails) | 48 hours |
| Enrolled / booked | Confirmation + pre-retreat prep sequence | Immediate |
| Retreat concluded | Post-retreat integration sequence | 24 hours post-event |
| No open in 60 days | Re-engagement sequence | Immediate |
| No open after re-engagement email 3 | Suppress from all sends | 14 days after Email 3 |
| Anniversary of first retreat | Anniversary + referral sequence | Day of |

For each trigger, the marketing-agent defines the sequence logic. The
email-sequences skill produces the copy. the operator approves both before any
automation is activated.

## Steps

1. Identify the strategic question: segment design, launch calendar, A/B test
   plan, frequency audit, or automation trigger map
2. Gather from the operator: offer details, real dates, real capacity, current list
   size by segment (if known)
3. Produce the requested strategy document in the output format below
4. Flag any assumptions made (e.g., "I assumed list size of 500 — confirm
   before running A/B split sizing")
5. Identify which copy assets are needed next (route to email-sequences or
   copywriting skill)
6. Save strategy document to memory/marketing/strategy/YYYY-MM-DD-[slug].md

## Output Format

Strategy documents use this structure:
1. Summary: what this strategy covers and the goal it serves
2. Segment definition (axis 1, 2, and 3 for this campaign)
3. Calendar or plan table
4. Copy assets needed (list with skill to use for each)
5. A/B test plan if applicable
6. Success metrics: what numbers define a successful campaign for this offer
7. Risks and open questions: what the operator needs to confirm before execution

## Error Handling

- If list size for the target segment is unknown: note it in the strategy as
  an open question; do not proceed to A/B test sizing calculations until the operator
  provides the number
- If launch dates conflict with a previous campaign or major cultural moment:
  flag the conflict and recommend alternative dates before building the calendar
- If the offer details change after the calendar is built: rebuild the
  calendar — do not patch individual dates; a changed offer usually affects the
  entire arc
- If a proposed automation trigger could cause a contact to receive more than 2
  emails per day across all sequences combined: flag the frequency collision
  and recommend suppression logic to prevent it
