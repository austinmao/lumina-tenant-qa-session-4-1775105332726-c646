---
name: replace-hardcoded
description: "Replace approved hardcoded organizational values with config/org.yaml references"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /replace-hardcoded
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["bd"]
---

# Replace Hardcoded Values

Replace approved categories of hardcoded organizational values with references to `config/org.yaml`.
Run `scan-hardcoded` first to get the categorized report. This skill operates on those results.

## Replacement Strategy by File Type

### SKILL.md and SOUL.md Files

These are Markdown consumed by OpenClaw agents. Agents read `config/org.yaml` or load `org-config` skill at runtime.

**Strategy**:
1. Add a note at the top of the skill body referencing org-config:
   ```
   > Organizational constants (emails, domain, Slack channels): load `org-config` skill or read `config/org.yaml`.
   ```
2. Replace hardcoded values with descriptive references:
   - `info@[the organization's domain]` → `the contact email (config/org.yaml: contact.email)`
   - `lumina@[the organization's domain]` → `the agent email (config/org.yaml: contact.agent_email)`
   - `#lumina-bot` → `the bot Slack channel (config/org.yaml: slack.bot_channel)`
   - `C0AHSENHJHG` → `the ops channel ID (config/org.yaml: slack.ops_channel_id)`
   - Typeform IDs → `the form ID (config/org.yaml: integrations.typeform_health_intake)`

**Exception**: Values in `description` frontmatter field stay literal (used for routing, not runtime).

### .tsx Email Templates

These are TypeScript files. Create a shared constants module.

**Strategy**: Create `templates/email/org-constants.ts`:
```typescript
// Organizational constants for email templates.
// Source of truth: config/org.yaml (for agents) and .env (for secrets).
export const ORG = {
  name: "[Organization name]",
  contactEmail: "info@[the organization's domain]",
  agentEmail: "lumina@[the organization's domain]",
  logoUrl: "[configured logo URL]",
  homepage: "https://www.[the organization's domain]",
  legalName: "[Organization legal name from config/org.yaml]",
} as const;
```
Then import `{ ORG }` in templates and replace literal strings with `ORG.contactEmail` etc.

### YAML Config/Reference Files

`brand-ref.yaml`, `web-ref.yaml` are reference docs, not runtime configs.

**Strategy**: Add a header comment:
```yaml
# Source of truth for runtime constants: config/org.yaml
# This file is a reference document — changes here do not affect agents.
```
Keep literal values in these files (they ARE reference config).

## Approval Flow

For each category from `scan-hardcoded` results:

1. Display:
   - Category name and occurrence count
   - List of affected files
   - Exact replacement strategy for this category
2. Ask: "Approve replacements for [category]? (yes/skip/edit)"
3. If **yes**: execute replacements for all files in that category
4. If **skip**: move to next category, create deferred beads issue
5. If **edit**: let user specify alternative strategy, re-present for confirmation

## Post-Replacement Verification

After each approved category:
1. For .tsx files: verify TypeScript syntax by checking for unclosed brackets/strings
2. For SKILL.md files: verify YAML frontmatter is still valid (check `---` delimiters intact)
3. If verification fails: revert the category's changes and report the specific error

## Beads Integration

Close the scan issue when replacements complete:
```bash
bd close bd-XXX --reason "Replaced N hardcoded [category] values in M files with config/org.yaml references"
```

Create deferred issues for skipped categories:
```bash
bd create "Deferred: [category] hardcoded values — not yet replaced" \
  --type task --priority 3 \
  --description "Skipped during guided replace session. N occurrences remain in: [file list]" \
  --labels "hardcoded,config-extraction,deferred"
```
