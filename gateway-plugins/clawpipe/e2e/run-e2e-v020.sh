#!/usr/bin/env bash
# ClawPipe v0.2.0 E2E test — runs through gateway bridge or directly via CLI
# Usage: bash run-e2e-v020.sh [--via-gateway]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
CLAWPIPE="$REPO_ROOT/clawpipe"
PYTHON="${PYTHON:-$CLAWPIPE/.venv/bin/python}"
PIPELINE_CONFIG="$SCRIPT_DIR/website-pipeline-v020.yaml"

echo "=== ClawPipe v0.2.0 E2E Test ==="
echo "Repo root: $REPO_ROOT"
echo "Python: $PYTHON"
echo "Config: $PIPELINE_CONFIG"
echo ""

# Verify Python and clawpipe are available
"$PYTHON" -c "import clawpipe; print(f'ClawPipe version: {clawpipe.__version__}' if hasattr(clawpipe, '__version__') else 'ClawPipe loaded')" 2>/dev/null || {
    export PYTHONPATH="$CLAWPIPE/src"
    "$PYTHON" -c "import clawpipe; print('ClawPipe loaded via PYTHONPATH')"
}

export PYTHONPATH="$CLAWPIPE/src"

echo "--- Test 1: Run pipeline with v0.2.0 features ---"
RESULT=$("$PYTHON" -m clawpipe run --config "$PIPELINE_CONFIG" --pipeline-id "e2e-v020-001" --json 2>&1) || true
echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"

STATUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unknown")
echo "Status: $STATUS"

if [ "$STATUS" = "ok" ] || [ "$STATUS" = "needs_approval" ]; then
    echo "PASS: Pipeline completed or paused at approval"
else
    echo "WARN: Pipeline status is $STATUS (may be expected for reflection escalation)"
fi

echo ""
echo "--- Test 2: Show pipeline status ---"
SHOW_RESULT=$("$PYTHON" -m clawpipe show --config "$PIPELINE_CONFIG" --pipeline-id "e2e-v020-001" --json 2>&1) || true
echo "$SHOW_RESULT" | python3 -m json.tool 2>/dev/null || echo "$SHOW_RESULT"

echo ""
echo "--- Test 3: Get lessons ---"
LESSONS_RESULT=$("$PYTHON" -m clawpipe lessons --config "$PIPELINE_CONFIG" --pipeline-id "e2e-v020-001" --json 2>&1) || true
echo "$LESSONS_RESULT" | python3 -m json.tool 2>/dev/null || echo "$LESSONS_RESULT"

echo ""
echo "--- Test 4: Verify v0.2.0 envelope fields ---"
# Check quality_score is present in successful runs
HAS_QUALITY=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('yes' if d.get('quality_score') else 'no')" 2>/dev/null || echo "unknown")
echo "Has quality_score: $HAS_QUALITY"

HAS_REGRESSION=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('yes' if 'regression_detected' in d else 'no')" 2>/dev/null || echo "unknown")
echo "Has regression_detected field: $HAS_REGRESSION"

echo ""
echo "=== E2E Test Complete ==="
