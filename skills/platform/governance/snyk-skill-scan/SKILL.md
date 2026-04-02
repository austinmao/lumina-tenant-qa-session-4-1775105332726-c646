---
name: snyk-skill-scan
description: "Scan agents and skills for security vulnerabilities with Snyk"
version: "1.0.0"
scan_exempt: governance-scanner
permissions:
  filesystem: read
  network: true
triggers:
  - command: /snyk-skill-scan
metadata:
  openclaw:
    emoji: "\U0001F6E1"
    requires:
      bins: ["uvx"]
      env: ["SNYK_TOKEN"]
      os: ["darwin", "linux"]
---

# Snyk Skill Scan

Scans OpenClaw agents and skills for security vulnerabilities using Snyk Agent Scan. Detects prompt injections, tool poisoning, malware payloads, credential exposure, and unsafe permission patterns.

## Overview

Wraps `snyk-agent-scan` (https://github.com/snyk/agent-scan) to audit SKILL.md and SOUL.md files for 15+ security issue types. Use before deploying any new or modified agent or skill — especially when adopting components from external sources.

## Issue Codes Detected

| Code | Severity | Description |
|------|----------|-------------|
| E001 | CRITICAL | Prompt injection in MCP server tools |
| E002 | HIGH | Tool shadowing (overriding built-in tools) |
| E003 | CRITICAL | Tool poisoning (malicious tool descriptions) |
| E004 | CRITICAL | Prompt injection in agent skills |
| E006 | CRITICAL | Malware payloads hidden in skill instructions |
| W007 | MEDIUM | Unsafe credential handling patterns |
| W008 | HIGH | Hardcoded secrets in skill files |
| W011 | MEDIUM | Untrusted external content ingestion |
| TF001 | HIGH | Toxic data flows between components |

## Steps

1. **Determine scan scope.** Ask the user what to scan:
   - A specific skill: `uvx snyk-agent-scan@latest --skills <path/to/SKILL.md>`
   - A skill directory: `uvx snyk-agent-scan@latest --skills <path/to/skills/>`
   - All Claude Code skills: `uvx snyk-agent-scan@latest --skills ~/.claude/skills`
   - All OpenClaw workspace skills: `uvx snyk-agent-scan@latest --skills skills/`
   - Full agent + MCP scan: `uvx snyk-agent-scan@latest --skills`

2. **Run the scan.**
   ```bash
   export SNYK_TOKEN="$SNYK_TOKEN"
   uvx snyk-agent-scan@latest --skills <target> --json 2>/dev/null
   ```
   - Add `--json` for structured output (recommended for automated pipelines)
   - Add `--full-toxic-flows` for deep toxic flow analysis on high-risk components
   - Add `--verbose` for detailed logging during troubleshooting

3. **Check for ClawHavoc indicators.** Independently of Snyk results, check for:
   ```bash
   # Origin tracking files from ClawHub
   find <target> -name "origin.json" -path "*/.clawhub/*" -o -name "origin.json" -path "*/.clawdhub/*"
   # Known C2 IP
   grep -r "91.92.242.30" <target>
   # External binary download patterns
   grep -ri "mediafire.com\|mega.nz\|clawdhub install" <target>
   ```
   Any match is a HIGH severity finding regardless of Snyk results.

4. **Format and report findings.** Structure the report as:
   ```
   ## Snyk Security Scan Report
   **Scan date:** YYYY-MM-DD HH:MM
   **Target:** <path>
   **Components scanned:** N
   **Findings:** X critical, Y high, Z medium, W low

   ### Critical Findings
   - [E004] `skills/foo/SKILL.md` — Prompt injection detected in instruction body
     **Remediation:** Remove or sanitize the injected instruction pattern

   ### High Findings
   ...

   ### Verdict
   PASS (zero critical/high) | FAIL (N blockers found)
   ```

5. **Save the report** to `memory/quality/security-scans/YYYY-MM-DD-<target-slug>.md`.

## Output

- Structured scan report with severity-ranked findings
- PASS/FAIL verdict (FAIL if any CRITICAL or HIGH findings)
- Remediation guidance for each finding
- ClawHavoc indicator check results

## Error Handling

- If `SNYK_TOKEN` is not set: "Set SNYK_TOKEN in ~/.openclaw/.env — get your token from https://app.snyk.io/account"
- If `uvx` is not installed: "Install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"
- If scan times out: Retry with `--server-timeout 30`
- If API returns 401: "SNYK_TOKEN is invalid or expired — regenerate at https://app.snyk.io/account"
- If no skills found at path: "No SKILL.md files found at <path> — verify the target path"
