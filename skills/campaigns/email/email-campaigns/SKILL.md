---
name: campaign-workflow
description: Use when orchestrating a full multi-channel campaign from topic to delivery — the 9-phase pipeline from intake through audit
version: "1.0.0"
author: "your-org"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /generate-campaign
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["curl", "jq", "npx", "python3"]
      env: ["CAMPAIGN_API_KEY", "CAMPAIGN_API_ENDPOINT"]
      os: ["darwin"]
---

# Campaign Workflow

Full 9-phase orchestration sequence for multi-channel campaigns. Loaded by Atlas (campaign-orchestrator agent) when triggered with "generate campaign for [topic]".

This skill coordinates the pipeline. API plumbing lives in `campaign-api`, `event-api`, and `offer-api` skills. Copy and code generation are delegated to specialist agents.

## MANDATORY: Tool Call Enforcement

Before executing any pipeline step, you MUST use actual tool calls:
1. `exec` for shell commands (mkdir, cp, python3)
2. `write` for creating/updating files (state.yaml, contracts, staging files)
3. `read` for reading files (contracts, artifacts, skill files)

Do NOT describe what you would do. Actually invoke the tools. If you report "Created directory X" without an `exec: mkdir -p X` tool call, the files do not exist.

## Pipeline State and Contract Management

When running the campaign pipeline, the orchestrator MUST:

1. Create a pipeline directory: `memory/pipelines/campaign-YYYY-MM-DD-[slug]/`
2. Copy contract templates from `skills/marketing/campaigns/contracts/` to the pipeline directory, replacing `{{campaign_id}}` with the actual campaign slug
3. Write a pipeline state file: `memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml`
   - Use `schema_version: 2` format.
   - Pre-populate ALL stages as `pending` with `approval_guard: true` on stages that require the operator's explicit approval (Phase 4 Approval, Phase 6 Infrastructure & Delivery).
   - Example skeleton:
     ```yaml
     schema_version: 2
     pipeline_id: campaign-YYYY-MM-DD-[slug]
     stages:
       intake:        { status: pending }
       phase2-assets: { status: pending }
       brand-gate:    { status: pending }
       email-e2e:     { status: pending }
       qa:            { status: pending }
       approval:      { status: pending, approval_guard: true }
       anchor-record: { status: pending }
       delivery:      { status: pending, approval_guard: true }
       activation:    { status: pending }
       measurement:   { status: pending }
       audit:         { status: pending }
       review:        { status: pending }
     ```
4. **CRITICAL — Workspace scoping**: Sub-agents resolve file paths relative to their OWN workspace directory, NOT the repo root. Use this workspace lookup:

   | Agent ID | Workspace (relative to repo root) |
   |---|---|
   | `agents-marketing-copywriter` | `agents/marketing/copywriter/` |
   | `agents-marketing-email-engineer` | `agents/marketing/email-engineer/` |
   | `agents-frontend-designer` | `agents/frontend/designer/` |
   | `agents-frontend-engineer` | `agents/frontend/engineer/` |

   **Before each `sessions_spawn`**:
   a. Copy the contract INTO the sub-agent's workspace:
      ```
      exec: mkdir -p <agent-workspace>/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
      exec: cp memory/pipelines/campaign-YYYY-MM-DD-[slug]/<stage>-handoff.yaml <agent-workspace>/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
      ```
   b. Include both the contract path AND the pipeline state path in the task: `handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/<stage>-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml`

   **After each sub-agent completes**:
   c. Copy the artifact FROM the sub-agent's workspace back to repo root:
      ```
      exec: cp <agent-workspace>/<artifact_path> <artifact_path>
      ```
5. After spawning a child agent, WAIT for the completion event. Do NOT poll. Do NOT call sessions_list. The completion event arrives automatically as a message in your session. After it arrives, continue to the next step.
6. After each sub-agent completes, verify the contract by running:
   ```
   exec: python3 -c "
   import json, sys
   sys.path.insert(0, '.')
   from compiler.engine.contract_assertions import run_assertions
   r = run_assertions('memory/pipelines/campaign-YYYY-MM-DD-[slug]/<stage>-handoff.yaml', '.')
   print(json.dumps({'passed': r.passed, 'total': r.total, 'failures': [{'type': f.assertion_type, 'detail': f.detail} for f in r.failures]}))
   "
   ```
   If verification fails, STOP the pipeline and notify the operator with the specific failures.
   Do NOT proceed to the next stage if any assertion fails.
