---
name: skill-permission-scan
description: "Scan a SKILL.md file for unsafe permission patterns and exfiltration risk"
version: "1.0.0"
scan_exempt: governance-scanner
permissions:
  filesystem: read
  network: false
triggers:
  - command: /skill-permission-scan
metadata:
  openclaw:
    emoji: "🔒"
    requires:
      bins: ["python3"]
      os: ["darwin", "linux"]
---

# Skill Permission Scanner

Audits a staged SKILL.md for unsafe permission patterns, declared-vs-body mismatches,
high-risk binary references, and data exfiltration risk indicators. Writes a structured
`permission-scan.yaml` artifact to the run directory.

## Overview

Runs as one of four parallel scanner agents in the skill-adoption pipeline (Agent Squad
sidecar). Input: SKILL.md path and run_dir from Agent Squad task payload. Output:
`permission-scan.yaml` with `status: clean | warn | blocked` and findings list.

## Steps

### 1. Parse frontmatter

Read the SKILL.md file and extract the YAML frontmatter block (between `---` delimiters).
Parse:
- `permissions.filesystem`: `none | read | write`
- `permissions.network`: `true | false`
- `metadata.openclaw.requires.bins`: list of required binaries

### 2. Check filesystem + network exfil-risk

**Rule**: If `filesystem: write` AND `network: true` are BOTH declared, this represents
an exfiltration risk pattern (write to disk then exfiltrate). Record a WARN finding:
```
code: exfil-risk
severity: warn
message: "filesystem:write + network:true declared — potential data exfiltration path"
```

### 3. Declared-vs-body mismatch scan

Scan the skill body (instructions below frontmatter) for keywords that contradict the
declared permissions:

**Filesystem mismatch** (`filesystem: none` declared but body contains FS keywords):
- Keywords: `open(`, `os.path`, `pathlib`, `read_text`, `write_text`, `shutil`,
  `os.listdir`, `os.makedirs`, `glob.glob`
- Finding: `code: fs-permission-mismatch, severity: warn`

**Network mismatch** (`network: false` declared but body contains HTTP keywords):
- Keywords: `requests.get`, `requests.post`, `httpx.`, `urllib.`, `curl `, `wget `,
  `fetch(`, `http.client`, `aiohttp.`
- Finding: `code: network-permission-mismatch, severity: warn`

### 4. Shell declaration check

If the skill body references `shell:`, `shell.execute`, `subprocess`, or raw bash
command invocation patterns without declaring `filesystem: write`:
- Finding: `code: undeclared-shell, severity: warn`

### 5. High-risk binary check

Check `metadata.openclaw.requires.bins` for high-risk binaries that enable covert
network activity or privilege escalation:
- High-risk: `nc`, `ncat`, `nmap`, `socat`, `netcat`, `tcpdump`, `tshark`,
  `curl` (when combined with `network: false`), `wget` (when combined with `network: false`)
- Finding: `code: high-risk-binary, severity: warn, binary: <name>`

### 6. Compute verdict

```
verdict = max severity of all findings:
  - any "blocked" finding → status: blocked
  - any "warn" finding    → status: warn
  - no findings           → status: clean
```

### 7. Write permission-scan.yaml

Write to `<run_dir>/permission-scan.yaml`:

```yaml
scanner: skill-permission-scan
status: clean | warn | blocked
skill_path: <path>
scanned_at: <ISO timestamp>
permissions_declared:
  filesystem: <declared value>
  network: <declared value>
bins_declared:
  - <bin1>
findings:
  - code: <code>
    severity: warn | blocked
    message: <message>
```

## Output

- `<run_dir>/permission-scan.yaml` with structured findings
- Status to stdout: `permission-scan: <status> (<N> finding(s))`

## Error Handling

- If SKILL.md not found: write `status: error, error: "file not found"` to permission-scan.yaml; exit 1
- If YAML frontmatter is malformed: write `status: error, error: "malformed frontmatter"`; exit 1
- If run_dir not provided: print findings to stdout only; exit 0
