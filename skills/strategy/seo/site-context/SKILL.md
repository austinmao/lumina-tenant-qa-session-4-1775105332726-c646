---
name: site-context
description: "Switch to a specific site / set active site / which site am I working on"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /site
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      os: ["darwin"]
---

# Site Context Skill

Resolves the active website tenant and writes a session file that all downstream agents and skills read.

The most recent `/site <name>` call is authoritative for this workspace. Parallel workspaces maintain independent site context.

---

## Usage

### Set active site

```
/site tenant-b
/site tenant-a
/site example-platform
```

### Show current site

```
/site
```

---

## Behavior

### When called with a site name (`/site <name>`)

1. Look for the tenant config file. Check these paths in order:
   - `tenants/<name>/tenant.yaml` (standard location)
   - `tenants/<name>/site-config.yaml` (alternative when compiler tenant.yaml occupies the standard path)

2. If neither file exists, respond with:
   > Tenant '<name>' not found. Available tenants: [list directories in tenants/]

3. Read the tenant config YAML and validate required fields:
   - `site_id` (string)
   - `domain` (string)
   - `brand_root` (path, must end with `/`)
   - `site_dir` (path, must end with `/`)
   - `sanity.dataset` (string)
   - `vercel.project` (string)
   - `website.blueprint` (path)
   - `website.build_log` (path)

4. If any required field is missing, respond with:
   > Tenant '<name>' is missing required fields: [list missing fields]

5. Expand all `${ENV_VAR}` references by reading from the process environment. If an env var is not set, respond with:
   > Environment variable <VAR_NAME> is not set. Add it to ~/.openclaw/.env

6. Write the fully resolved config to `memory/site-context.yaml` with this header:
   ```yaml
   # Active site context — written by /site command
   # Last set: <ISO timestamp>
   # Source: tenants/<name>/<filename>
   ```

7. Confirm to user:
   > Active site set to **<name>** (<domain>)
   > Brand: <brand_root>
   > Dataset: <sanity.dataset>
   > Blueprint: <website.blueprint>

### When called without arguments (`/site`)

1. Check if `memory/site-context.yaml` exists.

2. If it exists, read and display:
   > Current site: **<site_id>** (<domain>)
   > Brand root: <brand_root>
   > Site dir: <site_dir>
   > Sanity dataset: <sanity.dataset>
   > Blueprint: <website.blueprint>

3. If it does not exist, respond with:
   > No active site set. Run `/site <name>` to set one.
   > Available tenants: [list directories in tenants/]

---

## How downstream agents and skills use site context

Any agent or skill that needs site-specific paths reads `memory/site-context.yaml`:

```yaml
# Example resolved content of memory/site-context.yaml
site_id: tenant-b
domain: example.com
brand_root: brands/tenant-b/
site_dir: sites/tenant-b/
sanity:
  project_id: abc123
  dataset: tenant-b
  api_version: "2025-01-01"
vercel:
  project: tenant-b-com
  team: team_xyz
analytics:
  ga4_property: G-XXXXXXX
website:
  blueprint: docs/website/tenant-b/blueprint.md
  build_log: docs/website/tenant-b/build-log.md
content_sources:
  senja: false
  airtable_retreats: false
  chroma_corpus: austin_teachings
  campaign_api: false
```

To resolve a brand file path: `<brand_root> + voice.md` = `brands/tenant-b/voice.md`
To resolve design tokens: `<brand_root> + tokens/design-system.yaml` = `brands/tenant-b/tokens/design-system.yaml`
To resolve blueprint: read `website.blueprint` directly

If `memory/site-context.yaml` does not exist when a downstream skill needs it, that skill should prompt: "No active site set. Run `/site <name>` first."

---

## Error Handling

- **Tenant not found**: List available tenants from `tenants/` directory
- **Missing required fields**: List specific missing fields with their expected types
- **Env var not set**: Name the specific variable and suggest adding it to `~/.openclaw/.env`
- **Malformed YAML**: Report the parse error and the source file path
