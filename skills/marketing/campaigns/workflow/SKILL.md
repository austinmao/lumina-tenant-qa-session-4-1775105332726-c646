---
name: campaign-workflow
description: "Use when validating or dry-running the legacy campaign workflow contract."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /generate-campaign
---

# Legacy Campaign Workflow Contract

This compatibility skill preserves the historic `skills/marketing/campaigns/workflow` entrypoint for validation and pipeline dry runs.

The canonical implementation lives under `skills/campaigns/email/email-campaigns/`.
