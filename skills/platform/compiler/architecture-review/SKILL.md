---
name: architecture-review
description: Use when reviewing an entire codebase or major subsystem to understand structure, boundaries, ownership, dependency hotspots, dead code, layering problems, or to create a prioritized refactor roadmap before implementation.
---

# Architecture Review

## Overview

Use this skill before repo-wide refactors. The goal is to produce a structural diagnosis, not code changes.

Focus on:
- module boundaries
- coupling and cycles
- duplicated responsibilities
- hidden ownership
- dead code and abandoned paths
- mismatch between docs, tests, and runtime structure

## Repo Focus

For this repo, audit at least:
- `skills/`, `agents/`, and `scripts/` for workflow sprawl and duplicated integration logic
- `web/` for app boundaries, data flow, and build/test separation
- `workers/` and `mcp-send-email/` for isolated runtimes and integration contracts
- `tests/`, `specs/`, and `docs/` for drift from actual implementation

## Review Process

1. Inventory top-level domains and runtime entrypoints.
2. Map dependencies between domains using imports, CLI calls, and shared config.
3. Identify cycles, god modules, duplicated adapters, and cross-layer violations.
4. Flag code with no clear caller, stale specs, or overlapping ownership.
5. Produce a refactor roadmap ordered by leverage and risk.

## Heuristics

- Prefer stable boundaries around integrations and side effects.
- Separate orchestration from provider-specific adapters.
- Keep prompt/skill text, business rules, and executable scripts from drifting apart.
- Refactor toward smaller ownership units, not abstract frameworks for their own sake.
- Recommend deletion when code is unused or duplicated.

## Deliverable

Produce:
- current architecture summary
- boundary map
- top hotspots
- dead-code candidates
- risky coupling points
- recommended refactor phases

Each phase should include:
- objective
- affected paths
- expected risk
- verification strategy

## When Not To Use

Do not use this skill for one-file cleanup, bug fixing, or dependency upgrades without a broader structural question.
