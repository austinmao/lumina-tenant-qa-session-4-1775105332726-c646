---
name: invite-to-imessage
description: "Invite qualified leads to continue the conversation on iMessage for a more personal channel"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "💬"
---

# invite-to-imessage

Send a warm, single-use iMessage invitation via SMS when a contact meets the qualification threshold for channel deepening.

## Trigger Conditions (ALL must be true)
1. `contact.reply_count >= 3` — they've engaged meaningfully
2. `contact.lead_stage` is `qualified` or `high_intent`
3. `contact.imessage_invited_at` is null — not yet invited
4. Contact is NOT suppressed

## Invitation Message Template

```
Hi {{first_name}}! Our conversations have been really meaningful. I'd love to continue on iMessage — it's a bit more personal and I can share more there. Feel free to text me at the same number from your iMessage app.
```

Customize for tone — keep it warm and brief (1-2 sentences). Never pressure.

## After Sending
- Record `imessage_invited_at` timestamp on contact
- Log to compliance events: type `opt_in`, source `imessage_invite`
- Note in conversation summary via memory-update

## Rules
- Never send if `imessage_invited_at` is already set — only invite once
- Never initiate mass iMessage invitations (rate cap: max 5 new iMessage convos/day)
- The invitation is sent via SMS (Twilio relay) — it is not an iMessage itself
- Only invite contacts who have shown genuine engagement (not just a single "hi")
