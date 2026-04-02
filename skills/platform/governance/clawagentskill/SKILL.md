---
name: clawagentskill
description: "Adopt a skill from the marketplace / port a Claude Code agent to OpenClaw / scan a skill for security issues / find available skills and agents"
version: "0.1.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /clawagentskill
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["python3", "npx"]
      env: []
      os: ["darwin", "linux"]
---

# clawagentskill — Agent & Skill Discovery for OpenClaw

Standalone package for discovering, scanning, and adopting skills from the marketplace,
or porting Claude Code agents to OpenClaw SOUL.md format.

## Install

```bash
pip install -e clawagentskill/
```

## Commands

```
/clawagentskill find "payment processing"     — Search skills.sh + agent repos
/clawagentskill adopt "stripe integration"     — Full pipeline: discover → scan → approve → install
/clawagentskill port <github-url> dept/name    — Port Claude Code agent to SOUL.md
/clawagentskill scan path/to/SKILL.md          — Run 4 security scanners
/clawagentskill status                         — Show recent adoption runs
```

## Replaces

This skill replaces the legacy `scripts/lobster-skill-run.py` script.
The Lobster workflow at `workflows/skill-adoption.lobster` now calls
`python3 -m clawagentskill` directly.
