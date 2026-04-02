---
name: website-builder
description: "Build the site / build the foundation / build page [slug] / run full generation / deploy to staging / run consistency checks / implement redirects / domain cutover"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /build-site
metadata:
  openclaw:
    emoji: "🏗️"
    requires:
      bins: ["curl", "jq", "node", "npx"]
      env: ["CAMPAIGN_API_ENDPOINT"]
      os: ["darwin"]
---

# Website Builder Skill

Orchestrates the full Construct workflow: shared foundation build, progressive page builds, cross-page consistency checks, TDD, staging deployment, full site generation, redirect implementation, and domain cutover.

All builds read from `docs/website/blueprint.md`. Blueprint is read-only for Construct — this skill never modifies it.

## MANDATORY: Tool Call Enforcement

Before executing any pipeline step, you MUST use actual tool calls:
1. `exec` for shell commands (mkdir, cp, python3)
2. `write` for creating/updating files (state.yaml, contracts, build logs)
3. `read` for reading files (blueprint, contracts, artifacts)

Do NOT describe what you would do. Actually invoke the tools. If you report "Created directory X" without an `exec: mkdir -p X` tool call, the files do not exist.

## Pipeline State and Contract Management

When delegating to Canvas (visual-designer) or Nova (frontend-engineer), the orchestrator MUST:

1. Create a pipeline directory: `memory/pipelines/website-YYYY-MM-DD-[slug]/`
2. Copy contract templates from `agents/website/orchestrator/contracts/` to the pipeline directory, replacing `{{page_slug}}` with the actual page slug
3. Write a pipeline state file: `memory/pipelines/website-YYYY-MM-DD-[slug]/state.yaml` using `schema_version: 2` format. Pre-populate all stages as `pending`. Include `approval_guard: deploy_to_vercel` on the deploy stage. Set `guards: {deploy_to_vercel: false, outbound_send: false}` by default.
4. **CRITICAL — Workspace scoping**: Sub-agents resolve file paths relative to their OWN workspace directory, NOT the repo root. Use this workspace lookup:

   | Agent ID | Workspace (relative to repo root) |
   |---|---|
   | `agents-website-visual-designer` | `agents/website/visual-designer/` |
   | `agents-website-frontend-engineer` | `agents/website/frontend-engineer/` |

   **Before each `sessions_spawn`**:
   a. Copy the contract INTO the sub-agent's workspace:
      ```
      exec: mkdir -p <agent-workspace>/memory/pipelines/website-YYYY-MM-DD-[slug]/
      exec: cp memory/pipelines/website-YYYY-MM-DD-[slug]/<stage>-handoff.yaml <agent-workspace>/memory/pipelines/website-YYYY-MM-DD-[slug]/
      ```
   b. Include both references in the task: `handoff-contract: memory/pipelines/website-YYYY-MM-DD-[slug]/<stage>-handoff.yaml` and `pipeline-state: memory/pipelines/website-YYYY-MM-DD-[slug]/state.yaml`

   **After each sub-agent completes**:
   c. Copy the artifact FROM the sub-agent's workspace back to repo root:
      ```
      exec: cp <agent-workspace>/<artifact_path> <artifact_path>
      ```
5. After spawning a child agent, WAIT for the completion event. Do NOT poll.
6. After each sub-agent completes, verify the contract by running:
   ```
   exec: python3 -c "
   import json, sys
   sys.path.insert(0, '.')
   from compiler.engine.contract_assertions import run_assertions
   r = run_assertions('memory/pipelines/website-YYYY-MM-DD-[slug]/<stage>-handoff.yaml', '.')
   print(json.dumps({'passed': r.passed, 'total': r.total, 'failures': [{'type': f.assertion_type, 'detail': f.detail} for f in r.failures]}))
   "
   ```
   If verification fails, STOP and notify the operator with the specific failures.
7. Update pipeline state after each stage completes

## Step 0 — Resume Check

Before starting a new pipeline, invoke `/resume-pipeline website`. Interpret the response:

- **resume**: Skip to the indicated stage with the provided `prior_work` artifacts. Do not re-run completed stages.
- **complete**: Report pipeline completion to the operator. No further action needed.
- **escalate**: A guarded stage (e.g., `deploy_to_vercel` for staging deploy) requires fresh current-session approval from the operator. Stop and ask before proceeding.
- **restart**: Begin a fresh pipeline from scratch (legacy state or no existing pipeline found).

