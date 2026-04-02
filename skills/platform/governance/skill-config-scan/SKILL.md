---
name: skill-config-scan
description: "Scan a SKILL.md file for configuration gate gaps and ClawHub origin tracking"
version: "1.0.0"
scan_exempt: governance-scanner
permissions:
  filesystem: read
  network: false
triggers:
  - command: /skill-config-scan
metadata:
  openclaw:
    emoji: "⚙️"
    requires:
      bins: ["python3"]
      os: ["darwin", "linux"]
---

# Skill Config Scanner

Audits a staged SKILL.md for configuration gate gaps: env var usage vs `requires.env`
declarations, hardcoded values, ClawHub origin tracking files, and `clawdhub` CLI
references. Writes a structured `config-scan.yaml` artifact to the run directory.

## Overview

Runs as one of four parallel scanner agents in the skill-adoption pipeline (Agent Squad
sidecar). Input: SKILL.md path and run_dir from Agent Squad task payload. Output:
`config-scan.yaml` with `status: clean | warn | blocked` and findings list.

## Steps

### 1. Parse frontmatter and body

Read the SKILL.md file. Extract:
- Frontmatter YAML block (between `---` delimiters)
- `metadata.openclaw.requires.env`: list of declared env var gates
- Skill body: all content below the closing `---` of frontmatter

### 2. Env var usage vs requires.env mismatch

Scan the skill body for environment variable references:
- Patterns: `$MY_VAR`, `${MY_VAR}`, `os.environ["MY_VAR"]`, `os.getenv("MY_VAR")`,
  `process.env.MY_VAR`, `ENV["MY_VAR"]`

Extract all env var names found in the body. Compare against `requires.env` list.
For each env var found in body but NOT in `requires.env`:
- Finding: `code: undeclared-env, severity: warn, env_var: <name>`
  Message: "Env var $<name> used in body but not declared in requires.env — skill may
  fail silently if var is unset"

### 3. Hardcoded value check

Scan the body for patterns that suggest hardcoded secrets or configuration:
- API key patterns: `sk-`, `xoxb-`, `xoxp-`, `Bearer `, `api_key =`, `API_KEY =`
  (followed by a quoted string value, not a variable reference)
- Token patterns: literals matching `[A-Za-z0-9]{32,}` in assignment context
- IP:port patterns that are not localhost/loopback: exclude `127.0.0.1`, `localhost`,
  `0.0.0.0`; flag any other hardcoded IP with port

For each match:
- Finding: `code: hardcoded-value, severity: blocked, pattern: <matched text redacted>`

### 4. ClawHub origin tracking check

Check if `.clawhub/origin.json` or `.clawdhub/origin.json` exists in the same
directory as the SKILL.md:
- If found: `code: clawhub-origin, severity: warn`
  Message: "ClawHub origin tracking file found — remove origin.json before deploying.
  clawdhub update will silently overwrite local modifications."

### 5. clawdhub CLI reference check

Scan the skill body for references to the `clawdhub` CLI installer:
- Patterns: `clawdhub install`, `clawdhub update`, `clawdhub add`
- Finding: `code: clawdhub-cli-ref, severity: blocked`
  Message: "clawdhub CLI references found — the installer is a known supply chain
  attack vector (ClawHavoc campaign). Remove these instructions."

### 6. Compiler scan integration

If `python3 -m compiler.engine.cli skill scan <path>` is available, run it and
incorporate its output into findings. Map compiler scan results:
- `blocked` → findings entry with `code: compiler-scan-blocked, severity: blocked`
- `warnings` → findings entry with `code: compiler-scan-warn, severity: warn`
- `clean` → no additional finding

### 7. Compute verdict

```
verdict = max severity:
  - any "blocked" finding → status: blocked
  - any "warn" finding    → status: warn
  - no findings           → status: clean
```

### 8. Write config-scan.yaml

Write to `<run_dir>/config-scan.yaml`:

```yaml
scanner: skill-config-scan
status: clean | warn | blocked
skill_path: <path>
scanned_at: <ISO timestamp>
env_vars_declared:
  - <var1>
env_vars_in_body:
  - <var1>
findings:
  - code: <code>
    severity: warn | blocked
    message: <message>
```

## Output

- `<run_dir>/config-scan.yaml` with structured findings
- Status to stdout: `config-scan: <status> (<N> finding(s))`

## Error Handling

- If SKILL.md not found: write `status: error, error: "file not found"`; exit 1
- If run_dir not provided: print findings to stdout only; exit 0
- compiler.engine.cli unavailable: skip step 6 with `compiler_scan: skipped` note
