---
name: instance-health
description: "Check this instance's deployment health — workspace, auth, services, identity"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /instance-health
metadata:
  openclaw:
    emoji: "🏥"
    requires:
      bins: ["curl", "jq"]
---

# Instance Health Check

## Overview

Validates that the current OpenClaw instance is correctly deployed and operational. Runs 8 checks covering workspace population, authentication, service health, and tenant identity. Produces a YAML report to stdout with an overall status and per-check results.

**When to use**: After deployment, during heartbeat checks, before canary promotion, or when debugging a misbehaving instance.

## Steps

### 1 — Run the health check script

Execute the following script via `shell.execute`. The script requires no arguments — it reads environment variables and local files to determine health.

```
exec: bash -c '
#!/usr/bin/env bash
set -euo pipefail

# ── Configuration ─────────────────────────────────────────────
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
GW_PORT="${PORT:-18789}"
MEM0_PORT="19010"
SQUAD_PORT="18790"

# ── State tracking ────────────────────────────────────────────
CORE_FAIL=0
NON_CRITICAL_FAIL=0
declare -a CHECK_LINES=()

emit_check() {
  local name="$1" status="$2"
  shift 2
  CHECK_LINES+=("    ${name}:")
  CHECK_LINES+=("      status: ${status}")
  while [ $# -gt 0 ]; do
    CHECK_LINES+=("      $1")
    shift
  done
}

# ── Check 1: workspace_agents ────────────────────────────────
AGENT_COUNT=$(find "$OPENCLAW_HOME/workspace/agents" -mindepth 2 -name "SOUL.md" 2>/dev/null | wc -l | tr -d " ")
if [ "$AGENT_COUNT" -gt 0 ]; then
  emit_check "workspace_agents" "pass" "count: ${AGENT_COUNT}"
else
  CORE_FAIL=1
  emit_check "workspace_agents" "fail" "count: 0" "detail: \"No SOUL.md files found in $OPENCLAW_HOME/workspace/agents/\""
fi

# ── Check 2: workspace_skills ────────────────────────────────
SKILL_COUNT=$(find "$OPENCLAW_HOME/workspace/skills" -mindepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d " ")
if [ "$SKILL_COUNT" -gt 0 ]; then
  emit_check "workspace_skills" "pass" "count: ${SKILL_COUNT}"
else
  CORE_FAIL=1
  emit_check "workspace_skills" "fail" "count: 0" "detail: \"No SKILL.md files found in $OPENCLAW_HOME/workspace/skills/\""
fi

# ── Check 3: tenant_overlay ──────────────────────────────────
TENANT_REPO="${TENANT_REPO_URL:-}"
POPULATED_MARKER="$OPENCLAW_HOME/workspace/.workspace-populated"
TENANT_YAML="$OPENCLAW_HOME/workspace/tenant.yaml"

if [ -z "$TENANT_REPO" ]; then
  # No tenant repo configured — valid for platform-only workspaces
  emit_check "tenant_overlay" "warn" "tenant_repo: null" "detail: \"TENANT_REPO_URL not set — platform-only workspace\""
  NON_CRITICAL_FAIL=1
elif [ -f "$POPULATED_MARKER" ] && [ -f "$TENANT_YAML" ]; then
  emit_check "tenant_overlay" "pass" "tenant_repo: \"${TENANT_REPO}\""
else
  MISSING=""
  [ ! -f "$POPULATED_MARKER" ] && MISSING=".workspace-populated marker missing"
  [ ! -f "$TENANT_YAML" ] && MISSING="${MISSING:+$MISSING; }tenant.yaml missing"
  emit_check "tenant_overlay" "warn" "tenant_repo: \"${TENANT_REPO}\"" "detail: \"${MISSING}\""
  NON_CRITICAL_FAIL=1
fi

# ── Check 4: llm_auth ────────────────────────────────────────
AUTH_FILE="$OPENCLAW_HOME/agents/main/agent/auth-profiles.json"
if [ -f "$AUTH_FILE" ]; then
  if jq empty "$AUTH_FILE" 2>/dev/null; then
    emit_check "llm_auth" "pass" "profiles_found: true"
  else
    CORE_FAIL=1
    emit_check "llm_auth" "fail" "profiles_found: false" "detail: \"auth-profiles.json exists but is not valid JSON\""
  fi
else
  CORE_FAIL=1
  emit_check "llm_auth" "fail" "profiles_found: false" "detail: \"$AUTH_FILE not found\""
fi

# ── Check 5: gateway_health ──────────────────────────────────
GW_RESP=$(curl -sf "http://localhost:${GW_PORT}/health" 2>/dev/null) && GW_OK=1 || GW_OK=0
if [ "$GW_OK" -eq 1 ]; then
  # Escape the response for safe YAML embedding
  GW_SAFE=$(echo "$GW_RESP" | tr -d "\n" | sed "s/\"/\\\\\"/g")
  emit_check "gateway_health" "pass" "response: \"${GW_SAFE}\""
else
  CORE_FAIL=1
  emit_check "gateway_health" "fail" "response: null" "detail: \"Gateway unreachable at localhost:${GW_PORT}\""
fi

# ── Check 6: mem0_health ─────────────────────────────────────
MEM0_RESP=$(curl -sf "http://localhost:${MEM0_PORT}/health" 2>/dev/null) && MEM0_OK=1 || MEM0_OK=0
if [ "$MEM0_OK" -eq 1 ]; then
  emit_check "mem0_health" "pass" "detail: \"Mem0 reachable at localhost:${MEM0_PORT}\""
else
  NON_CRITICAL_FAIL=1
  emit_check "mem0_health" "warn" "detail: \"Mem0 unreachable at localhost:${MEM0_PORT}\""
fi

# ── Check 7: agent_squad_health ──────────────────────────────
SQUAD_RESP=$(curl -sf "http://localhost:${SQUAD_PORT}/health" 2>/dev/null) && SQUAD_OK=1 || SQUAD_OK=0
if [ "$SQUAD_OK" -eq 1 ]; then
  emit_check "agent_squad_health" "pass" "detail: \"Agent Squad reachable at localhost:${SQUAD_PORT}\""
else
  NON_CRITICAL_FAIL=1
  emit_check "agent_squad_health" "warn" "detail: \"Agent Squad unreachable at localhost:${SQUAD_PORT}\""
fi

# ── Check 8: tenant_identity ─────────────────────────────────
COMPOSIO_ID="${COMPOSIO_USER_ID:-}"
if [ -z "$COMPOSIO_ID" ]; then
  # No COMPOSIO_USER_ID set — skip check (valid during local dev)
  emit_check "tenant_identity" "skip" "composio_user_id: null" "tenant_yaml_match: false" "detail: \"COMPOSIO_USER_ID not set — skipping identity check\""
elif [ -f "$TENANT_YAML" ]; then
  # Extract customer_id from tenant.yaml (handles both quoted and unquoted values)
  TENANT_CID=$(grep -E "^customer_id:" "$TENANT_YAML" 2>/dev/null | head -1 | sed "s/^customer_id:[[:space:]]*//" | tr -d "\"'\'' " || echo "")
  if [ "$COMPOSIO_ID" = "$TENANT_CID" ]; then
    emit_check "tenant_identity" "pass" "composio_user_id: \"${COMPOSIO_ID}\"" "tenant_yaml_match: true"
  else
    CORE_FAIL=1
    emit_check "tenant_identity" "fail" "composio_user_id: \"${COMPOSIO_ID}\"" "tenant_yaml_match: false" "detail: \"Mismatch: COMPOSIO_USER_ID=${COMPOSIO_ID} vs tenant.yaml customer_id=${TENANT_CID}\""
  fi
else
  CORE_FAIL=1
  emit_check "tenant_identity" "fail" "composio_user_id: \"${COMPOSIO_ID}\"" "tenant_yaml_match: false" "detail: \"tenant.yaml not found — cannot verify identity\""
fi

# ── Compute overall status ────────────────────────────────────
if [ "$CORE_FAIL" -gt 0 ]; then
  STATUS="unhealthy"
  EXIT_CODE=2
elif [ "$NON_CRITICAL_FAIL" -gt 0 ]; then
  STATUS="degraded"
  EXIT_CODE=1
else
  STATUS="healthy"
  EXIT_CODE=0
fi

# ── Emit YAML report ─────────────────────────────────────────
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "---"
echo "timestamp: \"${TIMESTAMP}\""
echo "instance_id: \"${COMPOSIO_ID:-unknown}\""
echo "status: ${STATUS}"
echo "checks:"
for line in "${CHECK_LINES[@]}"; do
  echo "$line"
done

exit $EXIT_CODE
'
```

