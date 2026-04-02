---
name: extract-profile
description: "Extract contact profile facts from conversation for memory persistence"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "📋"
---

# extract-profile

Extract structured profile facts from the conversation history. Run this after each meaningful exchange to surface data worth storing in contact memory.

## Extractable Fields

| Field | Type | Description |
|-------|------|-------------|
| `first_name` | string | Confirmed first name from conversation |
| `interests` | string[] | Topics mentioned with interest |
| `experience_level` | enum | never / curious / some / experienced |
| `motivation` | string | Primary reason for interest in retreat |
| `concerns` | string[] | Hesitations, fears, questions not yet answered |
| `location` | string | City/state if mentioned |
| `occupation` | string | If mentioned and relevant |
| `timeline` | string | When they might be ready to attend |
| `referred_by` | string | How they heard about the organization |

## Rules
- Only extract from what was explicitly stated — never infer or fabricate
- Mark uncertain extractions with `"confidence": "low"`
- Do not store medical history details — flag for medical-screening agent instead
- Keep `concerns` neutral — do not editorialize

## Output

```json
{
  "first_name": "Sarah",
  "interests": ["healing", "integration", "community"],
  "experience_level": "curious",
  "motivation": "recovering from burnout and looking for a reset",
  "concerns": ["is it safe", "what happens during the ceremony"],
  "timeline": "sometime in spring 2026"
}
```
