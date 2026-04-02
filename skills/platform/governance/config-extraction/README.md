# skills/config-extraction/

2 sub-skills for finding and replacing hardcoded organizational values.

**Invoked by**: `/config-extraction` Claude Code skill (`.claude/skills/config-extraction/`)
**Also accessible via**: `/openclaw` orchestrator ("scan for hardcoded values", "replace hardcoded values")

---

## Sub-skills

| Skill | Trigger | Purpose | Deps |
|---|---|---|---|
| `scan-hardcoded` | Scan for hardcoded organizational values | 6-category scan across the entire repo | `jq` |
| `replace-hardcoded` | Replace hardcoded values with config references | Category-by-category guided replacement | `jq` |

## Scan Categories

1. **Domain/URLs** — `example.org` references (config: `identity.domain`, `identity.homepage`)
2. **Email addresses** — `@example.org` addresses (config: `contact.email`, `contact.agent_email`)
3. **Org identity** — org name, legal entity, address (config: `identity.*`)
4. **Slack channels** — hardcoded channel names (config: `slack.*`)
5. **Service IDs** — Typeform form IDs, Airtable base IDs (config: `integrations.*`)
6. **Brand colors** — hex color codes (config: `brand_colors.*`)

## Exclusions

The scanner never flags:
- `config/org.yaml` itself
- `skills/org-config/SKILL.md` (the agent-facing cache)
- Brand/web reference YAMLs (`brands/your-brand/tokens/design-system.yaml`, `docs/web/web-ref.yaml`)

## Config Reference

All values live in `config/org.yaml`. Agents access them via the `org-config` skill (inlines top 15 constants at ~24 token overhead). See `docs/technical/config.md` for the full constant reference.
