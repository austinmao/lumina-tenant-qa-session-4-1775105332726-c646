---
name: participant-prep
description: "Use when preparing a participant for retreat onboarding, next steps, and readiness."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /participant-prep
---

# Participant Prep

Use this skill for retreat onboarding, participant preparation, readiness reminders, and other programs-facing support work.

It exists as the `skills/programs/...` entrypoint so the skill catalog and discovery layer can represent the programs department directly.
