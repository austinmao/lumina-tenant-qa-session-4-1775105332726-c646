---
name: pipeline-triggers
description: >
  Identify and classify incoming sales events for the organization's four
  pipeline triggers: lead capture (form/newsletter), Calendly booking confirmed,
  post-Zoom call with Fireflies sync, and Attio deal stage change. Use this
  skill when a new event arrives and you need to determine which trigger it
  matches and which sub-agent should handle it.
version: 1.0.0
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "pipeline"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env: []
      bins: []
---

# Pipeline Triggers Skill

## Purpose

Classify incoming events and route them to the correct sales pipeline trigger.
This skill contains no API calls — it is a classification and routing layer
only. The director agent reads this skill and uses it to decide what to do next.

## The Four Triggers

### Trigger 1 — Lead Capture

**Matches when:**
- A new contact submits a newsletter opt-in form
- A new contact submits a website inquiry or application form
- A webhook from Typeform, Squarespace, or Mailchimp fires with a new subscriber
- An Attio contact is created with stage = "New Lead" or no stage set

**Owner:** agents/sales/lead-nurture

**Immediate actions (in order):**
1. Confirm contact does not already exist in Attio (check email dedup)
2. Create/update Attio contact: set stage to "New Lead"; log source
3. Identify assigned rep (from Attio or round-robin Ethan/Val if unassigned)
4. Auto-send welcome email within 5 minutes (see sales-sequences skill)
5. Log touchpoint in Attio contact notes

---

### Trigger 2 — Booking Confirmed

**Detection method:** Attio poll (NOT a direct Calendly webhook)

Calendly has a native Attio integration (confirmed active) that auto-creates
records in the **"Calendly Booking Events"** list and the **"Calendly Answers"**
list in Attio, and creates/updates People records for invitees. The agent polls
Attio for new entries in that list — no custom webhook handler is needed.

**Matches when (on each heartbeat poll):**
- A new record appears in the Attio "Calendly Booking Events" list
  with `status = active` and `created_at` after the last processed timestamp
- The linked People record has not yet been set to stage "Call Scheduled"

**Owner:** agents/sales/lead-nurture

**Immediate actions (in order):**
1. Read the new "Calendly Booking Events" record: extract invitee name, email,
   event start_time, event name, organizer (Ethan or Val)
2. Read any linked "Calendly Answers" records for intake form data
3. Look up the linked People record in Attio; update stage → "Call Scheduled"
4. Assign rep from organizer field (Ethan or Val); if unknown, default to ethan@
5. Auto-send booking confirmation email immediately (see sales-sequences skill)
6. Schedule pre-call nurture email for 24h before event start_time
7. Schedule day-of iMessage for 1–2h before (only if sms_opt_in: true in Attio)
8. Log all scheduled touches in Attio contact notes
9. Record the processed event ID to avoid re-processing on next poll

---

### Trigger 3 — Post-Call Fireflies Sync

**Matches when:**
- A Fireflies.ai summary appears in Attio for a contact
- A Zoom call recording is synced to Attio with transcript data
- A meeting record in Attio is updated with call notes from Fireflies

**Owner:** agents/sales/enrollment

**Immediate actions (in order):**
1. Read the Fireflies summary from Attio (meetings / call_recordings endpoint)
2. Extract: pain points named, goals stated, objections raised, commitments made
3. Identify assigned rep from Attio contact record
4. Create a Deal in Attio (see deal-management skill for schema)
5. Auto-send personalized post-call follow-up email within 2 hours
   (must reference specific details from Fireflies — no generic templates)
6. Log Fireflies summary link in Attio deal notes

---

### Trigger 4 — Deal Stage Change

**Matches when:**
- An Attio deal stage field is updated

**Owner:** agents/sales/enrollment (or agents/sales/pricing-yield for pricing stages)

**Stage-specific routing:**

| Stage | Owner | Automation |
|---|---|---|
| Proposal Sent | enrollment | Auto-send 48h iMessage check-in; 5-day nurture email if no response |
| Negotiating | enrollment | Draft objection response → flag for rep review → do NOT auto-send |
| Objection Raised | enrollment | Draft response → flag for rep review → do NOT auto-send |
| Closing | enrollment | Draft closing message → rep approval REQUIRED → do NOT auto-send |
| Won — Booked | enrollment | Auto-send booking confirmation sequence |
| Lost — Not Moving Forward | lead-nurture | Add to 90-day re-engagement queue; no immediate follow-up |

## Classification Ambiguity Rules

- If an event matches multiple triggers (e.g., a new Calendly booking AND a
  Fireflies meeting appear for the same contact in the same poll cycle),
  process triggers in order: 1 → 2 → 3 → 4.
  Never process the same event twice for the same contact.
- If a contact's stage in Attio does not match the expected stage for the
  trigger, log the discrepancy in Attio notes and proceed with the trigger
  as received (do not assume stage order was skipped intentionally).
- If the assigned rep cannot be determined from Attio, default to
  ethan@[the organization's domain] and flag for manual rep assignment.

## Compliance Pre-Check

Before any trigger action executes:
- Verify contact does not have a do-not-contact flag in Attio
- Verify iMessage opt-in (sms_opt_in: true) before any SMS/iMessage action
- Verify no medical/intake data is included in any outbound message
