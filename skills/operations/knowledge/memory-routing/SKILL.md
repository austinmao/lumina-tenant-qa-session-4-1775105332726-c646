---
name: memory-routing
description: "Decide how memory should be retrieved or stored in this workspace"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /memory-routing
metadata:
  openclaw:
    emoji: "🧭"
---

# Memory Routing

## Overview

Use this skill when deciding how memory is retrieved by default, when Mem0 is additive, and where new memory should be stored. `config/memory-routing.yaml` is the source of truth. If this file and any prose disagree, follow the YAML registry.

## Retrieval Order

1. Default retrieval is universal: use gateway `memory.search` over curated file memory for every implemented agent.
2. Search semantically across compact curated memory first: `MEMORY.md`, relevant `memory/topics/*.md`, and retained daily logs.
3. Direct full-file reads are reserved for memory maintenance, audit, or explicit operator-directed work. They are not the default response-time path.
4. If the current agent is in the enhanced tier declared in `config/memory-routing.yaml`, proactively use `memory-mem0` every turn against both the agent namespace and `shared`.
5. If the current agent is not in the enhanced tier but the task needs cross-agent or shared-domain context, perform an on-demand read-only `memory-mem0` search against the `shared` namespace only. Non-tier agents do not search proactively every turn, do not read agent-specific structured namespaces, and do not write to structured memory.

## Storage Decision Tree

Apply the first matching route from `config/memory-routing.yaml`:

1. `daily_log_only`
   Use for transient session notes, one-off task context, and low-value noise.
   Destination: `memory/YYYY-MM-DD.md`
2. `curated_file_memory`
   Use for durable agent-specific preferences, facts, and operating rules that fit in compact summary form.
   Destination: the relevant `MEMORY.md`
3. `topic_file`
   Use for durable, reference-heavy material that must stay human-readable but is too detailed for `MEMORY.md`.
   Destination: `memory/topics/<topic>.md`
4. `canonical_dual_write`
   Use for canonical shared policies or decisions that must be both human-readable and cross-agent retrievable.
   Destination: curated shared file memory plus Mem0 `shared`
5. `structured_memory`
   Use for durable shared cross-agent context that should be retrievable at runtime but does not need a canonical file mirror.
   Destination: Mem0 `shared`

Only enhanced-tier agents write to structured memory by default.

## Conflict Precedence

If curated file memory and Mem0 disagree on the same fact, Mem0 wins. Apply the Mem0 version for the current task and update curated file memory to match so the two layers do not drift.

## Failure Behavior

- Mem0 timeout or connection failure: stop waiting after 5 seconds, log the failure to `memory/logs/mem0-writes/YYYY-MM-DD.md`, and continue with file-memory context only.
- Gateway `memory.search` failure: log the failure to `memory/YYYY-MM-DD.md` and continue with compact explicit file reads only when the current task still needs the context.
- Successful retrievals are not logged.

## Output

Apply the routing policy consistently without adding local one-off retrieval rules to agent identity files.