7. Update pipeline state after each stage completes and emit a governance event to Paperclip (non-fatal — pipeline continues even if Paperclip is offline):
   ```bash
   python3 scripts/paperclip-event.py stage campaign-YYYY-MM-DD-[slug] <from_stage> <to_stage> --agent "Marketing Campaign Orchestrator"
   ```
   Replace `YYYY-MM-DD-[slug]` with the campaign run ID, and `<from_stage>/<to_stage>` with the stage names (e.g., `intake→phase2`, `phase2→gate`, `gate→approval`, `approval→deliver`).

## Step 0 — Resume Check

Before starting a new pipeline, invoke `/resume-pipeline campaign`. Interpret the response:

- **resume**: Skip to the indicated stage with the provided `prior_work` artifacts. Do not re-run completed stages.
- **complete**: Report pipeline completion to the operator. No further action needed.
- **escalate**: A guarded stage requires fresh current-session approval from the operator. Stop and ask before proceeding.
- **restart**: Begin a fresh pipeline from scratch (legacy state or no existing pipeline found).

If no in-progress pipeline exists, proceed normally with a fresh pipeline.

## Execution Model

**CRITICAL: Do NOT stop between phases to ask the user for permission.** Run the entire pipeline from intake through the approval gate autonomously. The ONLY stop point is the approval gate, where you post the preview and wait for the user to reply.

**Do NOT say** "Next I can proceed..." or "Shall I continue?" — just continue.

### Preferred: Autonomous Single-Turn (Agent Squad)

Check Agent Squad sidecar first: `curl -sf http://localhost:18790/health`

If available, use the `coordinate` skill to dispatch ALL asset agents in parallel within a single turn:

1. Run Phase 1 (Intake) — produce strategy, create contracts
2. Write all copy assets directly (you handle copy for v2 campaigns with existing source material)
3. Use `coordinate` skill to dispatch Forge (HTML), Canvas (design), Nova (build) in parallel
4. Run brand gate (Phase 3) on all assets
5. Post approval preview — STOP and wait

This completes in 1-2 turns instead of 6.

### Fallback: Multi-Turn Serial (sessions_spawn)

If Agent Squad is unavailable, fall back to serial delegation. Each `sessions_spawn` requires yielding:

1. **Turn 1**: Setup + intake + spawn Quill for copy → YIELD
2. **Turn 2**: Verify copy, spawn Forge for HTML → YIELD
3. **Turn 3**: Verify HTML, run brand gate, spawn Canvas → YIELD
4. **Turn 4**: Verify design, spawn Nova → YIELD
5. **Turn 5**: Verify build, run QA, post approval → STOP

After spawning each child, your turn ENDS. The child's result arrives as a new message — CONTINUE from where you left off. Do NOT ask the user for permission between turns.

Campaigns without landing pages skip Canvas/Nova. Campaigns without email assets skip Forge.

## Phase 1 — Intake & Research

1. Write `memory/campaigns/YYYY-MM-DD-[slug].md` with topic, campaign_type, timestamp
2. Load `marketing/campaign-strategy` skill — determine campaign type (retreat launch, webinar, newsletter, workshop), target segment, persona framework
3. If campaign type is `retreat` or `webinar`: call `airtable-retreats` skill to fetch live capacity (spots remaining, dates). Record in staging file. Flag if spot count is unconfirmed.
4. Call `senja` skill to fetch 1-2 relevant testimonials matching the target segment. Record in staging file with attribution.
5. If topic is novel or brand-adjacent: call `marketing/voice-calibration` skill to confirm tone, persona, and any language constraints before delegating
6. If campaign includes a multi-email sequence: consult `marketing-funnel` agent — "Design the email sequence structure for [topic] targeting [segment]." Record funnel design in staging file.

**Marketing skills to consider at intake:**
- `marketing/marketing-psychology` — select 2-3 behavioral models that fit the target segment and campaign goal
- `marketing/analytics-tracking` — define the event taxonomy for this campaign (which DISCOVER/ENGAGE/CONVERT/DEEPEN events to track)
- `marketing/ab-test-setup` — if this is a repeating campaign type, define one A/B test hypothesis for the highest-leverage asset

