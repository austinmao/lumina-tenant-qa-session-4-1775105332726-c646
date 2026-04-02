---
name: validate-structure
description: "Use when validating SKILL.md or SOUL.md structure before shipping"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /validate-skill
  - command: /validate-agent
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Validate Structure

## Overview

Use `python3 skills/qa/validate/scripts/validate.py --target <path>` to run the
structural checks for a `SKILL.md` or `SOUL.md` file before shipping changes.

## Commands

- `/validate-skill <path>` validates a skill manifest.
- `/validate-agent <path>` validates an agent identity file.