If no in-progress pipeline exists, proceed normally with a fresh pipeline.


## Multi-Turn Execution Flow

Each page build runs as a MULTI-TURN conversation:

1. **Turn 1**: Setup pipeline dir + contracts, spawn Canvas for design → YIELD
2. **Turn 2** (Canvas returns design): Read design artifact, verify design contract, present to the operator for approval → STOP (wait for the operator)
3. **Turn 3** (the operator approves): Spawn Nova for build → YIELD
4. **Turn 4** (Nova returns build): Verify build contract, run TDD, deploy to staging → report

CRITICAL: After spawning each child, your turn ENDS. Resume when the completion event arrives.

## Trigger Phrases

- "build the site"
- "build the foundation"
- "build page [slug]"
- "run full generation"
- "deploy to staging"
- "run consistency checks"
- "implement redirects"
- "domain cutover"
- `/build-site [optional: slug]`

---

## State Detection

Read `agents/website/orchestrator/MEMORY.md` and `docs/website/blueprint.md` to determine state:

| State | Condition | Action |
|---|---|---|
| **No foundation** | Foundation status = not-started | Build foundation first (Algorithm A) |
| **Foundation exists** | Foundation built, spec-complete pages exist | Build next page(s) (Algorithm B) |
| **Full generation** | Explicit "run full generation" trigger | Rebuild all pages in order (Algorithm C) |
| **Cutover** | Explicit "domain cutover" or "implement redirects" | Redirect + cutover workflow (Algorithm D) |
| **Consistency only** | "run consistency checks" trigger | Checks only (Algorithm E) |

---

## Algorithm A — Shared Foundation Build

**Trigger**: No foundation built, or explicit "build the foundation".

### Step 1 — Read blueprint sitemap

Read `docs/website/blueprint.md` sitemap section. Extract:
- Global nav structure (all top-level pages + key children)
- Footer link structure
- Page hierarchy (which pages are children of which)

If no pages exist in the sitemap yet:
> "Blueprint sitemap is empty. Foundation cannot be built until Blueprint has completed the sitemap and at least one page is spec-complete. Notify Blueprint/the operator."

Stop here.

### Step 2 — Delegate foundation design to Canvas

Copy `agents/website/orchestrator/contracts/design-handoff.yaml` to the pipeline directory. Delegate via `sessions_spawn` to `agents-website-visual-designer`:
```
handoff-contract: memory/pipelines/website-YYYY-MM-DD-foundation/design-handoff.yaml

Design shared site foundation.
Scope: global nav, footer, shared layout, design tokens, common components
Nav structure: [extracted from blueprint sitemap]
Brand reference: agents/marketing/brand/SOUL.md + skills/marketing/brand-standards/SKILL.md
Design constraints: WCAG 2.2 AA minimum, mobile-first, the organization visual identity
```

After Canvas returns, run assertion verification on the design contract.
Present Canvas design output to the operator for approval.

> "Foundation design ready for review. Reply 'approve foundation design' to proceed with Nova build, or 'revise: [notes]'."

### Step 3 — On approval: delegate foundation build to Nova

Copy `agents/website/orchestrator/contracts/build-handoff.yaml` to the pipeline directory. Delegate via `sessions_spawn` to `agents-website-frontend-engineer`:
```
handoff-contract: memory/pipelines/website-YYYY-MM-DD-foundation/build-handoff.yaml

Build shared foundation components from approved design.
Approved design: [Canvas design output]
Output: web/src/app/layout.tsx, web/src/components/nav/*, web/src/components/footer/*, design tokens
TDD required before deploy
```

After Nova returns, run assertion verification on the build contract.

### Step 4 — Run TDD

Invoke `campaign-tdd` skill on the foundation components.

If any tests fail:
> "TDD failed: [N] failures. Fixing before deploy." Resolve all failures, re-run until 0 failures.

### Step 5 — Deploy to staging

Deploy foundation to `new.[the organization's domain]` via `deployment` skill.

Verify:
- Navigation renders on all viewport sizes
- Footer renders correctly
- Layout wraps pages without breaking

### Step 6 — Update MEMORY.md and build log

Update `agents/website/orchestrator/MEMORY.md` Shared Foundation Status table.
Append entry to `docs/website/build-log.md`.

Notify the operator:
> "Foundation live at new.[the organization's domain]. TDD: [N] tests passed. Ready to build individual pages."