## Phase 2 — Asset Generation (Parallel Coordination)

Phase 2 uses the `coordinate` skill to run independent asset generation agents concurrently. Copy tasks (landing page, email) and HTML build run in parallel, reducing duration from 4-5x to ~1.5x single-agent time.

**Sidecar health check**: Before Phase 2, call `curl -sf http://localhost:18790/health`. If the sidecar is unavailable, fall back to serial execution (documented in Fallback section below).

### Phase 2 Setup (before dispatching agents)

Before dispatching any agents in Phase 2:
1. Create all required pipeline contracts in `memory/pipelines/campaign-YYYY-MM-DD-[slug]/`
2. Copy each contract INTO the target agent's workspace (workspace scoping — agents resolve paths relative to their own workspace):

   | Agent ID | Workspace (relative to repo root) |
   |---|---|
   | `agents-marketing-copywriter` | `agents/marketing/copywriter/` |
   | `agents-marketing-email-engineer` | `agents/marketing/email-engineer/` |
   | `agents-website-visual-designer` | `agents/website/visual-designer/` |
   | `agents-website-frontend-engineer` | `agents/website/frontend-engineer/` |

   ```
   exec: mkdir -p agents/marketing/copywriter/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   exec: cp memory/pipelines/campaign-YYYY-MM-DD-[slug]/copy-handoff.yaml agents/marketing/copywriter/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   exec: mkdir -p agents/marketing/copywriter/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   exec: cp memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy-handoff.yaml agents/marketing/copywriter/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   exec: mkdir -p agents/marketing/email-engineer/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   exec: cp memory/pipelines/campaign-YYYY-MM-DD-[slug]/html-handoff.yaml agents/marketing/email-engineer/memory/pipelines/campaign-YYYY-MM-DD-[slug]/
   ```

3. Assign unique `artifact_path` values for each task (paths must not collide):
   - Landing page copy → `memory/pipelines/campaign-YYYY-MM-DD-[slug]/lp-copy.md`
   - Email copy → `memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy.md`
   - Email HTML → `memory/pipelines/campaign-YYYY-MM-DD-[slug]/email.html`

### Phase 2 Parallel Dispatch

Load `coordinate` skill and dispatch the following agents in parallel:

```json
{
  "pipeline": "campaign",
  "stage": "phase2-assets",
  "tasks": [
    {
      "agent_id": "agents-marketing-copywriter",
      "task": "Write landing page copy for [topic]. Segment: [segment]. Transformation story context: [from transformation-story skill]. Testimonials: [from senja]. Reference page-cro for CRO framework.\n\nQuill: reference marketing/page-cro (7-layer CRO framework, trust signals, objection handling, CTA language), marketing/free-offer-strategy (if landing page is for a free offer).",
      "artifact_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/lp-copy.md",
      "contract_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/copy-handoff.yaml"
    },
    {
      "agent_id": "agents-marketing-copywriter",
      "task": "Write email copy for [topic]. Segment: [segment]. Funnel structure: [from step 6]. Request: subject line variants (min 5), preview text, full body copy per email.\n\nQuill: reference marketing/email-sequence-frameworks (lifecycle sequence archetypes, emotional pacing), marketing/copy-editing (Eight Sweeps before finalizing).",
      "artifact_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy.md",
      "contract_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy-handoff.yaml"
    },
    {
      "agent_id": "agents-marketing-email-engineer",
      "task": "Build email HTML for [topic]. Copy: [provide email copy text inline or path]. Photo: [from media selection step]. Template domain: [onboarding/marketing/sales].\n\nForge: load email-design-system skill for the brand design tokens. Request: production TSX template registered in render.ts, with plain-text version.",
      "artifact_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/email.html",
      "contract_path": "memory/pipelines/campaign-YYYY-MM-DD-[slug]/html-handoff.yaml"
    }
  ]
}
```

After the coordinate call returns:
- Copy artifacts from agent workspaces back to repo root (see `coordinate` skill step 5)
- Run contract assertions for each successful artifact (see `coordinate` skill step 6)
- If any assertions fail: STOP and notify the operator

