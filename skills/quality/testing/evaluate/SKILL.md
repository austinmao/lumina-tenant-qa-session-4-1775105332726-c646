---
name: evaluate-contracts
description: "Use when evaluating scenario, handoff, or pipeline contracts against existing outputs"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /evaluate
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Evaluate Contracts

## Overview

Use `python3 skills/qa/evaluate/scripts/evaluate.py` to evaluate scenario,
handoff, or pipeline contracts and write structured reports to `memory/logs/qa/`.