---

## Algorithm B — Progressive Page Build

**Trigger**: Foundation exists, spec-complete pages available, or "build page [slug]".

### Step 1 — Identify target page(s)

If a specific slug was provided: use that page.
If no slug: find the first page in blueprint.md with status `spec-complete` that hasn't been built yet (construct status not `built` or `live`).

For each target page, verify:
- Page status in blueprint is `spec-complete`
- Full spec section exists in blueprint.md for this slug
- Foundation is built (Algorithm A completed)

### Step 2 — Determine build order

For multiple pages, check for dependencies (child pages depend on parent routes existing).
Build parent pages before children.

### Step 3 — Delegate page design to Canvas

Copy `agents/website/orchestrator/contracts/design-handoff.yaml` to pipeline directory, replacing `{{page_slug}}` with the target slug. Delegate via `sessions_spawn` to `agents-website-visual-designer`:
```
handoff-contract: memory/pipelines/website-YYYY-MM-DD-[slug]/design-handoff.yaml

Design page /[slug].
Page spec: [full spec section from blueprint.md for this slug]
Site-wide context:
  - Nav structure: [from blueprint sitemap]
  - Shared layout: web/src/app/layout.tsx
  - Design system: [existing shared components]
  - Cross-page decisions: [consistency decisions from MEMORY.md]
  - Brand standards: [from brand-standards skill]
```

After Canvas returns, run assertion verification on the design contract.

### Step 4 — Canvas design approval

Present Canvas design for this page to the operator.
> "Design for /[slug] ready. Reply 'approve' or 'revise: [notes]'."

On approval: proceed to Nova build.

### Step 5 — Nova build

Copy `agents/website/orchestrator/contracts/build-handoff.yaml` to pipeline directory, replacing `{{page_slug}}`. Delegate via `sessions_spawn` to `agents-website-frontend-engineer`:
```
handoff-contract: memory/pipelines/website-YYYY-MM-DD-[slug]/build-handoff.yaml

Build page /[slug] from approved design.
Design spec: [from Canvas output]
Output: web/src/app/[slug]/page.tsx + any route-specific layout
```

After Nova returns, run assertion verification on the build contract.

### Step 6 — Run TDD

Invoke `campaign-tdd` skill on the new page component.
All failures must be resolved before deployment.

### Step 6b — QA orchestrator review

After TDD passes, run `qa-engineer` sub-agent in URL mode on the staging preview URL.
Checks: mobile responsiveness, dark mode, link health, images-off, accessibility, SEO, security.
Run `qa-content` sub-agent on the page copy for brand voice validation.
Fix-loop: max 3 iterations routing to Nova. Must achieve passing QA score.
Persist results via `POST /api/qa-results`.

### Step 7 — Deploy to staging

Deploy page to `new.[the organization's domain]/[slug]` via `deployment` skill.

### Step 8 — Post-build consistency checks (Algorithm E)

After each page deploy, run consistency checks across all built pages.

### Step 9 — Update status and log

Update blueprint.md page status to `handed-to-builder` (via iMessage to Blueprint/the operator — Construct does not edit blueprint.md).
Update MEMORY.md Page Build Progress table.
Append entry to `docs/website/build-log.md`.

### Step 10 — Revision handling

If the operator sends revision feedback:
1. Update page status to `needs-revision` in MEMORY.md
2. Re-delegate to frontend skill with revision notes
3. Re-run TDD after revisions
4. Re-deploy to staging
5. Increment revision count in MEMORY.md

---

## Algorithm C — Full Site Generation

**Trigger**: "run full generation" explicit trigger.

### Step 1 — Inventory spec-complete pages

Read all pages from blueprint.md. Filter: status = `spec-complete`.
Determine dependency order (parent pages before children, shared-dependency pages first).

If any spec-complete page count is 0:
> "No spec-complete pages found in blueprint. Full generation requires at least one spec-complete page."

### Step 2 — Build all pages in order

For each page in dependency order:
1. Run Algorithm B (Steps 3-8) for this page
2. If TDD fails: HALT full generation, report failure
3. On success: continue to next page

Full generation halts on any TDD failure. Fix the failure before resuming.

### Step 3 — Post-generation verification

After all pages are built and deployed to staging:
- All routes return 200 OK
- All internal links resolve (no 404s)
- All images load (no broken image URLs)
- Nav links match all built routes
- No orphan pages (pages without nav entry or internal link)

