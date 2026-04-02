---
name: campaign-tdd
description: "Use when running TDD for campaign artifacts"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /campaign-tdd
metadata:
  openclaw:
    emoji: "🧪"
    requires:
      bins: ["npx"]
      os: ["darwin"]
---

# Campaign TDD Skill

**Mandatory step after every campaign code generation.** Whenever OpenClaw produces new Next.js pages, API routes, or email templates for a campaign, this skill ensures TDD is run before the campaign is considered complete.

## When to invoke

Run this skill after any campaign pipeline that creates or modifies:
- `web/src/app/api/**/*.ts` — API routes
- `web/src/app/**/page.tsx` — Next.js page components
- `web/src/emails/campaigns/<campaign_id>-<slug>/**/*.tsx` — React Email templates

Do NOT invoke for copy-only changes (Mailchimp drafts, MEMORY.md, markdown guides).

## Protocol

### Step 1 — Inventory new code artifacts

List every new or modified file in:
- `web/src/app/api/`
- `web/src/app/**/page.tsx`
- `web/src/emails/campaigns/<campaign_id>-<slug>/`

### Step 2 — Invoke openclaw-tdd-engineer

Delegate to the `openclaw-tdd-engineer` Claude Code sub-agent with:

```
Run TDD for the [campaign-slug] campaign artifacts.

New code files to test:
[list each file from Step 1]

Per-artifact test requirements:

API routes (web/src/app/api/**):
  - 401/403 for missing or wrong auth tokens
  - 400 for missing or invalid required fields
  - 200 happy path — verify response shape AND side-effects (file writes, DB calls)
  - 500 when downstream dependency fails (mock fs/DB/API to throw)

Page components (web/src/app/**/page.tsx):
  - Every distinct render state (placeholder / active / expired / error)
  - Fail-safe: malformed or missing config → graceful fallback, no thrown error
  - Key text/elements present per state

Email templates (web/src/emails/**):
  - Renders without throwing with required props
  - Conditional sections render correctly (attendedLive: true vs false, etc.)
  - No required prop missing from the template call signature

TDD protocol:
1. Write all tests first
2. Run npx vitest run — confirm new tests fail (red)
3. Verify implementation makes them pass (green)
4. Report: N tests before → N+M tests after, any bugs found

Working directory: /Users/luminamao/Documents/Github/openclaw/web
```

### Step 3 — Gate on green

**Do not mark the campaign as complete until `npx vitest run` reports 0 failures.**

If tests reveal implementation bugs: fix the implementation, re-run, confirm green.

### Step 4 — Report to the operator

```
✅ Campaign TDD complete: [campaign-slug]

Tests: [N before] → [N after] (+[M] new)
Files covered: [list]
Bugs found: [N — describe if any] / None
All tests passing: ✅
```

### Test Mode Artifact

In `test_mode=true`, still write a deterministic completion note to
`memory/drafts/webinars/YYYY-MM-DD-[campaign-slug]-tdd-complete.md` even if the
delegated engineer is simulated or the code inventory is empty.

Use this shape:

```text
# TDD Complete — [campaign-slug]

Tests before: [N]
Tests after: [N or N+M]
Failures: 0
vitest output: simulated in test mode
Files covered:
- [file list or "no generated code artifacts found"]
```

## Test file location convention

| Artifact type | Test file location |
|---|---|
| `web/src/app/api/[name]/route.ts` | `web/src/tests/api/[name].test.ts` |
| `web/src/app/[path]/page.tsx` | `web/src/tests/pages/[path].test.tsx` |
| `web/src/emails/campaigns/<campaign_id>-<slug>/<Name>.tsx` | `web/src/tests/emails/campaigns/<campaign_id>-<slug>/<Name>.test.tsx` |

## Notes

- This skill does not write tests itself — it delegates to `openclaw-tdd-engineer`
- The `openclaw-tdd-engineer` writes tests, runs vitest, and fixes any failures
- This runs after every campaign, not just the first one
- Test count grows with each campaign — this is expected and correct
