# skills/project-health/

3 sub-skills for keeping the OpenClaw project clean and well-structured.

**Invoked by**: `/project-health` Claude Code skill (`.claude/skills/project-health/`)
**Also accessible via**: `/openclaw` orchestrator ("clean up the project", "find duplicates", "audit structure")

---

## Sub-skills

| Skill | Trigger | Purpose |
|---|---|---|
| `cleanup-artifacts` | Clean dev artifacts | Deletes `__pycache__/`, `*.pyc`, `.DS_Store`, stale preview HTML; prunes `memory/tmp/` per retention policy |
| `find-duplicates` | Find duplicate skills | Two-pass: content hash (md5) + semantic description overlap |
| `audit-structure` | Audit project structure | Checks kebab-case naming, depth violations, orphaned files, missing domain READMEs |

## Protected Directories

Never touched by any health skill:
- `memory/` (except `memory/tmp/` — cleaned per 7-day retention)
- `agents/**/memory/`
- `.beads/`
- `config/`

## Findings → Beads

All findings are logged as beads issues for human review. The skills never auto-delete anything from protected directories.

## Retention Policy (from `config/org.yaml`)

| Category | Retention |
|---|---|
| `memory/tmp/` | 7 days |
| `memory/logs/` operational logs | 30 days |
| Stale preview HTML (`web/public/preview-*.html`) | 1 day |
