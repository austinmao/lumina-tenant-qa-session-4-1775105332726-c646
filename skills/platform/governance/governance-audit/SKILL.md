---
name: governance-audit
description: "Run governance audit on repo"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /governance-audit
metadata:
  openclaw:
    emoji: "\U0001F3DB"
    requires:
      bins: ["python3"]
      env: []
      os: ["darwin"]
---

# Governance Audit

Validates alignment across the runtime, catalog, and governance layers.

## What It Checks

- Every active runtime agent/skill has a governance record
- Every governance record passes schema validation
- Sub-skills have `parent_capability` set
- Active entrypoints have owner, approval, risk, and budget tiers
- No deprecated records have `paperclip.export: true`
- No duplicate canonical IDs or aliases
- Lifecycle status matches runtime presence

## How to Run

```bash
python3 scripts/scaffold.py governance-audit
```

## Output

- `PASSED` with zero errors
- `FAILED` with error count and details
- Warnings for coverage gaps (not blocking)

## Conflict Resolution

When the audit detects disagreements between governance and runtime:
1. The conflict is flagged as an error with both values shown
2. A human reviews and resolves each conflict case-by-case
3. The audit blocks promotion and export for unresolved conflicts
