---
name: ralph
description: "Use when running the heartbeat-driven QA feedback loop for failed orchestrator outputs."
version: "1.0.0"
permissions:
  filesystem: write
  network: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Ralph QA Loop

## Overview

Use `python3 skills/qa/ralph/scripts/ralph.py` to detect newly produced
artifacts, evaluate them with the shared QA engine, re-invoke orchestrators in
fresh sessions when deterministic checks fail, and escalate persistent or
infrastructure failures.

## Commands

- Run a specific scenario contract:
  `python3 skills/qa/ralph/scripts/ralph.py --scenario-file skills/newsletter/tests/scenarios.yaml --scenario-name happy-path`
- Scan the default heartbeat watch paths:
  `python3 skills/qa/ralph/scripts/ralph.py`
- Override the watch set and retry budget:
  `python3 skills/qa/ralph/scripts/ralph.py --watch-path "/abs/path/*.md" --max-runs 2`

## Heartbeat Notes

- Ralph is intended for heartbeat-style polling of `memory/drafts/` and
  `memory/staging/`.
- State is written to `memory/logs/qa/ralph/`.
- Escalations use Slack when the Slack token env var is set and otherwise return
  a structured local fallback payload.