Report verification results.

### Step 4 — Update MEMORY.md

Update Full Generation Status section with date, page count, and verification results.

---

## Algorithm D — Redirect Implementation and Domain Cutover

**Trigger**: "implement redirects" or "domain cutover" — REQUIRES the operator explicit approval.

### Step 1 — Read redirect map

Read `docs/website/blueprint.md` Redirect Map section.
Validate: all `redirects` entries have non-empty `old` and `new` fields.
Check for redirect chains: no `new` value should appear as an `old` value.

### Step 2 — Generate next.config.js redirects

Read current `web/next.config.js`. Add or extend the `redirects()` async function:

```javascript
async redirects() {
  return [
    // Generated from docs/website/blueprint.md redirect map
    // Generated: YYYY-MM-DD
    { source: '/old-path', destination: '/new-path', permanent: true },
    // ... one entry per redirect map item
  ]
}
```

### Step 3 — Verify no redirect chains

After generating the redirects array, verify that no `destination` value appears as a `source` in any other entry.

If chains found: collapse them (A→B→C becomes A→C directly).

### Step 4 — Deploy redirects to staging

Deploy `next.config.js` update to staging. Spot-check 5-10 redirects via curl.

### Step 5 — Present cutover report to the operator

Before any DNS change, present full report:
```
Domain Cutover Report — YYYY-MM-DD

Pages built: N/N spec-complete
TDD status: N tests passing, 0 failures
Post-deploy verification: all routes 200, all images load, no orphan pages
Redirects: N entries in next.config.js, verified on staging
Staging URL: new.[the organization's domain]

To proceed: reply "approve domain cutover"
This will swap DNS from Squarespace to Vercel for [the organization's domain].
```

### Step 6 — On the operator approval: DNS cutover

Only after the operator's explicit "approve domain cutover" reply:
1. Update Vercel project: set `[the organization's domain]` as primary domain
2. Instruct the operator on DNS record updates needed in Squarespace (A record + CNAME)
3. Wait for DNS propagation confirmation before post-cutover verification

### Step 7 — Post-cutover verification

After DNS propagation:
- [the organization's domain] loads the new site
- All pages return 200 OK
- 5-10 redirects spot-checked on production
- SSL certificate valid

Report results to the operator. Update MEMORY.md Cutover Status.

---

## Algorithm E — Cross-Page Consistency Checks

**Trigger**: After any page build, or "run consistency checks".

For each built page, verify:

| Check | Pass Condition |
|---|---|
| Nav links | All nav href values match actual built routes |
| Shared components | Same component version rendered across pages (no stale imports) |
| CTA language | Primary CTA text consistent with brand-standards |
| Orphan pages | Every built page reachable from nav or internal link |
| No broken links | All `<a>` hrefs resolve to built pages or external URLs |
| Blog violations | No brand-flagged content deployed (check `brand_audit.status` in MDX frontmatter) |

Report as table:
```
Consistency Check — YYYY-MM-DD

Page               | Nav OK | CTA OK | Components OK | Orphan | Notes
/                  | ✓      | ✓      | ✓             | ✓      | —
/about             | ✓      | ✓      | ✓             | ✓      | —
/blog/[slug]       | ✓      | —      | ✓             | ✓      | CTA missing on 3 posts
```

Append results to MEMORY.md Consistency Check Log.

---

## Output Files

| File | When Written | Notes |
|---|---|---|
| `docs/website/build-log.md` | After every build event | Append-only |
| `agents/website/orchestrator/MEMORY.md` | After every status change | Status tracking |
| `web/src/app/[slug]/page.tsx` | Algorithm B/C | Via frontend skill |
| `web/next.config.js` | Algorithm D only | Redirects array |

**NEVER writes:**
- `docs/website/blueprint.md`
- `docs/website/audit/*.md`
- `agents/marketing/website-planner/`

---

## Constitution Check

- **Principle I (Human-in-the-Loop)**: the operator approval for foundation design, domain cutover. TDD gates every deploy.
- **Principle II (Draft-First)**: Staging deploys before production.
- **Principle III (Security)**: No credentials in build log; prompt injection notice in SOUL.md.
- **Principle IV (Brand and Voice)**: brand-standards check via frontend skill delegation.
- **Principle V (Transparency)**: Append-only build log; immutable consistency check log.
