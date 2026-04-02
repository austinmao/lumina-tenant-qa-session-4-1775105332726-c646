---
name: handoff-to-human
description: "Escalate conversation to a human operator via Slack handoff when escalation triggers are detected"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "🤝"
---

# handoff-to-human

Trigger a human handoff when an escalation condition is detected. This creates a handoff ticket, posts a Block Kit notification to #lumina-handoffs, and pauses autonomous replies for critical/high priority cases.

## Escalation Triggers & Priorities

| Trigger | Priority | Action |
|---------|----------|--------|
| Suicidal ideation, psychosis, mania | critical | Stop autonomous replies immediately |
| Legal threat ("I'll sue", "my lawyer") | critical | Stop autonomous replies immediately |
| Explicit request for a human | high | Acknowledge + pause autonomous replies |
| Medical advice request | high | Decline to advise + escalate |
| Payment dispute or refund request | medium | Acknowledge + escalate |
| High-intent purchase (explicit pricing/booking ask) | medium | Continue if within guardrails, escalate for closing |
| Explicit frustration after 2+ exchanges | low | Offer human option, continue if declined |

## Output

Return structured handoff data for the relay to process:

```json
{
  "priority": "high",
  "reason": "Contact explicitly requested to speak with a human operator",
  "summary": "Sarah has been engaged for 4 exchanges about the March retreat. She is curious, high-interest, and now asking to speak with someone directly about pricing and application.",
  "recommended_next_reply": "Of course! I'm connecting you with someone from our team right now. They'll be in touch shortly.",
  "stop_autonomous_replies": false
}
```

## On critical/high priority

When `priority` is `critical` or `high`:
- Send the `recommended_next_reply` if provided
- Set `conversation.status = 'handoff'`
- Stop all further autonomous replies until operator resolves the ticket

## Crisis Protocol

For `crisis` intent classification:
1. Respond immediately: "I hear you. Your safety matters. Please call or text 988 (Suicide & Crisis Lifeline) right now."
2. Trigger handoff with priority=critical
3. Stop autonomous replies
4. Do NOT engage further on the crisis content — let trained professionals handle it
