---
name: sms-campaigns
description: >
  Plan and draft SMS marketing campaigns: retreat invitations, event reminders,
  urgency messages, and two-way conversational SMS. Use this skill when asked to
  draft an SMS message, plan an SMS campaign calendar, or design a two-way SMS
  engagement flow. All drafts require the operator's explicit approval and route
  through the sms-outreach skill before any message is sent.
version: 1.0.0
metadata:
  openclaw:
    emoji: "sms"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env: []
      bins: []
---

# SMS Campaigns Skill

## Overview

Design and draft SMS campaigns. SMS is the
highest-intimacy marketing channel — one step above a personal phone call.
Every message must feel like it comes from the operator personally, not from a brand.
This skill covers campaign planning, message drafting, timing strategy, and
two-way conversation design. No messages are sent from this skill — all sends
route through the sms-outreach skill with the operator's explicit approval.

## Compliance Prerequisites (verify before any draft)

Before drafting any SMS campaign:
1. Confirm all recipients have provided TCPA-compliant opt-in consent
2. Confirm opt-in records exist in Airtable for the target segment
3. Confirm the configured sending number is registered and compliant
4. If any of the above cannot be confirmed: stop and ask the operator before proceeding

Non-compliance with TCPA carries fines up to $1,500 per message per recipient.
This is non-negotiable — do not draft for non-consented lists.

## Message Types

### Invitation SMS

For retreat announcements, webinar invitations, and event openings.

Rules:
- 160 characters maximum for single-segment delivery
- Lead with the reader's name or a warm opener (not "Hey!" — too generic)
- State the single benefit or outcome, not the logistics
- Include one clear action (reply Y, click link, call number)
- Identify sender explicitly at the end
- Include opt-out for marketing messages

Structure: [Name or warm opener] + [one benefit or urgency hook] + [one action]
+ [— [Operator name] at [Organization name]] + [Reply STOP to opt out]

Example:
"Hi {first_name} — one spot opened for our March retreat. Want details?
Reply Y. — [Operator name] at [Organization name]. Reply STOP to opt out."
(Character count: 101)

### Urgency SMS

For final 24 to 48 hours of a launch. Maximum 2 SMS per day in this window.

Rules:
- Urgency must be real: state exact time, exact spots remaining, exact deadline
- Never use countdown timers, artificial scarcity, or fabricated limits
- One message: state the deadline, name what closes, give the link
- No multi-part urgency (do not send 5 SMS in a row on close day)

Structure: [Deadline] + [what closes] + [link] + [sender]

Example:
"Closes tonight 11:59pm PT — 2 spots left for the March retreat.
[link] — [Operator name] at [Organization name]"
(Character count: 87 + link)

### Reminder SMS

For day-of or 48-hour pre-event reminders to confirmed attendees.

Rules:
- Warm, practical tone — not marketing tone
- Include logistics: date, time, location or link
- One action if any (add to calendar, confirm attendance)
- Under 160 characters

Structure: [Name] + [reminder context] + [key logistics] + [sender]

Example:
"Hi {first_name} — see you Saturday! Retreat starts 9am PT at [location].
Reach out with any questions. — the operator"
(Character count: 97)

### Two-Way Engagement SMS

For conversations that invite a reply and branch based on response.

Design principle: the first SMS asks one yes/no or short-answer question. The
reply triggers a follow-up from the operator (or a defined response from the agent
with the operator's approval per conversation branch).

Step 1 — Draft the opening SMS (question or invitation)
Step 2 — Define response branches:
  - If YES or positive reply: draft follow-up (details, link, next step)
  - If NO or not interested: draft graceful exit ("Understood — I'll keep you
    in mind for future retreats. Reply STOP any time.")
  - If no reply after 48 hours: no follow-up SMS (do not chase)

Step 3 — Present all branches to the operator for review and approval before any
message in the conversation is sent

## Campaign Calendar Planning

When asked to plan an SMS calendar for a launch:

Standard launch SMS schedule (align with launch sequence emails):
- Pre-launch: 0 SMS (save SMS for launch and close)
- Announcement (72 to 48 hours before open): 1 SMS — "Something's coming
  [date]. Watch for it." — teaser only, no details
- Launch Day: 2 SMS — morning (retreat is open + link) + evening (social proof
  + spots count)
- Closing Day (final 24 hours): 2 SMS — 24-hour warning + final 2-hour call
- After cart close: 0 SMS (no post-close apology campaigns)

Total launch SMS per recipient: maximum 5 across the full sequence.

## Timing Rules

- Send window: 9am to 8pm local time of the recipient only
- Best performance windows: Tuesday to Thursday, 10am to 12pm or 6pm to 8pm
- Never send on Monday mornings or Friday evenings
- Never send more than 2 SMS per day per recipient during launches
- Standard (non-launch) maximum: 1 to 2 SMS per week per recipient

## Character Count Rules

- Single SMS: 160 characters (ASCII) or 153 characters (Unicode/emoji)
- Multi-part SMS (161+ chars): splits into 2 segments; both segments are billed
  and delivered separately — increases cost and reduces readability
- Best practice: keep under 140 characters to account for personalization token
  expansion (e.g., {first_name} becomes "Maria Elena" = 11 chars)
- Always count the final character count after substituting longest likely token
  value before approving a draft

## Steps

1. Confirm with the operator: message type, target segment, send date/time, any
   real urgency or deadlines to include
2. Draft the message(s) — full copy, under 160 characters, with tokens in
   curly-brace format
3. Count characters after substituting the longest likely personalization value
4. If message exceeds 160 characters: shorten before presenting; never present
   a multi-part draft without flagging it explicitly
5. For two-way campaigns: draft all response branches before presenting
6. Add annotation block: character count, timing recommendation, TCPA compliance
   note, opt-out path confirmation
7. Present to the operator; remind that send requires routing through sms-outreach skill

## Output Format

For each SMS draft, deliver:
- Message text with tokens in {curly_braces}
- Character count (worst case after token expansion)
- Send timing recommendation
- Opt-out path (if marketing message)
- For two-way: full branch tree (reply YES path, reply NO path, no-reply path)
- Annotation block
- Approval gate reminder: "Route through sms-outreach skill with the operator's
  explicit approval before sending."

## Error Handling

- If segment opt-in status is unknown: stop and ask the operator before drafting
- If the message exceeds 160 characters after all attempts to shorten: present
  it anyway but flag the overage explicitly and recommend splitting into two
  separate messages on different send windows instead of one multi-part SMS
- If a real deadline or capacity number cannot be confirmed: do not use urgency
  framing — revert to benefit-led message structure
- If a reply arrives outside a two-way campaign design: flag to the operator for manual
  response; do not auto-reply without the operator's instruction