### 2 — Interpret results

| Exit code | Status | Meaning |
|---|---|---|
| `0` | healthy | All 8 checks passed |
| `1` | degraded | Core checks passed; non-critical services (Mem0, Agent Squad, tenant overlay) have warnings |
| `2` | unhealthy | One or more core checks failed — instance cannot serve traffic safely |

**Core checks** (failure = unhealthy): `workspace_agents`, `workspace_skills`, `llm_auth`, `gateway_health`, `tenant_identity`

**Non-critical checks** (failure = degraded): `tenant_overlay`, `mem0_health`, `agent_squad_health`

### 3 — Act on results

- **healthy**: No action required.
- **degraded**: Log the warnings. Investigate non-critical failures when convenient. Instance is operational.
- **unhealthy**: Do NOT promote this instance (canary gate must reject). Investigate the failed core check(s):
  - `workspace_agents` / `workspace_skills` fail: `populate-workspace.sh` did not run or failed — re-run it.
  - `llm_auth` fail: `auth-profiles.json` missing or malformed — check Doppler config injection.
  - `gateway_health` fail: Gateway process not running — check `openclaw daemon status` or Railway container logs.
  - `tenant_identity` fail: `COMPOSIO_USER_ID` does not match `tenant.yaml` `customer_id` — wrong tenant repo cloned or env var misconfigured.

## Output

YAML document to stdout. Example:

```yaml
---
timestamp: "2026-03-21T14:30:00Z"
instance_id: "your-tenant"
status: healthy
checks:
    workspace_agents:
      status: pass
      count: 12
    workspace_skills:
      status: pass
      count: 45
    tenant_overlay:
      status: pass
      tenant_repo: "https://github.com/your-org/lumina-tenant-example"
    llm_auth:
      status: pass
      profiles_found: true
    gateway_health:
      status: pass
      response: "{\"status\":\"ok\"}"
    mem0_health:
      status: pass
      detail: "Mem0 reachable at localhost:19010"
    agent_squad_health:
      status: pass
      detail: "Agent Squad reachable at localhost:18790"
    tenant_identity:
      status: pass
      composio_user_id: "your-tenant"
      tenant_yaml_match: true
```

## Error Handling

- If `curl` or `jq` is not installed, the skill will not load (gated via `requires.bins`).
- If `$OPENCLAW_HOME` is not set, defaults to `~/.openclaw`.
- If `$PORT` is not set, defaults to `18789` (standard gateway port).
- If `$COMPOSIO_USER_ID` is not set, the `tenant_identity` check is skipped (status: `skip`), not failed.
- The script uses `set -euo pipefail` but catches individual check failures gracefully — a failing `curl` or missing file does not abort the entire script.
