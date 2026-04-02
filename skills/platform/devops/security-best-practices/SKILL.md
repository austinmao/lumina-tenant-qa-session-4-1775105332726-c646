---
name: security-best-practices
description: Use when performing a security review or secure-by-default refactor for Python or JavaScript/TypeScript code, especially when checking secrets handling, auth boundaries, input validation, outbound integrations, or unsafe shell and file operations.
---

# Security Best Practices

## Overview

Use this skill for focused security review work. It is not a general code review skill.

Prioritize exploitable issues over style:
- secret exposure
- auth and authorization gaps
- command injection and unsafe shell execution
- SSRF and unsafe outbound fetches
- path traversal and unsafe file writes
- insecure webhook verification
- over-broad logging of PII or tokens

## Repo Focus

In this repo, inspect these areas first:
- `skills/` and `agents/` for prompt-driven tool usage and send flows
- `scripts/` and `workers/` for shell execution, webhooks, media processing, and file IO
- `web/` and `mcp-send-email/` for request handling, client/server boundaries, and config leaks
- `.env` usage, config loaders, and anything touching Airtable, Gmail, Slack, Zoom, Resend, Twilio, Attio, or Retreat Guru

## Review Process

1. Map trust boundaries.
2. Identify inputs from users, webhooks, email bodies, URLs, documents, and env vars.
3. Trace where those inputs reach shell commands, file paths, external APIs, templates, logs, or browser output.
4. Check whether validation, escaping, signature verification, and least-privilege controls exist.
5. Report findings by severity with concrete file references and an exploit path.

## Checklist

- Secrets are loaded from env, never hardcoded, logged, or committed.
- Webhooks verify signatures or shared secrets before side effects.
- User-controlled strings never reach shell commands without strict argument separation.
- File paths are normalized and constrained to intended directories.
- External fetches do not allow arbitrary internal hosts or token forwarding.
- Templates and markdown rendering do not allow unintended script execution.
- Logs avoid recipient PII, tokens, auth headers, and sensitive payload bodies.
- Permission-sensitive actions require explicit approval gates where expected.

## Output Format

Report:
- Critical
- High
- Medium
- Low
- Residual risks

For each finding include:
- what is vulnerable
- how it could be abused
- exact file path
- recommended fix

## When Not To Use

Do not use this as the primary skill for architecture cleanup, broad refactoring, or non-security modernization.
