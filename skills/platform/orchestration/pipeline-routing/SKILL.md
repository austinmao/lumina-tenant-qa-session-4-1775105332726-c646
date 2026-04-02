---
name: pipeline-routing
description: "Classify incoming work and select a ClawPipe pipeline config"
version: 1.0.0
permissions:
  filesystem: read
  network: false
triggers:
  - command: /route-pipeline
metadata:
  openclaw:
    emoji: "🔀"
    requires:
      bins: []
      env: []
    cognition:
      complexity: medium
      cost_posture: economy
      risk_posture: low
---

<!-- oc:section id="skill-overview" source="catalog/skills/pipeline-routing.yaml" checksum="6005b3c8df58" generated="2026-03-28" -->
Classify incoming work (issue context, conversation thread, or event) into a route classification, resolve it to a ClawPipe pipeline config path via the pipeline registry, assess priority, and assemble pipeline input context.
<!-- /oc:section id="skill-overview" -->

## Steps

1. **Load pipeline registry** from `config/pipeline-registry.yaml`.
2. **Extract classification signals** from the incoming work item:
   - Parse `title`, `description`, `labels`, and `keywords` from the source.
   - Match against each route's `keywords` and `labels` arrays in the registry.
   - Score each route by match count; select the highest-scoring route.
3. **If no route matches** (score = 0 for all routes):
   - Return `{ "status": "needs_input", "message": "No matching pipeline config for this work type. Available routes: [list]. Provide classification or add a registry entry." }`
   - Log unroutable work to `memory/logs/routing/YYYY-MM-DD.yaml`.
4. **Assess priority** using urgency signals:
   - Check for deadline mentions, SLA tier labels, blocked-dependency flags.
   - Map to priority enum: `critical` | `high` | `normal` | `low`.
   - If no signals found, use the route's `default_priority` from the registry.
5. **Assemble pipeline input context**:
   - Extract: title, description, constraints, prior decisions from the work item.
   - Trim to the pipeline's configured token budget (default: 4000 tokens).
   - Include `required_input_fields` from the matched route as validation checklist.
6. **Return route result**:
   ```json
   {
     "status": "routed",
     "route": "<route-name>",
     "pipeline_config": "<config-path>",
     "priority": "<priority-level>",
     "input_context": { ... },
     "confidence": 0.0-1.0
   }
   ```

## Output

JSON object with fields: `status`, `route`, `pipeline_config`, `priority`, `input_context`, `confidence`. Status is either `routed` or `needs_input`.

## Error Handling

- If `config/pipeline-registry.yaml` is missing or malformed: return `{ "status": "error", "error": "Pipeline registry not found or invalid YAML at config/pipeline-registry.yaml" }`.
- If no route matches: return `needs_input` status (not an error — allows operator to classify manually).
- If required_input_fields are missing from the work item: include `missing_fields` array in the response for upstream validation.
