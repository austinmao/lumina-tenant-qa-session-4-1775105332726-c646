#!/bin/bash
# Stage 3: Generate HTML pages from brand tokens + sitemap
set -euo pipefail
ARTIFACTS_DIR="${CLAWPIPE_ARTIFACTS:-/tmp/clawpipe-e2e/artifacts}"
mkdir -p "$ARTIFACTS_DIR/pages"

# Read brand tokens
BRAND_FILE="$ARTIFACTS_DIR/brand-tokens.json"
if [ ! -f "$BRAND_FILE" ]; then
  echo "ERROR: brand-tokens.json not found" >&2
  exit 1
fi

# Generate index.html
cat > "$ARTIFACTS_DIR/pages/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ClawPipe — Pipeline Orchestration</title>
  <style>
    :root {
      --primary: #6366f1;
      --secondary: #a855f7;
      --accent: #14b8a6;
      --bg: #0f172a;
      --surface: #1e293b;
      --text: #f8fafc;
      --font: Inter, system-ui, sans-serif;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: var(--font); background: var(--bg); color: var(--text); min-height: 100vh; }
    nav { display: flex; gap: 2rem; padding: 1.5rem 3rem; background: var(--surface); }
    nav a { color: var(--text); text-decoration: none; font-weight: 500; }
    nav a:hover { color: var(--accent); }
    .hero { text-align: center; padding: 6rem 2rem; }
    .hero h1 { font-size: 3.5rem; background: linear-gradient(135deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1.5rem; }
    .hero p { font-size: 1.25rem; color: #94a3b8; max-width: 600px; margin: 0 auto 2rem; }
    .cta { display: inline-block; padding: 0.875rem 2rem; background: var(--primary); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; }
    .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; padding: 4rem 3rem; }
    .card { background: var(--surface); border-radius: 1rem; padding: 2rem; }
    .card h3 { color: var(--accent); margin-bottom: 0.75rem; }
    footer { text-align: center; padding: 2rem; color: #475569; border-top: 1px solid var(--surface); }
    footer span#pipeline-id { font-family: monospace; color: var(--accent); }
  </style>
</head>
<body>
  <nav>
    <a href="/">Home</a>
    <a href="/features">Features</a>
    <a href="/docs">Docs</a>
  </nav>
  <section class="hero">
    <h1>ClawPipe</h1>
    <p>Config-driven pipeline orchestration for AI agent workflows. Define stages in YAML, let ClawPipe handle retry, approval gates, and parallel dispatch.</p>
    <a href="/docs" class="cta">Get Started</a>
  </section>
  <section class="features">
    <div class="card">
      <h3>Config-Driven</h3>
      <p>Define pipelines in YAML — stages, dependencies, retry policies, and approval gates. No code required.</p>
    </div>
    <div class="card">
      <h3>Retry & Recovery</h3>
      <p>Automatic retry with exponential backoff, failure classification, and resume from any stage.</p>
    </div>
    <div class="card">
      <h3>Gateway Integration</h3>
      <p>Runs as an OpenClaw gateway plugin. Invoke via /tools/invoke or from any agent session.</p>
    </div>
  </section>
  <footer>
    <p>Built by ClawPipe v0.1.0 — Pipeline ID: <span id="pipeline-id">e2e-test</span></p>
  </footer>
</body>
</html>
HTML

# Generate features.html
cat > "$ARTIFACTS_DIR/pages/features.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Features — ClawPipe</title>
  <style>
    :root { --primary: #6366f1; --accent: #14b8a6; --bg: #0f172a; --surface: #1e293b; --text: #f8fafc; }
    body { font-family: Inter, system-ui, sans-serif; background: var(--bg); color: var(--text); }
    nav { display: flex; gap: 2rem; padding: 1.5rem 3rem; background: var(--surface); }
    nav a { color: var(--text); text-decoration: none; }
    main { padding: 4rem 3rem; max-width: 800px; margin: 0 auto; }
    h1 { color: var(--primary); margin-bottom: 2rem; }
    .feature { margin-bottom: 2rem; padding: 1.5rem; background: var(--surface); border-radius: 0.75rem; border-left: 4px solid var(--accent); }
    .feature h2 { color: var(--accent); margin-bottom: 0.5rem; }
  </style>
</head>
<body>
  <nav><a href="/">Home</a><a href="/features">Features</a><a href="/docs">Docs</a></nav>
  <main>
    <h1>Features</h1>
    <div class="feature"><h2>YAML Configuration</h2><p>Define entire pipelines declaratively.</p></div>
    <div class="feature"><h2>Stage Dependencies</h2><p>DAG-based execution with depends_on.</p></div>
    <div class="feature"><h2>Approval Gates</h2><p>Pause pipelines for human review.</p></div>
    <div class="feature"><h2>Failure Classification</h2><p>Categorize failures for smart retry.</p></div>
    <div class="feature"><h2>Parallel Dispatch</h2><p>Run independent stages concurrently via Agent Squad.</p></div>
  </main>
</body>
</html>
HTML

echo "html-gen: OK — wrote index.html, features.html"
exit 0
