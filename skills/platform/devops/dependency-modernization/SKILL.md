---
name: dependency-modernization
description: Use when auditing or upgrading project dependencies, deprecations, build tooling, or package drift across JavaScript/TypeScript and Python code, especially before or during a modernization refactor.
---

# Dependency Modernization

## Overview

Use this skill to audit dependency health and plan upgrades without blindly bumping versions.

Focus on:
- outdated packages
- deprecated libraries and APIs
- duplicate packages across workspaces
- toolchain drift
- security-sensitive transitive dependencies
- unnecessary dependencies that can be removed

## Repo Focus

Check:
- root `package.json`
- `web/package.json`
- `templates/email/package.json`
- `mcp-send-email/`
- Python dependencies in `pyproject.toml`
- any local scripts that assume specific CLI versions

## Workflow

1. Inventory package managers and manifests.
2. Identify outdated, deprecated, duplicated, and unused dependencies.
3. Group upgrades by risk:
   - patch and low-risk
   - minor but behavior-sensitive
   - major or migration-required
4. Read release notes for anything non-trivial.
5. Upgrade in small batches with verification after each batch.

## Commands To Consider

- `npm outdated`
- workspace-specific test commands
- Python package audit and lockfile checks if present
- repo search for deprecated APIs before version bumps

## Rules

- Do not mix broad dependency upgrades with architecture refactors in one diff.
- Upgrade the minimum set needed for each batch.
- Prefer removing unused dependencies over replacing them.
- Call out lockfile and CI impact explicitly.
- Treat auth, email, payments, and webhook libraries as higher-risk.

## Deliverable

Produce:
- dependency inventory
- grouped upgrade plan
- migrations required
- verification matrix
- rollback notes for risky upgrades

## When Not To Use

Do not use this skill for application-level code review or one-off bug fixes unrelated to dependency health.
