---
name: audit-structure
description: "Audit project directory structure, naming conventions, orphaned files, and domain READMEs"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /audit-structure
metadata:
  openclaw:
    emoji: "📐"
    requires:
      bins: ["bd"]
---

# Audit Structure

Systematic audit of directory layout, naming conventions, and file organization.

## Step 1: Naming Convention Check

### Agent directories
- Pattern: `agents/<domain>/<function>/`
- Rule: lowercase, hyphen-separated, max 3 nesting levels
- Flag: directories with underscores, camelCase, spaces, or >3 nesting levels

### Skill directories
- Pattern: `skills/<name>/SKILL.md` or `skills/<domain>/<name>/SKILL.md`
- Rule: kebab-case directory names only
- Flag: directories with underscores, camelCase, or spaces

### Claude Code sub-agents
- Pattern: `.claude/agents/<descriptive-name>.md`
- Rule: kebab-case filenames
- Flag: files not following this pattern

## Step 2: Orphaned File Detection

### Unreferenced scripts
- List all files in `scripts/`
- Check if each is referenced in any SKILL.md, SOUL.md, CLAUDE.md, or docs/
- Flag scripts not referenced anywhere

### Unreferenced docs
- List all files in `docs/`
- Check if each is referenced in CLAUDE.md, agent-registry.md, or any skill/agent
- Flag docs not referenced anywhere

### Stale scaffold directories
- Find `agents/**/` directories containing only `.gitkeep`
- Cross-reference with `docs/agent-registry.md` rollout plan phases
- Flag scaffolds not assigned to any rollout phase

## Step 3: Directory Depth Check

Flag any path exceeding 3 levels of nesting under top-level directories:
```
agents/domain/agent/subdir/  ← 4 levels = violation
skills/domain/skill/subdir/  ← 4 levels = violation
```

Exception: `skills/newsletter/sub-skills/*/` is a documented pattern (pre-approved).

## Step 4: Domain README Check

For domains with 2+ agents, verify `agents/<domain>/README.md` exists.
Scale threshold: 20+ total agents requires domain-level index files.

Current domains to check:
- `agents/marketing/` — 8+ agents → needs README.md
- `agents/sales/` — 5+ agents → needs README.md
- `agents/programs/` — 4+ agents → needs README.md
- `agents/operations/` — 2+ agents → needs README.md
- `agents/frontend/` — 2+ agents → needs README.md

## Step 5: Summary Report

```
## Structure Audit — YYYY-MM-DD

### Naming Violations: N
[name] → suggested-fix

### Orphaned Files: N
[path] — recommendation: delete | move to docs/artifacts/ | document

### Depth Violations: N
[path] — suggested flattening

### Missing Domain READMEs: N
agents/[domain]/ — N agents, no README.md

### Beads Issues Created: N
bd-XXX: [title]
```

## Beads Integration

Create beads issues for each category with findings:
```bash
bd create "Structure: [category] — N violations" \
  --type chore --priority 3 \
  --description "[specific items with paths and recommended actions]" \
  --labels "structure,project-health"
```
