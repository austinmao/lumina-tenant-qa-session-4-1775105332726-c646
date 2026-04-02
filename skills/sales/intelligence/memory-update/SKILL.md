---
name: memory-update
description: "Persist extracted profile facts and conversation summary to contact memory"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "💾"
---

# memory-update

Persist profile facts extracted by `extract-profile` and a conversation summary to the contact's memory record. Run this after meaningful exchanges (typically every 2-3 messages or when new facts are learned).

## When to Run
- After learning the contact's first name
- After extracting interests, motivation, or concerns
- After any significant shift in the conversation (new topic, emotion, qualification advance)
- Before invoking handoff-to-human (so the operator has full context)

## What to Store

Merge new facts with existing memory. Never overwrite — append or update:

```json
{
  "contact_id": "uuid",
  "facts": {
    "first_name": "Sarah",
    "interests": ["healing", "integration"],
    "experience_level": "curious",
    "motivation": "recovering from burnout",
    "concerns": ["safety", "what to expect"]
  },
  "conversation_summary": "Sarah reached out after seeing an Instagram post. She's curious about plant medicine for burnout recovery. No prior ceremony experience. Interested in March or April retreat.",
  "last_updated": "2026-03-07T16:30:00Z"
}
```

## Rules
- Never store PII beyond first name (no last name, email, or address in memory)
- Never store API keys, credentials, or sensitive system data
- Keep conversation_summary under 200 words
- Medical flags (medication mentions) go to compliance notes only — not to general memory
- This is contact-specific memory — it never mixes with other contacts
