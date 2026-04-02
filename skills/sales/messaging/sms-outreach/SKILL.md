---
name: sms-outreach
description: >
  Draft and send SMS marketing messages and retreat reminders to the organization
  participants via Twilio. Use this skill when the operator asks to send an SMS
  campaign, text participants about an upcoming retreat, send a reminder, or
  check SMS delivery status. Always requires the operator's explicit approval before
  any message is sent.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TWILIO_ACCOUNT_SID
        - TWILIO_AUTH_TOKEN
        - TWILIO_PHONE_NUMBER
      bins:
        - curl
        - jq
    primaryEnv: TWILIO_ACCOUNT_SID
    emoji: "sms"
    homepage: https://www.twilio.com/docs/messaging
---

# SMS Outreach Skill

## Purpose

Send SMS messages to the organization retreat participants via Twilio. Supports
individual messages and batch campaigns. All messages require the operator's
explicit approval before sending. Recipients must be in the verified
Airtable participant list.

## Required Setup

Ensure the following are set in .env:
- TWILIO_ACCOUNT_SID — Twilio account identifier
- TWILIO_AUTH_TOKEN — Twilio auth token
- TWILIO_PHONE_NUMBER — the configured sending number

## Workflow: Draft to Send

### Step 1 — Draft
When asked to draft an SMS campaign or individual message:
1. Write the message text — keep it concise (SMS best practice: under 160 characters where possible; if longer, note it will segment)
2. Use the active brand voice: warm, personal, never pushy
3. Save draft to memory/drafts/YYYY-MM-DD-sms-[slug].md including: message text, intended recipient segment, phone number source
4. Post to the operator in #lumina-bot: "SMS draft ready: [preview of message]. Intended for [segment — e.g., 'all active participants']. Approx [N] recipients. Ready to send, or would you like to adjust?"

### Step 2 — Operator Approval
Wait for the operator's explicit confirmation. Do not send without a clear "yes," "send it," or equivalent in the current session.

### Step 3 — Send
On approval:
1. Query Airtable (use airtable-participants skill) to get phone numbers for the approved segment
2. Validate all numbers are in E.164 format (+1XXXXXXXXXX) before sending
3. Send one message per recipient via Twilio REST API
4. Log each send response (SID, status, error code if any)
5. On any error: note it and continue with remaining recipients; compile error list for the operator

### Step 4 — Log
After all sends complete:
1. Write send report to memory/logs/sends/YYYY-MM-DD-sms.md with:
   - Message text
   - Total recipients
   - Successful sends (SIDs)
   - Failed sends (number, error code, reason)
   - the operator's approval timestamp
2. Post summary to the operator in #lumina-bot

## Behavior Rules

- Never send to any phone number not in the verified Airtable participant list or explicitly provided by the operator
- Never send without the operator's per-campaign explicit approval
- Never use urgency language, pressure tactics, or scarcity framing in any SMS draft
- Always identify the organization in the message — recipients must know who is texting them
- Always include an opt-out path in any marketing or campaign SMS (e.g., "Reply STOP to unsubscribe")
- If a recipient replies STOP or UNSUBSCRIBE: flag to the operator immediately; update their Airtable record (with the operator's instruction)
- Log every send — never skip logging

## Voice Guidelines for SMS

SMS is brief. Make every word count in the active brand voice:

Good: "Hi [Name], we have a retreat coming up on [date] and would love to have you join us. Reply to learn more."

Not good: "Don't miss out! LIMITED SPOTS for our upcoming retreat! Act now!"

Sign messages clearly: "— [Organization name]" or "— [Operator name] at [Organization name]"

## Example Invocations

- "Text all active participants about the March retreat"
- "Send a reminder SMS to people who signed up for the February event"
- "Draft an SMS for anyone who hasn't completed registration"
- "Check if last week's SMS campaign was delivered"
- "Send a personal text to [name] about their registration"

## Twilio API Reference

Send an SMS:
```bash
curl -s -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  --data-urlencode "From=$TWILIO_PHONE_NUMBER" \
  --data-urlencode "To=+1XXXXXXXXXX" \
  --data-urlencode "Body=Message text here" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq .
```

Check message status by SID:
```bash
curl -s "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages/{MessageSid}.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq '.status, .error_code, .error_message'
```
