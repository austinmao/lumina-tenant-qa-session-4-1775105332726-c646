---
name: qualify-lead
description: "Evaluate retreat fit, interest, and readiness; advance lead_stage based on conversation depth"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "📊"
---

# qualify-lead

Evaluate the contact's fit, interest, and readiness based on the conversation history and extracted profile data. Advance their lead_stage when qualification criteria are met.

## Qualification Dimensions

Load qualification dimensions from `config/qualify-lead-dimensions.yaml`.

The config defines:
- **stage_transitions** — criteria required to advance through each pipeline stage
- **fit_signals_positive** — indicators that a contact is a good candidate
- **disqualification_signals** — surface to operator; do not auto-reject
- **qualifying_dimensions** — the five evaluation lenses: fit, interest, readiness, timing, budget

### Stage Framework (generic)

Five-stage pipeline: `signed_up` → `replied` → `engaged` → `qualified` → `high_intent`.
Special transitions: `any → handoff` (escalation trigger) and `any → suppressed` (opt-out).
Exact criteria for each transition are defined in the tenant config.

## Output

Return a JSON object:
```json
{
  "current_stage": "engaged",
  "recommended_next_stage": "qualified",
  "advance": true,
  "qualification_notes": "Contact has shared personal healing context and asked about March dates."
}
```
