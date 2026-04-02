#!/bin/bash
# Stage 2: Generate sitemap structure
set -euo pipefail
ARTIFACTS_DIR="${CLAWPIPE_ARTIFACTS:-/tmp/clawpipe-e2e/artifacts}"
mkdir -p "$ARTIFACTS_DIR"

cat > "$ARTIFACTS_DIR/sitemap.json" <<'JSON'
{
  "pages": [
    {"slug": "index", "title": "ClawPipe — Pipeline Orchestration", "template": "hero-landing"},
    {"slug": "features", "title": "Features", "template": "feature-grid"},
    {"slug": "docs", "title": "Documentation", "template": "docs-layout"}
  ],
  "nav": [
    {"label": "Home", "href": "/"},
    {"label": "Features", "href": "/features"},
    {"label": "Docs", "href": "/docs"}
  ]
}
JSON

echo "sitemap: OK — wrote sitemap.json"
exit 0
