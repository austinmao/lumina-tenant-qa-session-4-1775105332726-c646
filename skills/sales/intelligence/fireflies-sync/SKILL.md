---
name: fireflies-sync
description: >
  Read Fireflies.ai meeting summaries and transcripts as synced into Attio CRM.
  Use this skill during Trigger 3 (post-Zoom call) to extract pain points, goals,
  objections, and commitments from a call recording so that the post-call follow-up
  email can be personalized. This skill reads from Attio only — it does not call
  the Fireflies API directly.
version: 1.0.0
permissions:
  filesystem: none
  network: true
metadata:
  openclaw:
    emoji: "transcript"
    homepage: https://docs.openclaw.ai/tools/skills
    requires:
      env:
        - ATTIO_API_KEY
      bins: []
---

# Fireflies Sync Skill

## Purpose

Fireflies.ai auto-syncs Zoom call recordings and summaries into Attio after
every call. This skill knows where to find that data in Attio and how to extract
the information needed to write a personalized post-call follow-up.

## Where Fireflies Data Lives in Attio

Fireflies has a native Attio integration (confirmed active). After every Zoom
call it auto-creates or updates a meeting record in Attio linked to the contact
by email match. OpenClaw reads this data — it does not sync anything.

- **Meeting records**: Attio meetings object, linked to contact via email
- **Call summary**: meeting record → `summary` or `description` attribute
- **Action items**: meeting record → `action_items` attribute or notes
- **Recording URL**: meeting record → `recording_url` attribute

## Extraction Steps

### Step 1: Locate the Meeting Record

Query Attio v2 for meetings linked to the contact:
```
POST /v2/objects/meetings/records/query
{
  "filter": {
    "filters": [
      {
        "attribute": { "slug": "linked_contacts" },
        "operator": "intersects",
        "value": { "target_object": "people", "slugs": ["<contact_slug>"] }
      }
    ]
  },
  "sort": [{ "direction": "desc", "attribute": "created_at" }],
  "limit": 5
}
```

Find the most recent meeting with `created_at` within the last 4 hours and
source or title containing "fireflies" or "zoom".

### Step 2: Extract Required Fields

From the meeting record, extract:

| Field to Extract | Source | Notes |
|---|---|---|
| Pain points named | summary field | Look for "challenges," "struggles," "dealing with" |
| Goals stated | summary field | Look for "wants," "hopes," "looking for," "goals" |
| Objections raised | summary field + action_items | Look for "concerns," "questions about," "hesitant" |
| Commitments made | action_items | What the facilitator promised to send/do |
| Next step agreed | action_items | What the lead agreed to consider or do |
| Retreat interest | summary | Which specific offering or date they discussed |
| Emotional tone | summary | Excited, cautious, skeptical, open — note for message tone |

### Step 3: Structure the Context Object

Build a context object to pass to the post-call email draft:

```json
{
  "contact_name": "<first name>",
  "call_date": "<YYYY-MM-DD>",
  "pain_points": ["<point 1>", "<point 2>"],
  "goals": ["<goal 1>", "<goal 2>"],
  "objections": ["<objection 1>"],
  "commitments_by_us": ["<what we said we'd send>"],
  "next_step_agreed": "<what they said they'd do>",
  "retreat_interest": "<retreat name or date>",
  "emotional_tone": "<excited|cautious|skeptical|open>",
  "fireflies_url": "<recording URL from Attio>",
  "assigned_rep": "<rep email>"
}
```

### Step 4: Validate Before Using

Before using the context to draft the follow-up:

- [ ] At least 2 pain points or goals extracted (if fewer, check if summary is incomplete)
- [ ] No medical diagnoses or clinical terminology included (HIPAA: omit from email)
- [ ] Objections recorded even if not fully resolved on call
- [ ] Fireflies URL captured for Attio deal note

If summary is incomplete (under 100 words), flag to the rep and send a generic
but warm follow-up instead — do not guess at what was said on the call.

## Privacy Rules

- Never include a contact's medication names, diagnoses, or mental health history
  in the extracted context or in any outbound message
- If the transcript contains the phrase "confidential" or the contact explicitly
  asked for privacy on any topic, omit that topic from the follow-up email
- Fireflies summaries are Attio data — treat as internal; do not forward the
  raw transcript to anyone outside the sales team

## Error Handling

| Condition | Action |
|---|---|
| No meeting record found in Attio within 60 min | Flag to rep; send generic warm follow-up |
| Fireflies summary is blank or <50 words | Flag to rep; use context from intake form only |
| Contact email doesn't match any Attio meeting | Check for email variants; if none found, flag to rep |
| Summary contains clinical/medical detail | Extract only non-medical information; omit clinical detail |
