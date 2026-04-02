---
name: codemod-refactor
description: Use when a TypeScript or JavaScript refactor is mostly mechanical across many files, such as renaming APIs, moving imports, rewriting call shapes, normalizing patterns, or applying an AST-based codemod instead of manual edits.
---

# Codemod Refactor

## Overview

Use this skill when the safest change is a repeatable mechanical transformation.

Default to AST-aware transforms for:
- identifier and API renames
- import path changes
- argument shape rewrites
- option object normalization
- JSX prop migrations
- replacing deprecated helpers across many files

## Preconditions

Before writing a codemod:
- define the exact before/after pattern
- identify the file set
- create or confirm characterization tests
- confirm the change is mechanical, not semantic

## Preferred Workflow

1. Select a narrow target pattern.
2. Collect 3-5 real examples from the repo.
3. Write the codemod against those examples.
4. Run it on a small subset first.
5. Review the diff manually.
6. Run tests and lint.
7. Expand to the full target set only after the subset diff is clean.

## Tooling Guidance

Prefer existing repo tooling first. If a transform needs custom code, keep it local and repeatable.

Good fits:
- `jscodeshift`
- `ts-morph`
- `recast`
- repository-local migration scripts

Avoid plain regex replacement when syntax context matters.

## Safety Rules

- Never mix semantic refactors into the codemod pass.
- Keep one codemod per concern.
- Preserve formatting when possible.
- Skip uncertain matches instead of guessing.
- Save a list of touched files for review.

## Deliverable

Return:
- target pattern
- transform used
- file scope
- skipped edge cases
- verification commands

## When Not To Use

Do not use this skill for architecture redesign, business-rule changes, or refactors that require deep per-file judgment.
