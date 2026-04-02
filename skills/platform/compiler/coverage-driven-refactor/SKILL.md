---
name: coverage-driven-refactor
description: Use when refactoring risky or weakly-tested code and you need characterization tests, coverage gaps, and a safe sequence for changing behavior without breaking existing workflows.
---

# Coverage-Driven Refactor

## Overview

Use this skill when the code should be changed, but its current behavior is only partially understood.

The pattern is:
- identify high-risk modules
- add characterization tests first
- refactor behind that safety net

## Repo Focus

In this repo, prioritize modules that:
- trigger sends or outbound actions
- orchestrate multiple integrations
- depend on env vars or webhook payloads
- contain duplicated parsing or routing logic
- have few or no tests in `tests/` or `web/e2e`

## Workflow

1. Identify the module or subsystem to refactor.
2. Find current tests and actual call sites.
3. Add characterization tests for current behavior, including edge cases and failure paths.
4. Run the new tests and verify they fail when the behavior changes.
5. Refactor in small slices.
6. Run focused tests after each slice, then the broader suite.

## Characterization Targets

Capture:
- input/output contracts
- side-effect triggers
- error handling
- env/config fallbacks
- serialization and parsing behavior
- approval-gated paths

## Verification

Use the smallest proving command first, then broaden:
- targeted `vitest` test file
- targeted `pytest` test file if Python path is involved
- broader suite for the touched area

If coverage tooling exists, use it. If it does not, use test presence plus behavior mapping as the practical proxy.

## Deliverable

Provide:
- risky areas selected
- tests added or proposed
- behavior now locked in
- safe refactor order
- remaining untested edges

## When Not To Use

Do not use this skill for greenfield feature work or for purely mechanical codemods that do not need behavior discovery.
