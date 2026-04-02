---
name: handoff-summary
description: "Generate a concise conversation summary for operator handoff context"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "📝"
---

# handoff-summary

Generate a concise, structured conversation summary from the last N messages. This summary is included in the Slack handoff notification so the operator has full context before taking over.

## Summary Structure

The summary should cover:
1. **Who they are**: First name, how they found the organization, relevant background
2. **What they want**: Primary interest or question
3. **Where they are**: Current lead_stage, number of exchanges
4. **Key context**: Any concerns, medical flags, emotional state, timeline
5. **Trigger**: Why the handoff was triggered
6. **Suggested next step**: What the operator should do first

## Length

100-200 words. Tight and scannable — the operator needs to respond quickly.

## Example Output

```
Sarah M. reached out after seeing an Instagram post about the March retreat. She's a healthcare professional, curious about plant medicine for burnout recovery — no prior ceremony experience. 4 SMS exchanges over 2 days. She just asked to speak with someone directly about pricing and enrollment.

Current stage: qualified (ready for handoff). She seems warm, open, and genuinely interested — not just browsing. Main concern: "is it safe given my background."

Trigger: Explicit request for human operator.

Suggested next step: Introduce yourself warmly, answer her safety question, then walk her through the application process.
```

## Rules
- Never include PII beyond first name and last initial in the Slack summary
- If medical concerns were raised, flag explicitly: "⚠️ Medical question raised: [brief description]"
- Keep tone neutral and factual — operators make their own assessments
- Reference message count and timespan for context
