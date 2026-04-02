# Lumina OS Versioning

Template repo: `<github-org>/lumina-tenant-template`

## Semantic Versioning

Lumina OS uses **semver** for template releases. The version number `MAJOR.MINOR.PATCH` increments as follows:

| Increment | When | Examples |
|---|---|---|
| **MAJOR** | Schema changes that break tenant compatibility, model/provider changes that alter agent behavior, removal of agents/skills/config keys | Renaming SOUL.md sections, changing skill frontmatter schema, removing a department pack |
| **MINOR** | New agents, new skills, new config keys, new platform scripts, content improvements to existing agents | Adding `quality/qa-automation` agent, adding `security-best-practices` skill |
| **PATCH** | Bug fixes, typo corrections, metadata updates, documentation | Fixing a broken pattern in a skill, correcting a SOUL.md instruction |

Tags follow the pattern `v{MAJOR}.{MINOR}.{PATCH}` (e.g., `v0.2.0`).

## File Classification Policy

Every file in the template is classified into one of three policies that determine how the sync script handles updates:

### platform-managed (overwrite)

Files owned by the platform. On sync, the tenant's copy is **overwritten** with the template version. Tenants should not modify these files — any changes will be lost on the next sync.

**Patterns**: `agents/*/*/SOUL.md`, `agents/*/*/HEARTBEAT.md`, `agents/*/*/BOOTSTRAP.md`, `skills/**`, `catalog/**`, `gateway-plugins/**`, `plugins/**`, `scripts/**`, `extensions/**`, `config/department-packs.yaml`, `config/memory-routing.yaml`, `config/pipeline-registry.yaml`, `config/runtime-integrations.yaml`, `config/templates/**`, `docs/**`, `*.template`

### tenant-customizable (three-way merge)

Files where the platform provides a base template and the tenant may override or extend. On sync, a **three-way merge** is performed using the previous template version as the merge base. If conflicts arise, conflict markers are left in place for manual resolution.

**Patterns**: `agents/*/*/AGENTS.md`, `config/org.yaml`, `config/openclaw.json`, `config/outbound-policy.yaml`, `CLAUDE.md`

### tenant-owned (skip)

Files that belong entirely to the tenant. The sync script **never touches** these files.

**Patterns**: `agents/*/*/IDENTITY.md`, `agents/*/*/MEMORY.md`, `agents/*/*/USER.md`, `agents/*/*/memory/**`, `tenant.yaml`, `tenant-manifest.yaml`

### Default Policy

Files not matching any pattern default to `platform-managed`.

### Classification Implementation

The classification logic lives in `scripts/file_classification.py`. Rules are evaluated in order — first match wins. The `classify(path)` function returns a `FilePolicy` enum value.

## Update Distribution Process

### 1. Prepare the release

```bash
# In the openclaw repo (source):
# 1. Populate the template repo from openclaw
bash scripts/populate-template.sh

# 2. Verify no tenant-specific contamination
bash scripts/verify-template-isolation.sh /path/to/lumina-tenant-template

# 3. Generate release manifest (auto-detect version or specify explicitly)
cd /path/to/lumina-tenant-template
python3 /path/to/openclaw/scripts/generate-release-manifest.py \
    --auto-version \
    --output release-manifest.yaml

# Or with explicit version:
python3 /path/to/openclaw/scripts/generate-release-manifest.py \
    --version 0.2.0 \
    --base-tag v0.1.0 \
    --output release-manifest.yaml
```

### 2. Tag and release

```bash
cd /path/to/lumina-tenant-template
git add release-manifest.yaml VERSIONING.md
git commit -m "chore: release v0.2.0"
git tag v0.2.0
git push origin main --tags
gh release create v0.2.0 --generate-notes
```

### 3. Trigger tenant sync

After tagging, trigger the sync workflow on the openclaw repo:

```bash
# Automated: dispatch from template repo to openclaw
gh api repos/<github-org>/openclaw/dispatches \
    -f event_type=template-release \
    -f 'client_payload[version]=v0.2.0'
```

Or trigger manually from the GitHub Actions UI: **Actions > Template Sync > Run workflow**.

### 4. Review and merge tenant PRs

The workflow creates one PR per tenant with a sync report in the body showing:
- Files overwritten (platform-managed)
- Files merged (tenant-customizable)
- Files skipped (tenant-owned)
- Files with conflicts (require manual resolution)

Review each PR. If conflicts exist (labeled `conflicts`), resolve them manually before merging.

### 5. Post-sync

After merging all tenant PRs, update the tenant registry:

```bash
# In openclaw repo — update all tenants to new version
# Edit config/tenant-registry.yaml: set template_version to v0.2.0 for all tenants
```

## Rollback Procedure

If a release causes issues in tenant repos:

### Rollback a single tenant

```bash
# 1. Close the sync PR (don't merge)
gh pr close <PR_NUMBER> --repo <github-org>/lumina-tenant-<customer>

# 2. Delete the sync branch
git push origin --delete template-sync/v0.2.0

# 3. Tenant stays at their previous version (no changes applied)
```

### Rollback after merge

```bash
# 1. Revert the merge commit in the tenant repo
cd /path/to/tenant-repo
git revert -m 1 <merge-commit-sha>
git push origin main

# 2. Regenerate tenant manifest at the previous version
python3 scripts/generate-tenant-manifest.py --customer <id>

# 3. Update tenant-registry.yaml to reflect the reverted version
```

### Emergency: force-sync to a known-good version

```bash
# Re-run sync pointing at the previous version
python3 scripts/sync-tenant-template.py --customer <id> --version v0.1.0
```

## Release Checklist

Before every template release:

- [ ] All changes committed to openclaw repo
- [ ] `populate-template.sh` run successfully
- [ ] `verify-template-isolation.sh` passes with 0 failures
- [ ] `generate-release-manifest.py` produces manifest with `policy` field on every entry
- [ ] CHANGELOG reviewed (auto-generated from git log)
- [ ] Version tag follows semver and `v` prefix convention
- [ ] `gh release create` executed
- [ ] `repository_dispatch` sent to trigger tenant sync (or manual workflow trigger)
- [ ] All tenant PRs reviewed and merged (or conflicts resolved)
- [ ] `config/tenant-registry.yaml` updated with new version for all tenants

## Version History

| Version | Date | Summary |
|---|---|---|
| v0.1.0 | 2026-03-25 | Initial release: 50 agents, 199 skills, 4 tenants, SHA256 manifest |
| v0.2.0 | 2026-03-28 | File classification policy, policy-aware sync, tenant manifests, automated distribution |
| v0.3.0 | TBD | Runtime integration normalization (077): canonical runtime policy, audit/apply/verify CLI, startup script convergence |