7. (Parallel result) **Landing page copy** — artifact at `memory/pipelines/campaign-YYYY-MM-DD-[slug]/lp-copy.md`
8. **Media selection** — run after parallel dispatch completes (media selection is non-delegated, run locally):
   - Use `photo-semantic-search` skill for abstract/emotional queries ("transformation energy", "sacred communal space") — HyDE + ChromaDB retrieval + LLM re-ranking, returns top 3 with CDN URLs and alt text
   - Use `retreat-photos` skill for specific subject searches ("fire ceremony", "yoga on deck") — keyword jq search against 1,267 indexed photos with 72 priority selections
   - For page-level curation (multiple sections): use `retreat-photos` Page-Level Curation Mode (PC-1 through PC-8) — batches all sections, skips icon/stats components, presents unified approval gate
   - Apply placement-specific CDN transforms: hero `?w=1600`, card `?w=800`, email `?w=600&format=jpeg`, thumbnail `?w=400`
   - Generate WCAG-compliant alt text for each selected photo
   - Present all selections to the operator for approval before finalizing — do not embed unapproved photos
9. (Parallel result) **Email copy** — artifact at `memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy.md`
10. (Parallel result) **Email HTML** — artifact at `memory/pipelines/campaign-YYYY-MM-DD-[slug]/email.html`. Forge must load `email-design-system` skill for the brand design tokens (colors, typography, layout, buttons), React Email component rules, deliverability requirements, and the new template checklist

### Phase 2 Fallback — Serial Execution

If `curl -sf http://localhost:18790/health` fails, fall back to serial `sessions_spawn`:

1. **Landing page copy** — Copy `skills/marketing/campaigns/contracts/copy-handoff.yaml` to pipeline directory. Delegate via `sessions_spawn` to `agents-marketing-copywriter`:
   `"handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/copy-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml\n\nWrite landing page copy for [topic]. Segment: [segment]. Transformation story context: [from transformation-story skill]. Testimonials: [from senja]. Reference page-cro for CRO framework."`
   After copywriter returns, copy artifact from workspace to repo root, run assertion verification on the contract.
2. **Email copy** — Copy `copy-handoff.yaml` as `email-copy-handoff.yaml`. Delegate via `sessions_spawn` to `agents-marketing-copywriter`:
   `"handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/email-copy-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml\n\nWrite email copy for [topic]. Segment: [segment]. Funnel structure: [from step 6]."`
   After copywriter returns, copy artifact, run assertions.
3. **Email HTML** — Copy `html-handoff.yaml`. Delegate via `sessions_spawn` to `agents-marketing-email-engineer`:
   `"handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/html-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml\n\nBuild email HTML for [topic]. Copy: [from step 2]. Photo: [from media selection step]. Template domain: [onboarding/marketing/sales]."`
   After Forge returns, copy artifact, run assertions.
11. **SMS** — generate directly: 1 segment max, under 160 chars, from the operator, clear reply invitation, no substance-specific language for general sends
    - Reference: `marketing/sms-campaigns` skill for timing and compliance
12. **Thank-you** — generate directly: warm, 3-4 sentences, next steps, consistent with landing page voice
    - Reference: `marketing/post-signup-activation` (activation moments by funnel stage — what happens after signup)
13. **Forms** (if campaign includes registration/quiz/application): reference `marketing/form-cro` skill for field ordering, emotional safety, mobile-first defaults. If form is implemented in Typeform, use `typeform` skill (API CRUD for forms, responses, insights).

**SEO/GEO assets** (if campaign includes evergreen content pages):
14. Reference `marketing/programmatic-seo` for page archetype selection and GEO optimization
15. Reference `marketing/schema-markup` for JSON-LD structured data (Event, Course, FAQPage as applicable)
16. Reference `marketing/comparison-pages` if campaign includes decision-education content

**Paid traffic** (if campaign includes paid acquisition):
17. Reference `marketing/paid-ads` for platform selection, audience targeting, ad copy compliance, and funnel-aware structure

**Landing page build** (if campaign produces a new web page):
18. Copy `skills/marketing/campaigns/contracts/design-handoff.yaml` and `skills/marketing/campaigns/contracts/build-handoff.yaml` to pipeline directory. Two-agent sequential workflow:
    - **Design**: Delegate via `sessions_spawn` to `agents-frontend-designer`: `"handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/design-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml\n\nDesign landing page for [topic]. Copy: [from step 7]. Photos: [from step 8]."` After Canvas returns, verify design contract.
    - **Build**: Delegate via `sessions_spawn` to `agents-frontend-engineer`: `"handoff-contract: memory/pipelines/campaign-YYYY-MM-DD-[slug]/build-handoff.yaml pipeline-state: memory/pipelines/campaign-YYYY-MM-DD-[slug]/state.yaml\n\nBuild landing page from design spec. Design: [from Canvas output]."` After Nova returns, verify build contract.
    Both must read `<brand_root>/tokens/design-system.yaml` and `docs/web/web-ref.yaml`.
