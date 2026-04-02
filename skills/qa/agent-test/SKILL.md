---
name: agent-test
description: "Use when running QA contract suites for skills, agents, or pipelines."
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /test-skill
  - command: /test-agent
  - command: /test-all
  - command: /test-pipeline
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
---

# Agent Test Runner

## Overview

Use the `agent-test` QA runner to discover scenarios, validate their target
structure, execute preconditions, trigger live runs, and evaluate resulting
artifacts from Claude Code or a shell session.

## Commands

- `/test-skill <name>` runs the scenarios for a single skill target.
- `/test-agent <domain>/<agent>` runs the scenarios for a single agent target.
- `/test-all [--tags smoke]` executes every discovered scenario that matches the
  supplied tag filters.
- `/test-pipeline <orchestrator>` runs the orchestrator pipeline contract.

## CLI

```bash
python3 skills/qa/agent-test/scripts/run.py --target newsletter
python3 skills/qa/agent-test/scripts/run.py --target marketing/brand
python3 skills/qa/agent-test/scripts/run.py --target skills/newsletter/sub-skills/brief --scenario brief-smoke --openclaw-profile dev --gateway-base http://127.0.0.1:19011
python3 skills/qa/agent-test/scripts/run.py --all --tags smoke
python3 skills/qa/agent-test/scripts/run.py --target webinar-orchestrator --pipeline
python3 skills/qa/agent-test/scripts/summary.py --date 2026-03-11
python3 skills/qa/agent-test/scripts/coverage.py --wave marketing-core --write-json
```
