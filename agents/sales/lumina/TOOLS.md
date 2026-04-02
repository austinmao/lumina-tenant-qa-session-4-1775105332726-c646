# Tools Configuration — Lumina

## Allowed Tools

- `memory.search` — retrieve contact context and conversation history
- `outbound.submit` — route sends through the outbound gate (email, SMS, iMessage)
- `sessions_spawn` — spawn sub-agents for skill execution
- `gateway.health` — check gateway status

## Deny List

The following tool groups are **never** available to this agent:

- **shell** — no shell execution (no `shell.execute`, `shell.run`, or equivalent)
- **file** — no direct filesystem reads or writes outside the workspace skill set
- **email** (direct) — all email must route through `outbound.submit`, never via direct API
- **browser** — no web browsing or URL fetching outside approved skill tools
- **runtime** — no code execution at runtime
- **automation** — no RPA or browser automation

## Notes

- Outbound sends always require `outbound.submit` (never direct channel APIs)
- Filesystem access is limited to read-only workspace files via `memory.search`
- No credentials, tokens, or secrets may be accessed directly; all API calls route through gateway tool handlers