19. If campaign code is generated (TSX templates, page components, API routes): load `campaign-tdd` skill — mandatory TDD before commit. Do not proceed until `npx vitest run` reports 0 failures.

## Phase 3 — Brand Gate

20. Run all copy assets (landing page, email body, SMS, thank-you) through `marketing/brand-standards` skill. Flag any violations. Revise with originating agent before proceeding.
21. Run all copy through `marketing/copy-editing` skill (Eight Sweeps including Voice Sweep). Do not advance to Slack preview with a failing brand gate.
22. Run all copy through `humanizer` skill. Nothing enters the approval stage with AI writing patterns intact.

## Phase 3.5 — Email E2E Gate (before approval)

**Required for any campaign that has email assets.** Run before step 23 (consolidation).

For each email asset type in the campaign (`email_marketing`, `email_newsletter`, `email_transactional`):
1. Render the humanized HTML email to a temp file: `/tmp/campaign-e2e-<asset-slug>-YYYY-MM-DD.html`
2. Invoke `email-e2e` wrapped in `retry-gate`:

```yaml
retry-gate:
  operation: "exec python3 skills/qa/email-e2e/scripts/run_e2e.py --subject '${subject}' --html-file '${html_path}'"
  workflow: campaign
  step: "email-e2e-${asset_slug}"
  routing:
    content: quill
    engineering: forge
```

3. Each asset gets its own retry-gate state file: `memory/logs/retry/YYYY-MM-DD-campaign-email-e2e-<asset-slug>.md`
4. Phase 3.5 passes **only when ALL email assets pass**. A single EXHAUSTED asset blocks Phase 4.
5. **Skip Phase 3.5 entirely** if the campaign has zero email assets (e.g., SMS-only or landing-page-only campaigns).

On any asset EXHAUSTED: halt campaign. Notify the operator via iMessage with asset name and failure detail. Do not proceed to Phase 4 until the operator intervenes.

## Phase 3b — QA Orchestrator

22b. Dispatch `qa-engineer` sub-agent on each email HTML asset — run the 7-check suite (P0 mobile, P1 deliverability, P2 Gmail clipping, P3 dark mode, P4 link health, P5 images-off, P7 accessibility). Fix-loop: max 3 iterations routing issues to Nova (frontend) or Forge (email). Must achieve passing score.
22c. Dispatch `qa-content` sub-agent on all copy assets — brand voice validation (kill list, CTA alignment, teaching insight, humanizer). Routes content issues to Quill.
22d. If campaign includes a landing page: run `qa-engineer` in URL mode on the deployed preview URL — SEO checks, security headers, cross-device rendering.
22e. Persist all QA results via `POST /api/qa-results` with campaign_id and asset_id. Include QA scores in the Phase 4 approval post.

## Phase 4 — Approval

23. Consolidate all assets into `memory/campaigns/YYYY-MM-DD-[slug].md` — include approved photo selections with CDN URLs and alt text
24. Post complete preview to `#lumina-bot` in Slack: title, topic, segment, campaign type, all assets with labels, photo selections with thumbnails, E2E results summary, [Approve] / [Edit] / [Cancel]
25. Wait for explicit the operator approval. Do not proceed on timeout or ambiguous response.

On [Edit]: revise the specified asset(s) with the originating agent, re-run brand gate (Phase 3), re-stage, re-post for approval.
On [Cancel]: write cancellation reason to staging file, notify the operator via iMessage. Emit rejection to Paperclip:
   ```bash
   python3 scripts/paperclip-event.py approval campaign-YYYY-MM-DD-[slug] approval --rejected --approver austin
   ```
On [Approve]: emit approval to Paperclip (audit log only — Slack is authoritative):
   ```bash
   python3 scripts/paperclip-event.py approval campaign-YYYY-MM-DD-[slug] approval --approved --approver austin
   ```

## Phase 5 — Anchor & Record Creation

