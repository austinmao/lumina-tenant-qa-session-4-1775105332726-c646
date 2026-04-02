---
name: classify-intent
description: "Classify inbound SMS message intent to route the conversation appropriately"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
metadata:
  openclaw:
    emoji: "🔍"
---

# classify-intent

Classify an inbound SMS message into one of the intent categories defined in the tenant config. Use this at the start of every inbound turn to route the conversation appropriately.

## Intent Taxonomy

Load intent taxonomy from `config/intents.yaml`.

The config defines intent categories, each with a name, description, example message, priority level, and optional escalation target. The `confidence_threshold` field sets the minimum confidence below which the skill should return `other`.

## Output

Return a JSON object:
```json
{
  "intent": "event_inquiry",
  "confidence": 0.92,
  "secondary_intent": "logistics_question"
}
```

## Rules (priority order, always enforced)
1. `crisis` always takes priority — if ANY crisis language is detected, return `crisis` regardless of other signals and follow the escalation action in the config.
2. `opt_out` takes second priority — escalate to compliance handler immediately.
3. When confidence is below the `confidence_threshold` defined in the config, return `other` and let response-compose handle gracefully.
