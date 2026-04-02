#!/bin/bash
# Stage 1: Extract brand tokens from config and emit JSON
set -euo pipefail
ARTIFACTS_DIR="${CLAWPIPE_ARTIFACTS:-/tmp/clawpipe-e2e/artifacts}"
mkdir -p "$ARTIFACTS_DIR"

cat > "$ARTIFACTS_DIR/brand-tokens.json" <<'JSON'
{
  "brand": "ClawPipe Demo Site",
  "colors": {
    "primary": "#6366f1",
    "secondary": "#a855f7",
    "accent": "#14b8a6",
    "background": "#0f172a",
    "surface": "#1e293b",
    "text": "#f8fafc"
  },
  "typography": {
    "heading": "Inter, system-ui, sans-serif",
    "body": "Inter, system-ui, sans-serif",
    "mono": "JetBrains Mono, monospace"
  },
  "spacing": { "unit": "0.25rem", "scale": [0, 1, 2, 4, 6, 8, 12, 16, 24] }
}
JSON

echo "brand-extract: OK — wrote brand-tokens.json"
exit 0
