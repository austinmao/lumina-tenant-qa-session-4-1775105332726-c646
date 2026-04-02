---
name: openclaw-self-update
description: "Check for openclaw CLI updates and refresh docs/openclaw-ref.yaml when the version changes"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /openclaw-self-update
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["openclaw", "git", "curl", "jq"]
      env: []
      os: ["darwin", "linux"]
---

# OpenClaw Self-Update Skill

Keeps `docs/openclaw-ref.yaml` current whenever the OpenClaw CLI version changes.

## Trigger

Invoked by the main agent heartbeat (Check #7) when the installed openclaw version
differs from the version stored in `memory/openclaw-version.txt`.

## Steps

### Step 1: Read current and stored versions

```bash
CURRENT=$(openclaw --version 2>/dev/null | tr -d '[:space:]')
STORED=$(cat memory/openclaw-version.txt 2>/dev/null | tr -d '[:space:]')
echo "Current: $CURRENT | Stored: $STORED"
```

If `CURRENT == STORED`: respond HEARTBEAT_OK, stop here.

### Step 2: Fetch release notes for the new version

```bash
curl -s "https://api.github.com/repos/openclaw/openclaw/releases" \
  -H "Accept: application/vnd.github+json" \
  | jq '[.[] | select(.tag_name >= "'"$STORED"'") | {tag: .tag_name, date: .published_at, body: .body}]'
```

Extract the combined changelog body for all releases between `STORED` and `CURRENT`.

### Step 3: Read current docs/openclaw-ref.yaml

Read the full file at `docs/openclaw-ref.yaml`.

### Step 4: Update the YAML

Using the release notes, identify changes that affect any of these sections:

| YAML key | Watch for changes to... |
|---|---|
| `architecture` | Gateway port, workspace files, loading order, heartbeat interval |
| `agent_types` | New agent types, hook changes |
| `skills.schema` | New frontmatter fields, changed field names or valid values |
| `security.cve_*` | New CVEs — ADD as new keys (e.g., `cve_2026_XXXXX`); never remove old ones |
| `security.hardened_config` | Config key changes, new recommended settings |
| `security.clawhavoc_supply_chain` | Updated counts or new attack patterns |
| `token_optimization` | New session commands, changed model IDs, new savings techniques |
| `operations` | Changed CLI commands, new flags, updated install steps |
| `email_automation` | Changes to Resend skill versions or send limits |
| `deployment_checklist` | New required steps |

Rules for updating:
- **Add** new CVEs, new config keys, new CLI commands
- **Update** changed values (version numbers, model IDs, rate limits)
- **Never remove** security entries — old CVEs stay as historical record
- **Update** the `# Last updated:` comment at the top to today's date
- Keep the existing YAML structure and key hierarchy intact
- Do not add prose — only structured YAML facts

### Step 5: Write updated YAML

Write the updated content back to `docs/openclaw-ref.yaml`.

### Step 6: Update version tracking

```bash
echo "$CURRENT" > memory/openclaw-version.txt
```

### Step 7: Commit and push

```bash
git add docs/openclaw-ref.yaml memory/openclaw-version.txt
git commit -m "chore(docs): update openclaw-ref.yaml for v${CURRENT}

Auto-updated by openclaw-self-update skill on heartbeat.
Previous version: ${STORED} → New version: ${CURRENT}"
git push
```

### Step 8: Notify

Post to #lumina-bot (channel `C0AGX6LEV1A`):
```
🔄 *openclaw updated* — v{STORED} → v{CURRENT}
docs/openclaw-ref.yaml refreshed and committed.
Key changes: {1-3 bullet summary of what changed in the release notes}
```

## Error Handling

- If GitHub API returns non-200: log the error to `memory/logs/openclaw-update-errors.md`
  and notify the operator in #lumina-bot. Do NOT update the version file — retry next heartbeat.
- If `git push` fails: log the error, do not mark version as updated.
- If release notes contain no architecture/security/skill changes: still update the
  `# Last updated:` header and commit — confirms the check ran even if no changes needed.