26. If no event record exists yet: load `event-api` skill to create the event record. Capture `event_id`.
27. If no offer record exists yet: load `offer-api` skill to create the offer record. Capture `offer_id`.
28. Load `campaign-api` skill: `POST /api/campaigns` (create campaign record with anchor IDs)
29. `POST /api/campaigns/[id]/assets` for each asset (landing page, email HTML, SMS, thank-you)
30. `GET /api/campaigns/[id]` to verify submission succeeded

## Phase 6 — Infrastructure & Delivery (post-approval, on the operator's explicit send instruction)

**Campaign infrastructure** (for webinar/retreat campaign types):
31. If campaign type is `webinar` or `retreat`: load `zoom` skill — create a campaign-specific Zoom meeting via `zoom-cli.js create`. Capture `join_url`. Save Zoom link to campaign DB config via `PATCH /api/campaigns/[id]`.
32. Load `google-calendar-event` skill — create Google Calendar event on the configured calendar address with Zoom join URL, event details, and registrant attendees. Requires the operator's explicit confirmation before creating.

**Page deployment** (if campaign produced a new web page in Phase 2):
33. Load `deployment` skill — deploy to Vercel production (the configured production domain). Verify live domain serves updated content. Only deploy with the operator's explicit confirmation.

**Channel delivery:**
34. L-track email: `mailchimp` skill — create draft campaign with HTML from Forge, subject/preview from Lumina, list segment from intake
35. R-track email: `email-newsletter` skill — schedule transactional send via Resend
36. SMS: `sms-outreach` skill — route approved SMS copy to Twilio
37. Log each send to `attio` skill (contact-level record) + `resend/log-to-attio` (email delivery record)

## Phase 7 — Post-Send Activation

38. Reference `marketing/post-signup-activation` to set up post-signup nurture sequence (confirmation, pre-event warmup, show-up optimization)
39. If campaign has a referral component: reference `marketing/referral-program` for timing and anti-transactional framing

## Phase 8 — Measurement Setup

40. Reference `marketing/analytics-tracking` to verify all campaign events are instrumented (registrations, email opens, page views by content type, conversions)
41. If A/B test was defined in Phase 1: reference `marketing/ab-test-setup` to confirm test is properly configured with sample size and success criteria

## Phase 9 — Audit

42. iMessage to the operator: "Campaign '[title]' submitted. ID: [id]. Assets: [count]. Delivery routed: [channels]."
43. Write submit + delivery record to `memory/logs/api-submits/YYYY-MM-DD.md`

## Phase 10 — Post-Launch Review

44. Load `review-campaign` skill — fetch the campaign from the DB, audit all assets against current brand and copy standards, identify gaps (missing asset types for the campaign type), flag off-brand language or outdated content. Stage proposed fixes for the operator's approval before PATCHing.
45. If review surfaces issues: revise with originating agent, re-run brand gate, re-post fix preview to Slack. Log review results to `memory/logs/api-submits/YYYY-MM-DD.md`.

## Skill Cross-Reference

| Phase | Skills Used |
|---|---|
| 1. Intake | `campaign-strategy`, `voice-calibration`, `airtable-retreats`, `senja`, `marketing-psychology`, `analytics-tracking`, `ab-test-setup` |
| 2. Generate | `transformation-story`, `email-sequences`, `email-sequence-frameworks`, `email-design-system`, `page-cro`, `free-offer-strategy`, `copy-editing`, `sms-campaigns`, `post-signup-activation`, `form-cro`, `typeform`, `programmatic-seo`, `schema-markup`, `comparison-pages`, `paid-ads`, `photo-semantic-search`, `retreat-photos`, `frontend`, `campaign-tdd` |
| 3. Brand Gate | `brand-standards`, `copy-editing`, `humanizer` |
| 3.5. Email E2E | `email-e2e`, `retry-gate` |
| 5. Record | `event-api`, `offer-api`, `campaign-api` |
| 6. Infrastructure & Delivery | `zoom`, `google-calendar-event`, `deployment`, `mailchimp`, `email-newsletter`, `sms-outreach`, `attio`, `resend/log-to-attio` |
| 7. Activation | `post-signup-activation`, `referral-program` |
| 8. Measurement | `analytics-tracking`, `ab-test-setup` |
| 10. Review | `review-campaign` |
