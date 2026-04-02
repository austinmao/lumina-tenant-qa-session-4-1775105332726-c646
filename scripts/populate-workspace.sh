#!/bin/bash
# populate-workspace.sh — Populate OpenClaw workspace with agents + skills at first boot
#
# Copies platform agents, skills, and tenant-specific overrides into the
# OpenClaw workspace directory.
#
# Version-aware: skips if PLATFORM_VERSION matches the stored marker version.
# If PLATFORM_VERSION is not set, defaults to "unknown" (forces re-population).
#
# Usage: COMPOSIO_USER_ID=<customer_id> bash scripts/populate-workspace.sh
#
# Environment:
#   COMPOSIO_USER_ID     — tenant identifier (required)
#   OPENCLAW_HOME        — OpenClaw home dir (default: ~/.openclaw)
#   TENANT_REPO_URL      — GitHub URL of customer's tenant repo (optional)
#   TENANT_REPO_REF      — Git ref to checkout after clone (optional tag/branch/SHA)
#   GITHUB_PAT           — GitHub Personal Access Token for private repo clone (optional)
#   PLATFORM_VERSION     — Platform version string for idempotency check (default: unknown)
#   SLACK_ALERT_WEBHOOK  — Slack webhook URL for failure alerts (optional)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
WORKSPACE="${OPENCLAW_HOME}/workspace"
TENANT_ID="${COMPOSIO_USER_ID:?COMPOSIO_USER_ID is required}"
POPULATED_MARKER="$WORKSPACE/.workspace-populated"
PLATFORM_VERSION="${PLATFORM_VERSION:-unknown}"
TENANT_REPO_URL="${TENANT_REPO_URL:-}"
TENANT_REPO_REF="${TENANT_REPO_REF:-}"
GITHUB_PAT="${GITHUB_PAT:-}"
SLACK_WEBHOOK="${SLACK_ALERT_WEBHOOK:-}"

# ── Version-aware idempotency check ────────────────────────────────────────
if [ -f "$POPULATED_MARKER" ]; then
    STORED_VERSION="$(cat "$POPULATED_MARKER" | tr -d '[:space:]')"
    if [ "$STORED_VERSION" = "$PLATFORM_VERSION" ]; then
        echo "[populate] Workspace already populated (version=$PLATFORM_VERSION). Skipping."
        exit 0
    else
        echo "[populate] Platform version changed: stored=$STORED_VERSION current=$PLATFORM_VERSION. Re-populating."
    fi
fi

echo "[populate] Populating workspace for tenant: $TENANT_ID (version=$PLATFORM_VERSION)"

mkdir -p "$WORKSPACE"

# ── Alert helper ────────────────────────────────────────────────────────────
notify_slack() {
    local msg="$1"
    if [ -n "$SLACK_WEBHOOK" ]; then
        curl -s -X POST "$SLACK_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"[populate-workspace] [${TENANT_ID}] $msg\"}" \
            >/dev/null 2>&1 || true
    fi
}

# ── Step 1: Copy platform agents ────────────────────────────────────────────
if [ -d "$REPO_ROOT/agents" ]; then
    echo "[populate] Copying platform agents..."
    cp -r "$REPO_ROOT/agents/"* "$WORKSPACE/" 2>/dev/null || true
    AGENT_COUNT=$(find "$WORKSPACE" -name "SOUL.md" -type f | wc -l | tr -d ' ')
    echo "[populate] Copied $AGENT_COUNT agents"
fi

# ── Step 2: Copy platform skills ────────────────────────────────────────────
if [ -d "$REPO_ROOT/skills" ]; then
    echo "[populate] Copying platform skills..."
    mkdir -p "$WORKSPACE/skills"
    cp -r "$REPO_ROOT/skills/"* "$WORKSPACE/skills/" 2>/dev/null || true
    SKILL_COUNT=$(find "$WORKSPACE/skills" -name "SKILL.md" -type f | wc -l | tr -d ' ')
    echo "[populate] Copied $SKILL_COUNT skills"
fi

# ── Step 3: Clone and apply tenant repo ─────────────────────────────────────
TENANT_CLONE_DIR="/tmp/tenant-repo-$$"

