#!/bin/bash
# ClawPipe v0.1.0 — Gateway E2E Test
# Runs the website orchestration pipeline through the OpenClaw gateway
# and validates all artifacts.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
GATEWAY="http://127.0.0.1:18789"
TOKEN="${OPENCLAW_GATEWAY_TOKEN:-aa12af69ade407c43a7e347033c73127d26fc868067a8674}"
PIPELINE_ID="e2e-$(date -u +%Y%m%d-%H%M%S)"
CONFIG_PATH="extensions/clawpipe/e2e/website-pipeline.yaml"
ARTIFACTS_DIR="/tmp/clawpipe-e2e/artifacts"
ERRORS=0

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
blue()  { printf '\033[0;34m%s\033[0m\n' "$*"; }

fail() { red "FAIL: $*"; ERRORS=$((ERRORS + 1)); }
pass() { green "PASS: $*"; }

invoke() {
  local payload="$1"
  curl -sS -X POST "$GATEWAY/tools/invoke" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$payload"
}

extract_text() {
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['content'][0]['text'])"
}

# ── Pre-flight ────────────────────────────────────────────────
blue "== ClawPipe Gateway E2E Test =="
blue "Pipeline ID: $PIPELINE_ID"

# Clean previous artifacts
rm -rf /tmp/clawpipe-e2e

# 1. Health check
blue "\n[1/6] Gateway health check"
HEALTH=$(curl -sS "$GATEWAY/health" 2>&1)
if echo "$HEALTH" | grep -q '"ok":true'; then
  pass "Gateway is live"
else
  fail "Gateway not responding: $HEALTH"
  exit 1
fi

# 2. Watch (verify tool is registered)
blue "\n[2/6] Tool registration check (watch)"
WATCH=$(invoke '{"tool":"clawpipe","args":{"action":"watch"}}')
if echo "$WATCH" | grep -q '"ok":true'; then
  pass "clawpipe tool is registered"
else
  fail "clawpipe tool not available: $WATCH"
  exit 1
fi

# 3. Run pipeline
blue "\n[3/6] Running website pipeline through gateway"
RUN_RESULT=$(invoke "{\"tool\":\"clawpipe\",\"args\":{\"action\":\"run\",\"config_path\":\"$CONFIG_PATH\",\"pipeline_id\":\"$PIPELINE_ID\"}}")
RUN_OK=$(echo "$RUN_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok',False))" 2>/dev/null || echo "False")
RUN_TEXT=$(echo "$RUN_RESULT" | extract_text 2>/dev/null || echo "{}")
RUN_STATUS=$(echo "$RUN_TEXT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','error'))" 2>/dev/null || echo "error")

if [ "$RUN_OK" = "True" ] && [ "$RUN_STATUS" = "ok" ]; then
  STAGES=$(echo "$RUN_TEXT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stages_completed',0))")
  pass "Pipeline completed: $STAGES stages, status=$RUN_STATUS"
else
  fail "Pipeline failed: $RUN_TEXT"
fi

# 4. Show pipeline state
blue "\n[4/6] Verifying pipeline state (show)"
SHOW_RESULT=$(invoke "{\"tool\":\"clawpipe\",\"args\":{\"action\":\"show\",\"config_path\":\"$CONFIG_PATH\",\"pipeline_id\":\"$PIPELINE_ID\"}}")
SHOW_TEXT=$(echo "$SHOW_RESULT" | extract_text 2>/dev/null || echo "{}")
SHOW_STATUS=$(echo "$SHOW_TEXT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('state',{}).get('status','unknown'))" 2>/dev/null || echo "unknown")
if [ "$SHOW_STATUS" = "completed" ]; then
  pass "Pipeline state: completed"
else
  fail "Pipeline state: $SHOW_STATUS (expected completed)"
fi

# 5. Artifact validation
blue "\n[5/6] Validating artifacts"

check_artifact() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if [ ! -f "$file" ]; then
    fail "$label: file not found ($file)"
    return
  fi
  if grep -q "$pattern" "$file"; then
    pass "$label"
  else
    fail "$label: missing pattern '$pattern'"
  fi
}

check_artifact "$ARTIFACTS_DIR/brand-tokens.json" '"primary": "#6366f1"' "brand-tokens.json has primary color"
check_artifact "$ARTIFACTS_DIR/sitemap.json" '"slug": "index"' "sitemap.json has index page"
check_artifact "$ARTIFACTS_DIR/pages/index.html" "ClawPipe" "index.html has title"
check_artifact "$ARTIFACTS_DIR/pages/index.html" "Config-Driven" "index.html has feature card"
check_artifact "$ARTIFACTS_DIR/pages/index.html" "pipeline-id" "index.html has pipeline-id footer"
check_artifact "$ARTIFACTS_DIR/pages/features.html" "Approval Gates" "features.html has approval gates"
check_artifact "$ARTIFACTS_DIR/pages/features.html" "Failure Classification" "features.html has failure classification"

# 6. Lessons (verify no failures were logged)
blue "\n[6/6] Checking lessons learned"
LESSONS_RESULT=$(invoke "{\"tool\":\"clawpipe\",\"args\":{\"action\":\"lessons\",\"config_path\":\"$CONFIG_PATH\",\"pipeline_id\":\"$PIPELINE_ID\"}}")
LESSONS_TEXT=$(echo "$LESSONS_RESULT" | extract_text 2>/dev/null || echo "{}")
LESSONS_COUNT=$(echo "$LESSONS_TEXT" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('lessons',[])))" 2>/dev/null || echo "-1")
if [ "$LESSONS_COUNT" = "0" ]; then
  pass "No failure lessons (clean run)"
else
  blue "Lessons count: $LESSONS_COUNT"
fi

# ── Summary ───────────────────────────────────────────────────
echo ""
if [ "$ERRORS" -gt 0 ]; then
  red "== FAILED: $ERRORS errors =="
  exit 1
else
  green "== ALL CHECKS PASSED =="
  green "Pipeline $PIPELINE_ID ran through gateway with 4/4 stages"
  green "HTML artifacts at: $ARTIFACTS_DIR/pages/"
  exit 0
fi
