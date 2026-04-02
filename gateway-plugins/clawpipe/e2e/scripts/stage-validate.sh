#!/bin/bash
# Stage 4: Validate generated HTML — check files exist, contain expected content
set -euo pipefail
ARTIFACTS_DIR="${CLAWPIPE_ARTIFACTS:-/tmp/clawpipe-e2e/artifacts}"
ERRORS=0

check_file() {
  local file="$1"
  local pattern="$2"
  if [ ! -f "$file" ]; then
    echo "FAIL: $file does not exist" >&2
    ERRORS=$((ERRORS + 1))
    return
  fi
  if ! grep -q "$pattern" "$file"; then
    echo "FAIL: $file missing pattern: $pattern" >&2
    ERRORS=$((ERRORS + 1))
    return
  fi
  echo "PASS: $file contains '$pattern'"
}

check_file "$ARTIFACTS_DIR/brand-tokens.json" '"primary": "#6366f1"'
check_file "$ARTIFACTS_DIR/sitemap.json" '"slug": "index"'
check_file "$ARTIFACTS_DIR/pages/index.html" "ClawPipe"
check_file "$ARTIFACTS_DIR/pages/index.html" "Config-Driven"
check_file "$ARTIFACTS_DIR/pages/index.html" "pipeline-id"
check_file "$ARTIFACTS_DIR/pages/features.html" "Approval Gates"
check_file "$ARTIFACTS_DIR/pages/features.html" "Failure Classification"

if [ "$ERRORS" -gt 0 ]; then
  echo "validate: FAILED — $ERRORS errors" >&2
  exit 1
fi
echo "validate: OK — all checks passed"
exit 0