clone_and_apply_tenant() {
    local repo_url="$1"

    # Inject GITHUB_PAT into HTTPS URL if provided
    if [ -n "$GITHUB_PAT" ]; then
        # Convert https://github.com/... → https://<pat>@github.com/...
        repo_url="${repo_url/https:\/\//https:\/\/${GITHUB_PAT}@}"
    fi

    echo "[populate] Cloning tenant repo (shallow)..."
    if ! git clone --depth 1 --single-branch "$repo_url" "$TENANT_CLONE_DIR" 2>&1; then
        echo "[populate] ERROR: Failed to clone tenant repo: $TENANT_REPO_URL"
        notify_slack "ERROR: Failed to clone tenant repo $TENANT_REPO_URL — continuing with platform-only workspace"
        return 1
    fi

    # Checkout specific ref if requested
    if [ -n "$TENANT_REPO_REF" ]; then
        echo "[populate] Checking out ref: $TENANT_REPO_REF"
        if ! git -C "$TENANT_CLONE_DIR" fetch --depth 1 origin "$TENANT_REPO_REF" 2>&1; then
            echo "[populate] ERROR: Failed to fetch ref $TENANT_REPO_REF — falling back to default branch"
            notify_slack "ERROR: Tenant repo ref $TENANT_REPO_REF not found — continuing with default branch"
        elif ! git -C "$TENANT_CLONE_DIR" checkout FETCH_HEAD 2>&1; then
            echo "[populate] ERROR: Failed to checkout ref $TENANT_REPO_REF — using default branch"
            notify_slack "ERROR: Failed to checkout tenant ref $TENANT_REPO_REF — continuing with default branch"
        fi
    fi

    # Apply tenant overlay (same order as before: agents, skills, config, brands)
    if [ -d "$TENANT_CLONE_DIR/agents" ]; then
        cp -r "$TENANT_CLONE_DIR/agents/"* "$WORKSPACE/" 2>/dev/null || true
        echo "[populate] Applied tenant agent overrides"
    fi

    if [ -d "$TENANT_CLONE_DIR/skills" ]; then
        cp -r "$TENANT_CLONE_DIR/skills/"* "$WORKSPACE/skills/" 2>/dev/null || true
        echo "[populate] Applied tenant skill overrides"
    fi

    if [ -d "$TENANT_CLONE_DIR/config" ]; then
        mkdir -p "$WORKSPACE/config"
        cp -r "$TENANT_CLONE_DIR/config/"* "$WORKSPACE/config/" 2>/dev/null || true
        echo "[populate] Applied tenant config"
    fi

    if [ -d "$TENANT_CLONE_DIR/brands" ]; then
        mkdir -p "$WORKSPACE/brands"
        cp -r "$TENANT_CLONE_DIR/brands/"* "$WORKSPACE/brands/" 2>/dev/null || true
        echo "[populate] Applied tenant brand assets"
    fi

    return 0
}

if [ -n "$TENANT_REPO_URL" ]; then
    clone_and_apply_tenant "$TENANT_REPO_URL" || true
    # Clean up temp clone
    rm -rf "$TENANT_CLONE_DIR" 2>/dev/null || true
else
    echo "[populate] WARNING: TENANT_REPO_URL not set — running with platform-only workspace"
    notify_slack "WARNING: TENANT_REPO_URL not set — platform-only workspace for ${TENANT_ID}"
    mkdir -p "$WORKSPACE/config"
fi

# ── Step 5: Copy shared config files ────────────────────────────────────────
if [ -f "$REPO_ROOT/config/memory-routing.yaml" ]; then
    mkdir -p "$WORKSPACE/config"
    cp "$REPO_ROOT/config/memory-routing.yaml" "$WORKSPACE/config/" 2>/dev/null || true
fi

# ── Step 6: Verify LLM auth profiles ────────────────────────────────────────
AGENT_AUTH_DIR="$OPENCLAW_HOME/agents/main/agent"
mkdir -p "$AGENT_AUTH_DIR"
if [ -f "$AGENT_AUTH_DIR/auth-profiles.json" ]; then
    echo "[populate] Auth profiles found — LLM credentials ready"
else
    echo "[populate] WARNING: No auth-profiles.json found at $AGENT_AUTH_DIR/"
    echo "[populate] The agent will not have LLM credentials until auth is configured."
    echo "[populate] Fix: run 'openclaw models auth login --provider openai-codex' inside the container"
    echo "[populate] Or copy auth-profiles.json to the volume via 'railway ssh'"
fi

# ── Mark as populated with version ──────────────────────────────────────────
echo "$PLATFORM_VERSION" > "$POPULATED_MARKER"
echo "[populate] Workspace populated successfully (version=$PLATFORM_VERSION)"
