---
name: sales-sequences
description: >
  Full outbound message sequences for the organization's sales pipeline: welcome
  email (Trigger 1), booking confirmation + pre-call nurture (Trigger 2),
  post-call follow-up (Trigger 3), stage-change nurture emails, post-booking
  integration sequence, and cold lead re-engagement. Use this skill when you
  need the exact structure and timing for any sales sequence.
version: 1.0.0
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "sequence"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env: []
      bins: []
---

# Sales Sequences Skill

## Shared Rules (All Sequences)

- From: lumina@[the configured sending domain]; Reply-To: lumina@[the organization's domain]; CC: assigned rep
- Personalization tokens: {first_name}, {rep_first_name}, {retreat_name}, {call_date}
- No health claims in any sequence (see sales-messaging skill for safe language)
- Log every send to Attio with timestamp, channel, and next-action note
- CAN-SPAM: include physical address + unsubscribe link in every commercial email

---

## Sequence 1 — Welcome Email (Trigger 1: Lead Capture)

**Send:** Immediately on signup, target < 5 minutes
**Channel:** Email
**Automation:** AUTO-SEND

**Subject:** "Welcome — here's what the organization is about"
*(or personalized to their stated interest if known from form data)*

**Body structure:**
1. Open with a specific acknowledgment (their stated interest, or the act of reaching out)
2. 2–3 sentences: what the organization does and who it's for — specific, not generic
3. Soft CTA: invite them to book a complimentary discovery call (include Calendly link)
4. Closing: no pressure, set the tone ("I'm here when you're ready")
5. Sign-off + physical address + unsubscribe

**Do not:** Pitch a specific retreat, include pricing, or use urgency language.

---

## Sequence 2 — Booking Confirmation + Pre-Call Nurture (Trigger 2)

### Email 2a — Booking Confirmation (send immediately on Calendly confirmation)

**Subject:** "Your call is confirmed — [Date] at [Time]"

**Body:**
1. Confirm: date, time, Zoom link
2. 2–3 sentences: what to expect on the call (not a sales pitch — a preparation note)
3. Optional: "Feel free to come with any questions"
4. Sign-off

### Email 2b — Pre-Call Nurture (send 24h before the call)

**Subject:** "A little something before we connect [tomorrow]"

**Body:**
1. One piece of genuine value relevant to their stated interest
   (a short story, a reflection, a framework — NOT a product pitch)
2. One sentence of warmth about looking forward to the conversation
3. PS: reminder of call time + Zoom link

### iMessage 2c — Day-Of Reminder (send 1–2h before call; only if opted in)

**Text:** "Hey {first_name}, looking forward to our call at {time} today.
Here's the Zoom link: {zoom_link}. See you soon! — Lumina + {rep_first_name}"

---

## Sequence 3 — Post-Call Follow-Up (Trigger 3: Fireflies sync)

**Send:** Within 2 hours of call end
**Channel:** Email
**Automation:** AUTO-SEND
**Personalization required:** Must use Fireflies context (see fireflies-sync skill)

**Subject:** "Thank you for our conversation, {first_name}"

**Body structure:**
1. Open with 1–2 specific things discussed on the call
   (e.g., "You mentioned feeling stuck after years of trying [X]...")
2. Name the next step agreed on the call
3. Include any resources or materials the facilitator committed to sending
4. Soft CTA: the next concrete action (confirm interest, review retreat page,
   schedule a follow-up, consider the offer)
5. Approval gate note (internal): if any pricing or commitment was discussed,
   flag this email for rep review before adding any specific numbers

**Must not:** Use a generic template when Fireflies data is available.
If Fireflies data is unavailable, use the intake form context + a warm, honest
note acknowledging the conversation.

---

## Sequence 4 — Proposal Sent Follow-Up (Trigger 4: "Proposal Sent" stage)

### iMessage 4a — 48h check-in (if opted in)

**Text:** "Hey {first_name}, wanted to check in — did you get a chance to look
over the retreat details? Happy to answer any questions. — Lumina"

### Email 4b — 5-day nurture (if no response to 4a)

**Subject:** "One thing that often makes this clearer"

**Body:**
1. One story or testimonial from a past participant (using safe language:
   "One guest shared that..." with explicit disclaimer that results vary)
2. Re-state the next step without re-pitching
3. Low-pressure close: "Whenever you're ready, I'm here"

---

## Sequence 5 — Post-Booking Integration (Trigger 4: "Won — Booked" stage)

### Email 5a — Booking Confirmation (send immediately)

**Subject:** "You're in — here's everything you need to know"

**Body:**
1. Confirm retreat name, dates, location
2. What to expect next (prep materials, pre-retreat call, community access)
3. Primary contact for questions (rep name + email)
4. Housekeeping: payment confirmation, cancellation policy

### Email 5b — Welcome to the Community (send day 2)

**Subject:** "Welcome to the organization family, {first_name}"

**Body:**
1. Personal welcome from Lumina + rep
2. Brief note on the transformation journey ahead (experiential language only)
3. Any community access details (Circle, Slack, group chat)

### Email 5c — Preparation Guide (send day 7)

**Subject:** "Your preparation guide for {retreat_name}"

**Body:**
1. Practical preparation information
2. What to bring / what not to bring
3. Health and logistics reminders
4. Pre-retreat call or intake form link (if applicable)

### iMessage 5d — Check-In (send day 14; if opted in)

**Text:** "Hey {first_name}, how are you feeling about the retreat?
Any questions coming up as you prepare? — Lumina + {rep_first_name}"

---

## Sequence 6 — Cold Lead Re-Engagement (90-day queue)

**Trigger:** 90 days since last meaningful engagement; meaningful event required
**Channel:** Email (primary); iMessage (if opted in, secondary)
**Automation:** Trigger-based only — never calendar-based

**Qualifying events for re-engagement:**
- New retreat dates announced
- Seasonal relevance (e.g., "heading into winter")
- A relevant piece of content or news
- A personal milestone the contact mentioned (anniversary, birthday if known)

### Email 6a — Re-engagement opener (day 0)

**Subject:** "[Specific event hook]"

**Body:**
1. Open with the meaningful event — make it feel natural, not forced
2. "Wanted to make sure we didn't drop the ball on our end" — honest, no guilt
3. One question that re-invites them into conversation
4. Soft CTA: "If the timing feels right, I'd love to reconnect"

### Email 6b — Value email (day 7, if no response)

**Subject:** "Something I thought you'd find useful"

**Body:**
1. One genuinely valuable piece of content (insight, story, resource)
2. No pitch. No CTA beyond "hit reply if this resonates"

### Email 6c — Gentle sunset (day 14, if no response)

**Subject:** "Keeping our list clean"

**Body:**
1. Honest: "I don't want to keep sending emails you're not finding useful"
2. One-click re-engagement link (Calendly or a simple form)
3. "If I don't hear from you by [date], I'll move you to our quarterly digest
   instead — no hard feelings either way"

After 6c with no response: move to quarterly digest cadence only.
Do not delete the Attio contact.
---

## Technical Rendering

This skill defines message structure and copy for all sales sequences. The copy
is composed in working memory and posted to Slack/Attio for review. When a
sequence email is approved for live send as branded HTML, use the shared render
pipeline:

```
templates/email/render.ts
```

### How to invoke the dispatcher

```bash
RESEND_API_KEY="$RESEND_API_KEY" \
RESEND_TRANSACTIONAL_FROM="$RESEND_TRANSACTIONAL_FROM" \
RESEND_TRANSACTIONAL_REPLY_TO="$RESEND_TRANSACTIONAL_REPLY_TO" \
  npx tsx templates/email/render.ts < /tmp/send-input.json
```

The stdin JSON must include a `templateName` field and a `participants` array:

```json
{
  "templateName": "sales-welcome",
  "participants": [{ "firstName": "Jordan", "email": "jordan@example.com" }],
  "dryRun": false
}
```

### templateName registry (sales domain)

| Sequence email | `templateName` value | Template file |
|---|---|---|
| Welcome email (Sequence 1) | _not yet created_ | needs `templates/email/sales/SalesWelcome.tsx` |
| Booking confirmation (Sequence 2a) | _not yet created_ | needs `templates/email/sales/BookingConfirmation.tsx` |
| Pre-call nurture (Sequence 2b) | _not yet created_ | needs `templates/email/sales/PreCallNurture.tsx` |
| Post-call follow-up (Sequence 3) | _not yet created_ | needs `templates/email/sales/PostCallFollowUp.tsx` |
| Post-booking confirmation (Sequence 5a) | _not yet created_ | needs `templates/email/sales/PostBookingConfirmation.tsx` |
| Post-booking welcome (Sequence 5b) | _not yet created_ | needs `templates/email/sales/PostBookingWelcome.tsx` |
| Preparation guide (Sequence 5c) | _not yet created_ | needs `templates/email/sales/PreparationGuide.tsx` |

### If no template exists yet

Before a sales email can be sent as branded HTML, its template must be created
in `templates/email/sales/` and registered in `templates/email/render.ts`.

Follow the "Adding a New Template" procedure in the `email-design-system` skill.
That skill contains the design tokens, React Email structural rules, and the
checklist that must be completed before any first live send.

Sales emails that are AUTO-SEND (see sales-messaging skill) must have their
template created and dry-run verified before the automation is enabled.
Do not activate AUTO-SEND on any sequence until the corresponding template
passes the email-design-system checklist.
