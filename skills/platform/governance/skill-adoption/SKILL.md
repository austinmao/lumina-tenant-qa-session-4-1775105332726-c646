---
name: skill-adoption
description: "Install a skill from the marketplace / find and install skill / adopt skill from skills.sh"
version: "1.0.0"
scan_exempt: governance-scanner
permissions:
  filesystem: none
  network: false
triggers:
  - command: /skill-adoption
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins: ["python3", "npx", "uvx"]
      env: ["SNYK_TOKEN", "OPENCLAW_GATEWAY_TOKEN"]
      os: ["darwin", "linux"]
---

# Skill Adoption Pipeline

Deterministic Lobster workflow for marketplace skill discovery, security scanning,
and governed installation. Implements: specs/058-skill-adoption-pipeline/.

## Overview

Searches the skills.sh marketplace for a skill matching the query, evaluates candidates
with quality gates, runs four parallel security scanners (Snyk, permission, config,
injection), applies a decision rule, prompts for operator approval, and installs the
skill into the local workspace via ClawScaffold. All run state is written to
`memory/skill-adopt-runs/{skill-slug}-{YYYYMMDD-HHMMSS}/`.

## Steps

### Step 1: Invoke the Lobster workflow

Invoke the Lobster pipeline for the skill-adoption workflow:

```bash
python3 scripts/lobster-run.py workflows/skill-adoption.lobster \
  --query '<search query>' \
  [--skill-url '<direct URL>'] \
  [--scan-mode quality|efficiency|simplicity]
```

If a direct `skill_url` is provided (e.g., `https://skills.sh/wshobson/agents/stripe-integration`),
the search step is skipped and the workflow fetches the skill directly.

### Step 2: Monitor pipeline stages

The workflow runs 16 stages:

1. **state-init** — Creates run directory; classifies source tier (A/B/C); writes meta.yaml
2. **init** — Validates prerequisites (bins: npx, uvx, python3; env: SNYK_TOKEN, OPENCLAW_GATEWAY_TOKEN)
3. **search** — Runs `npx skills find <query>` or resolves Tier A directly
4. **select** — Applies quality gates (install_count thresholds); writes selection.yaml
5. **download** — Fetches SKILL.md to staging area; runs toxic pre-filter (ClawHavoc patterns)
6. **parallel-scan** — Dispatches 4 scanners to Agent Squad (Snyk, permission, config, injection); Tier A skips this stage
7. **decide** — Applies Rule C across scanner results; writes decision.yaml with verdict: install|rebuild|blocked
8. **approval-gate** — Renders approval preview; requires operator confirmation
9. **install-or-rebuild** — Copies clean skill or runs OpenProse rewrite for warn verdicts; writes rebuild-diff.yaml if rebuilt
10. **clawscaffold-adopt** — Registers skill in governance catalog via ClawScaffold
11. **clawspec-generate** — Generates ClawSpec test scenarios for installed skill
12. **clawwrap-check** — Detects outbound.submit usage; registers ClawWrap target if found
13. **paperclip-register** — Registers skill in Paperclip governance; writes paperclip-ref.yaml
14. **e2e-test** — Runs ClawSpec smoke tests; pairwise regression if upgrading existing skill
15. **sync** — Regenerates .claude/skills/ wrappers via sync-skills-to-claude.sh
16. **notify-gateway** — Appends to skills-list-changed.flag; prints gateway reload hint

### Step 3: Review approval prompt

When the approval-gate step prompts:
- Review the skill details (name, publisher, trust score, scanner verdicts, verdict)
- Type `yes` to approve or `no` to abort
- If verdict is `rebuild`, review the proposed diff before approving

### Step 4: Restart gateway

After successful install, restart the OpenClaw Gateway to load the new skill:

```bash
openclaw gateway restart
```

## Tier Classification

- **Tier A** (openclaw, lumina): Parallel-scan is skipped; direct local install
- **Tier B** (trusted publishers: vercel-labs, anthropic, microsoft): install_count >= 10,000 required
- **Tier C** (all others): install_count >= 1,000 required; full scan + operator review mandatory

## Decision Rules (Rule C)

- Any `blocked` scanner finding → verdict: blocked (pipeline halts)
- Any `warn` + untrusted publisher → verdict: rebuild (OpenProse sanitizes the skill)
- All scanners clean → verdict: install

## Output

- `memory/skill-adopt-runs/{skill-slug}-{timestamp}/` — full run artifacts
- `skills/.../<name>/SKILL.md` — installed skill file
- `memory/skill-adopt-runs/{run}/paperclip-ref.yaml` — Paperclip governance reference

## Error Handling

- If SNYK_TOKEN or OPENCLAW_GATEWAY_TOKEN not set: pipeline halts at init with clear message
- If pre-filter detects ClawHavoc patterns: pipeline halts at download; prefilter.yaml written
- If verdict is blocked: nothing written to skills/; blocked-reason.yaml written
- If Agent Squad unavailable: falls back to sequential scanner dispatch (slower but safe)
- If Paperclip unreachable: logs SKIP to meta.yaml; continues non-blocking
