---
name: scan-hardcoded
description: "Scan the project for hardcoded organizational values — names, emails, URLs, colors, channel IDs, form IDs"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /scan-hardcoded
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: ["bd"]
---

# Scan Hardcoded Values

Find all hardcoded organizational constants that should reference `config/org.yaml` instead.
Run before `replace-hardcoded` to get the full categorized report.

## Excluded from Scan (Intentional Hardcoding)

These files MAY contain the patterns below — do NOT flag them:
- `config/org.yaml` — the source of truth itself
- `skills/org-config/SKILL.md` — the intentional inline cache
- `skills/email-design-system/SKILL.md` — design system reference (intentional)
- `<brand_root>/tokens/design-system.yaml` — brand reference (intentional)
- `docs/web/web-ref.yaml` — web reference (intentional)
- `.env.example` — example env file (intentional)

## Scan Categories

### Category 1: Domain & URLs

Search for literal domain usage in SKILL.md, SOUL.md, and .tsx files:
- `[the organization's domain]`
- `[the configured community domain]`
- `zoom.[the organization's domain]`
- `media.[the organization's domain]`
- `[the configured sending domain]`
- `home.[the organization's domain]`
- `images.squarespace-cdn.com` (Squarespace CDN logo)

Replacement target: Reference `config/org.yaml` identity.domain, media.cdn_base, or media.logo_url

### Category 2: Email Addresses

Search in SKILL.md, SOUL.md, and .tsx files:
- `info@[the organization's domain]`
- `lumina@[the organization's domain]`
- `info@[the configured sending domain]`
- Any pattern matching `*@[the organization's domain]`

Replacement target: Reference `config/org.yaml` contact.email, contact.agent_email, contact.resend_from

### Category 3: Organization Identity

Search in SKILL.md, SOUL.md, and .tsx files:
- `508(c)(1)(a)` (legal entity reference)
- `non-profit church in Denver` (legal name)
- `"[Organization name]"` as standalone brand name (in template strings, not compound domain)

Replacement target: Reference `config/org.yaml` identity.name, identity.legal_name

### Category 4: Slack Channels

Search in SKILL.md and SOUL.md files:
- `#lumina-bot` or `lumina-bot` (without #)
- `#ops-onboarding` or `ops-onboarding` (without #)
- `C0AHSENHJHG` (channel ID)

Replacement target: Reference `config/org.yaml` slack.bot_channel, slack.ops_channel, slack.ops_channel_id

### Category 5: External Service IDs

Search in SKILL.md, SOUL.md, web-ref.yaml (informational), and .tsx files:
- Typeform form ID `C2GbeJsV`
- Typeform form ID `pCpKY5jE`
- Zoom meeting IDs (numeric, 9-11 digits embedded in URLs)

Replacement target: Reference `config/org.yaml` integrations.typeform_health_intake, integrations.typeform_webinar_survey

### Category 6: Brand Colors (in non-config files)

Search in SKILL.md, SOUL.md, and .tsx files only:
- `#8b7355` (email accent)
- `#f5f0ea` (body-bg)
- `#14B8A6` (web accent teal)
- `#1a1a1a` (text primary / header footer)
- `#333333` (text body)
- `#faf7f2` (hero bg)

Note: Colors in email-design-system, brand-ref.yaml, web-ref.yaml are intentional — skip those files.

Replacement target: Reference `config/org.yaml` brand_colors.* or the org-config skill

## Output Format

For each category:
```
### Category N: [Name]
Total occurrences: X across Y files

| File | Line | Hardcoded value | Replacement |
|---|---|---|---|
| skills/foo/SKILL.md | 42 | info@[the organization's domain] | org-config: contact.email |

Beads issue: bd-XXX
```

## Beads Integration

Create one beads issue per category with findings:
```bash
bd create "Hardcoded: [category] — N occurrences in M files" \
  --type task --priority 2 \
  --description "Scan found N hardcoded [category] values. Files: [list]. Use replace-hardcoded skill to execute." \
  --labels "hardcoded,config-extraction"
```

## Summary

```
## Hardcoded Values Scan — YYYY-MM-DD

Total: N hardcoded values across M files in 6 categories
Beads issues created: bd-XXX, bd-YYY, ...

By Category:
1. Domain & URLs: N occurrences
2. Email Addresses: N occurrences
3. Organization Identity: N occurrences
4. Slack Channels: N occurrences
5. External Service IDs: N occurrences
6. Brand Colors: N occurrences
```
