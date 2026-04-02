---
name: memory-mem0
description: "Store, search, or delete a memory in the structured memory layer"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /memory-mem0
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["curl", "jq"]
      env: ["OPENAI_API_KEY"]
      os: ["darwin"]
---

# Memory Skill — Mem0 Structured Memory Layer

Base URL: `http://localhost:19010`

This skill provides store, search, and delete operations against the self-hosted Mem0 memory service. Agents load this skill contextually. Proactive searches happen before every response (see agent SOUL.md). Explicit stores happen when the operator makes a durable decision.

---

## Namespace Convention

Every memory belongs to exactly one namespace. Choose based on scope:

| Namespace format | When to use | Example |
|---|---|---|
| `<domain>-<agent>` | Decisions that apply to this agent only | `marketing-brand`, `sales-director`, `operations-coordinator` |
| `shared` | Decisions that should apply to ALL agents | Brand prohibitions, pricing decisions, infrastructure errors |

**Rule**: If the operator says something like "always do X" or "never use Y" without limiting it to one agent, store it in `shared`. If it's a pipeline-specific preference, use the agent namespace.

---

## Store Operation

Store a memory when the operator makes a durable decision, states a preference, or resolves an error that should persist across sessions.

Every memory write must also append to the write log (see Write Logging section below).

**Request**:
```bash
curl -s -X POST http://localhost:19010/v1/memories/ \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "<decision or fact to store>"}],
    "user_id": "<namespace>",
    "metadata": {
      "type": "<decision|preference|fact|error>",
      "source": "<conversation|seed>"
    }
  }' | jq .
```

**`type` values**:
- `decision` — an explicit choice the operator made (prohibited word, process change, policy)
- `preference` — how the operator likes things done (tone, format, communication style)
- `fact` — objective information (prices, dates, contacts, systems)
- `error` — a resolved infrastructure error to prevent recurrence

**Example — store a brand decision in shared namespace**:
```bash
curl -s -X POST http://localhost:19010/v1/memories/ \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Never use the word Breakthrough in copy. Use Realization, Opening, or Integration instead."}],
    "user_id": "shared",
    "metadata": {"type": "decision", "source": "conversation"}
  }' | jq .
```

**Response fields to log**:
- `id` — memory ID (save this for potential future deletion)
- `memory` — the stored text (confirm it captured the intent correctly)

---

## Search Operation

Search memory before every response using the user's message as the query. Search both the agent namespace and `shared`.

**Timeout rule**: If the search does not return within 5 seconds, log the timeout and proceed without memory context. Never block a response waiting for memory.

**Request — search agent namespace**:
```bash
curl -s "http://localhost:19010/v1/memories/search/?query=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "<query>")\
&user_id=<namespace>&limit=5" | jq '.results'
```

**Request — search shared namespace**:
```bash
curl -s "http://localhost:19010/v1/memories/search/?query=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "<query>")\
&user_id=shared&limit=5" | jq '.results'
```

**Simplified combined search pattern (use this)**:
```bash
MEM0_BASE="http://localhost:19010"
QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

AGENT_RESULTS=$(curl -sf --max-time 5 "${MEM0_BASE}/v1/memories/search/?query=${QUERY_ENC}&user_id=${AGENT_NS}&limit=5" 2>/dev/null)
SHARED_RESULTS=$(curl -sf --max-time 5 "${MEM0_BASE}/v1/memories/search/?query=${QUERY_ENC}&user_id=shared&limit=5" 2>/dev/null)

echo "$AGENT_RESULTS" | jq '.results[]?.memory' 2>/dev/null
echo "$SHARED_RESULTS" | jq '.results[]?.memory' 2>/dev/null
```

**Using results**: Inject the returned `memory` strings into your reasoning before generating a response. Higher `score` values (closer to 1.0) indicate stronger relevance. Ignore results with score < 0.5.

**Zero results**: If both searches return empty results, proceed normally — no action needed.

---

## Delete Operation

**NEVER delete a memory without the operator's explicit approval in the current session.**

Deletion is session-scoped. A prior-session approval never carries forward.

Before deleting: confirm the memory ID with the operator by showing the memory text and its ID. Do not proceed if the operator says anything ambiguous.

**Request**:
```bash
curl -s -X DELETE http://localhost:19010/v1/memories/<memory_id>/ | jq .
```

**After deletion**: Log the deletion to `memory/logs/mem0-writes/YYYY-MM-DD.md` with action: deleted, memory_id, reason, and the operator's approval timestamp.

---

## Write Logging

**Every memory write (store or delete) MUST append to the write log.** This is an audit requirement.

Log file: `memory/logs/mem0-writes/YYYY-MM-DD.md` (create if not exists)

**Append format**:
```
- [HH:MM MT] ACTION=<store|delete> namespace=<namespace> type=<type> source=<source> id=<memory_id> summary="<first 80 chars of stored content>"
```

**Example store log entry**:
```
- [14:23 MT] ACTION=store namespace=shared type=decision source=conversation id=mem_abc123 summary="Never use the word Breakthrough in copy. Use Realization, Opening, or Integration"
```

**Example delete log entry**:
```
- [14:45 MT] ACTION=delete namespace=shared type=decision source=conversation id=mem_abc123 summary="the operator approved deletion — superseded by new decision on 2026-03-07"
```

---

## Graceful Degradation

If Mem0 is unreachable (connection refused, timeout > 5s, or HTTP 5xx):

1. Log the failure: append to `memory/logs/mem0-writes/YYYY-MM-DD.md`:
   ```
   - [HH:MM MT] ACTION=search-failed namespace=<ns> error="<error message>" — continuing without memory context
   ```
2. Continue processing the user's request normally — do NOT block or delay the response
3. Do NOT notify the operator unless the failure persists across 3+ consecutive heartbeat cycles

The memory layer is supplemental context. Agents must function correctly when it is unavailable.

---

## Conflict Handling

Before storing a decision that may contradict a prior one:

1. Search Mem0 for related content: `query = "<topic> <key terms>"`
2. If a related memory is found, note the conflict in your response to the operator: "I found a prior memory that may conflict: [existing memory]. Storing your new decision and flagging the prior one."
3. Store the new decision (with `source: conversation`)
4. Optionally: store a note that the prior entry is superseded, referencing its ID. Do NOT delete the prior entry without the operator's explicit approval.

**Recency wins**: In search results, newer memories with higher relevance scores take precedence. The Mem0 service handles recency weighting automatically.
