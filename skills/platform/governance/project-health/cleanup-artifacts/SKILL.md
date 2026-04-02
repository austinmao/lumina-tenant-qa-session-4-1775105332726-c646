---
name: cleanup-artifacts
description: "Clean up development artifacts, stale files, and temporary outputs from the project"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /cleanup
metadata:
  openclaw:
    emoji: "🧹"
    requires:
      bins: ["find", "bd"]
---

# Cleanup Artifacts

Remove development artifacts and stale operational files. NEVER touches `memory/` (except `memory/tmp/` per retention policy) or `.beads/`.

## Protected Directories (NEVER clean)

- `memory/` — all subdirectories and files **except** `memory/tmp/` (cleaned by retention policy below)
- `agents/**/memory/` — per-agent memory
- `.beads/` — issue tracker database
- `config/` — centralized configuration

## Step 1: Load Retention Config

Read `config/org.yaml` section `cleanup.retention_days`:
- `tmp_files`: days before temp files are deleted (default: 7)
- `operational_logs`: days before operational logs outside memory/ are pruned (default: 30)
- `stale_previews`: days before preview HTML files are deleted (default: 1)

## Step 2: Scan for Artifacts

### Always Delete (no approval needed)

- `__pycache__/` directories anywhere in the repo (except in `.beads/`)
- `*.pyc` files
- `.DS_Store` files not caught by .gitignore
- `*.tsbuildinfo` files
- `.wrangler/` directories

### Delete if Stale (check age against retention config)

- Files in `memory/tmp/` older than `tmp_files` days (exception to memory/ protection)
- Files in `agents/**/tmp/` older than `tmp_files` days
- `web/public/preview-*.html` older than `stale_previews` days
- `scripts/**/__pycache__/` directories (also covered by Always Delete above)

### Report Only (create beads issue, don't auto-delete)

- Untracked files in `web/scripts/` (may be intentional dev scripts — review first)
- Files larger than 10MB not in .gitignore
- Empty directories (excluding `.gitkeep` scaffolds)

## Step 3: Execute Cleanup

For "Always Delete" items:
1. List all items found with full paths
2. Delete them using `rm -rf`
3. Report: "Deleted N items in M categories"

For "Delete if Stale" items:
1. List items with age in days
2. Delete items older than retention threshold
3. Report: "Deleted N stale items (threshold: X days)"

## Step 4: Update .gitignore if Needed

Check if `__pycache__/` is globally excluded in `.gitignore`. If not, add a Python section:
```
# Python bytecode (global)
__pycache__/
*.pyc
*.pyo
```

## Step 5: Create Beads Issues

For "Report Only" items, create one beads issue per category:
```bash
bd create "Cleanup: [category] — N items found" \
  --type chore --priority 3 \
  --description "Found during project health scan. Items: [list]" \
  --labels "cleanup,project-health"
```

## Step 6: Summary Report

Output a structured report:
```
## Cleanup Report — YYYY-MM-DD

### Deleted
- __pycache__/: N directories
- Stale previews: N files
- memory/tmp/ stale: N files

### Beads Issues Created
- bd-XXX: [title]

### Protected (skipped)
- memory/: always protected (except tmp/)
- .beads/: always protected
```
