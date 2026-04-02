---
name: send-newsletter
description: "Use when validating or dry-running the legacy newsletter orchestration contract."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /send-newsletter
---

# Legacy Newsletter Contract

This compatibility skill preserves the historic `skills/marketing/email/newsletter` entrypoint for validation and pipeline dry runs.

The canonical implementation and richer contract set live under `skills/campaigns/newsletter/`.
