# context-inject

OpenClaw plugin for multi-agent context architecture (feature 002).

## Current Status: Partial — See Limitations

The ContextEngine `prepareSubagentSpawn` hook **cannot modify the task string** sent to sub-agents. The API provides `parentSessionKey` and `childSessionKey` for session-level operations (like lossless-claw's expansion grants), but not for content injection.

## What Actually Works

The handoff contract system works through a **different mechanism**: the orchestrator includes `handoff-contract: <path>` in the `sessions_spawn` task string, and the sub-agent reads the contract file via its `read` tool. This is verified working:

- Copywriter reads draft contract → uses bound persona (Seth Godin x Wise Alchemist)
- Brand guardian reads gate contract → runs bound checks (kill list, Godin filter, etc.)
- Contract assertions run via `exec` on the orchestrator side after each delegation

## What This Plugin Does

1. **Session context delegation** (via `prepareSubagentSpawn`): Sets up LCM-compatible context grants between parent and child sessions. This allows the ContextEngine to manage context windows across delegated work.

2. **Post-completion cleanup** (via `onSubagentEnded`): Revokes context grants when sub-agents finish.

The plugin does NOT inject SOUL.md content or modify task strings — that's handled by the orchestrator SKILL.md instructions.

## Contract Assertion Verification

Assertions are verified by the **orchestrator**, not the plugin. After each `sessions_spawn` completes, the orchestrator runs:

```bash
python3 -c "
from compiler.engine.contract_assertions import run_assertions
import json
r = run_assertions('memory/pipelines/newsletter-YYYY-MM-DD/draft-handoff.yaml', '.')
print(json.dumps({'passed': r.passed, 'failures': [{'type': f.assertion_type, 'detail': f.detail} for f in r.failures]}))
"
```

## Installation

Add the plugin path to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "load": {
      "paths": ["/path/to/openclaw/plugins/context-inject"]
    }
  }
}
```

## Requirements

- OpenClaw Gateway v2026.3.7+
- Python 3.11+ with `pyyaml` (for contract assertion runner)
- `compiler/engine/contract_assertions.py` accessible from workspace root
