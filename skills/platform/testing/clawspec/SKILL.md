---
name: clawspec
description: "Run ClawSpec tests for agents and skills / generate test scenarios / check coverage"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /clawspec
metadata:
  openclaw:
    emoji: "\U0001F9EA"
    requires:
      bins: ["python3"]
---

# ClawSpec — Contract-First Test Runner

Run scenario-based tests against agents, skills, and orchestration pipelines.
Integrates with Opik for trace observability, drift detection, and baseline management.

## Prerequisites

- OpenClaw gateway running (`openclaw gateway status`)
- Python 3.11+ with `pyyaml` installed
- Optional: `OPIK_API_KEY` env var for trace enrichment and regression detection

## 1. Run Tests for a Specific Target

```bash
# Agent smoke tests
python3 skills/qa/agent-test/scripts/run.py --target agents/operations/coordinator --tags smoke
# Skill smoke tests
python3 skills/qa/agent-test/scripts/run.py --target skills/campaigns/newsletter --tags smoke
# Single named scenario
python3 skills/qa/agent-test/scripts/run.py --target skills/campaigns/newsletter --scenario sunday-service-smoke
# Evaluate assertions only (no gateway call — fast inner loop)
python3 skills/qa/agent-test/scripts/run.py --target skills/campaigns/newsletter --evaluate-only
# Pipeline contract
python3 skills/qa/agent-test/scripts/run.py --target agents/campaigns/campaign-orchestrator --pipeline
```

## 2. Generate Test Scenarios for Uncovered Items

Scans `agents/` and `skills/` for items missing `tests/scenarios.yaml`.

```bash
python3 scripts/clawspec-coverage-sweep.py --generate --dry-run   # preview only
python3 scripts/clawspec-coverage-sweep.py --generate              # write files
python3 scripts/clawspec-coverage-sweep.py --generate --force      # overwrite existing
```

Auto-detected tiers: `orchestrator` (delegates via `sessions_spawn`),
`interior-agent` (no delegation), `boundary-skill` (external channels),
`interior-skill` (pure logic, default).

## 3. Retrofit Existing Scenarios with Opik Assertions

Injects missing assertions (`no_span_errors`, `model_used`, `tool_sequence`) per tier.

```bash
python3 scripts/clawspec-coverage-sweep.py --retrofit --dry-run    # preview
python3 scripts/clawspec-coverage-sweep.py --retrofit               # apply
```

## 4. Check Coverage

The `--generate --dry-run` combination doubles as a coverage checker:

```bash
python3 scripts/clawspec-coverage-sweep.py --generate --dry-run
# Output: "[generate] found N items without test scenarios"
```

Coverage ledger: `docs/testing/coverage-ledger.yaml`
Assertion gaps: `memory/logs/qa/assertion-gaps.yaml`

## 5. Capture / Update Baselines

Baselines store percentile-based performance stats (duration, tokens, cost) from
Opik traces. Used for regression detection on subsequent runs.

```bash
# Capture baselines (skips items that already have baselines.yaml)
python3 scripts/clawspec-coverage-sweep.py --baseline

# Force-overwrite existing baselines
python3 scripts/clawspec-coverage-sweep.py --baseline --force

# Dry-run preview
python3 scripts/clawspec-coverage-sweep.py --baseline --dry-run
```

Baselines are stored at `<target>/tests/baselines.yaml` alongside `scenarios.yaml`.
Provisional baselines (single run) auto-promote to stable after 5+ runs.

## 6. Run Unit / Integration Tests

```bash
cd src && pytest tests/ -k clawspec -q
```

## Scenario File Format

Files live at `<agent-or-skill>/tests/scenarios.yaml`. Structure:

```yaml
version: "1.0"
target:
  type: agent                    # "agent" or "skill"
  path: agents/operations/coordinator
  trigger: agent:operations/coordinator
defaults: { timeout: 90, test_mode: true }
scenarios:
  - name: smoke-basic
    tags: [smoke, interior-agent]
    given: [{ type: file_absent, path: memory/drafts/artifact.md }]
    when: { invoke: "agent:operations/coordinator", params: { test_mode: true } }
    then:
      - { type: artifact_exists, path: memory/drafts/artifact.md }
      - { type: no_span_errors }
      - { type: llm_call_count, min: 1, max: 5 }
  - name: rejects-out-of-scope
    tags: [negative]
    when: { invoke: "agent:operations/coordinator do something forbidden" }
    then: [{ type: tool_not_permitted, tool: send_message }]
```

Assertion types: `artifact_exists`, `no_span_errors`, `model_used`, `tool_sequence`,
`tool_not_permitted`, `tool_not_invoked`, `llm_call_count`, `llm_judge`,
`token_budget`, `agent_identity_consistent`, `delegation_path`.

## Error Handling

| Message | Fix |
|---|---|
| `Trace not found for scenario` | Verify gateway is running: `openclaw gateway status` |
| `opik package not installed` | `pip install opik` |
| `clawspec_gen failed ... using minimal` | Run from repo root with `PYTHONPATH=.` |
| `p95 unreliable` | Need 10+ runs for stable percentiles; 20+ recommended |
| `Observability backend unavailable` | Opik unreachable or key invalid; tests still run without traces |
| `no baseline` in regression report | Run `--baseline` or let auto-baseline accumulate 5 runs |
