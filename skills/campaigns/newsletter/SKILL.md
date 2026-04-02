---
name: send-newsletter
description: "Use when drafting, reviewing, or sending a newsletter through the full pipeline"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /send-newsletter
metadata:
  openclaw:
    emoji: "📬"
    requires:
      env:
        - MAILCHIMP_API_KEY
        - DATABASE_URL
        - ATTIO_API_KEY
        - SLACK_BOT_TOKEN
        - HTML_PATH
      bins:
        - curl
        - jq
        - python3
---

# Newsletter Skill

## Overview

Orchestrates the full newsletter lifecycle: brief assembly,
Chain-of-Draft copy generation, brand gate, approval, segmented delivery, and
analytics. Route here for any request to write, draft, review, or send a newsletter.

## Newsletter Type Registry

| Type | Schedule | Audience | Persona |
|---|---|---|---|
| Sunday Service | Sunday 9 AM MT | All active subscribers (journey-staged) | Seth Godin × Wise Alchemist |
| Integration Dispatch | Ad hoc post-retreat | Alumni (30-90 days post-retreat) | Ram Dass register |
| Science Brief | Monthly | All subscribers | Science Translator |
| Community Letter | Quarterly | Full list | Communal "we" voice |
| Threshold Letter | Pre-retreat (7 days out) | Enrolled participants only | Storytelling Sage |

## Pipeline Map

```
trend-intelligence (Friday) → [the operator review window] → brief (Sunday) → draft → gate → [approval or auto-pilot] → deliver
                                                         ↑                                                           ↓
                                                    subject-line ←──────────────────────────────────────── re-engage (post-send cleanup)
                                                    segment ─────────────────────────────────────────────────────────↑
                                                    analytics (48h after deliver) ───────────────────────────────────→ brief (next issue)
```

## Pipeline State and Contract Management

When running the newsletter pipeline, the orchestrator MUST:

1. Create a pipeline directory: `memory/pipelines/newsletter-YYYY-MM-DD/`
2. Copy contract templates from `skills/marketing/email/newsletter/contracts/` to the pipeline directory, replacing `{{date}}` with today's date
3. Write a pipeline state file: `memory/pipelines/newsletter-YYYY-MM-DD/state.yaml`
4. **CRITICAL — Workspace scoping**: Sub-agents resolve file paths relative to their OWN workspace directory, NOT the repo root. The orchestrator (main agent) operates from the repo root. Use this workspace lookup for each delegation target:

   | Agent ID | Workspace (relative to repo root) |
   |---|---|
   | `agents-marketing-copywriter` | `agents/marketing/copywriter/` |
   | `agents-marketing-brand` | `agents/marketing/brand/` |

   **Before each `sessions_spawn`**:
   a. Copy the contract INTO the sub-agent's workspace so it can read it:
      ```
      exec: mkdir -p <agent-workspace>/memory/pipelines/newsletter-YYYY-MM-DD/
      exec: cp memory/pipelines/newsletter-YYYY-MM-DD/<stage>-handoff.yaml <agent-workspace>/memory/pipelines/newsletter-YYYY-MM-DD/
      ```
   b. Include the relative contract path in the task: `handoff-contract: memory/pipelines/newsletter-YYYY-MM-DD/<stage>-handoff.yaml`

   **After each sub-agent completes**:
   c. Copy the artifact FROM the sub-agent's workspace back to repo root so assertions can verify it:
      ```
      exec: cp <agent-workspace>/<artifact_path> <artifact_path>
      ```
      Example: `cp agents/marketing/copywriter/memory/drafts/2026-03-16-sunday-service.md memory/drafts/2026-03-16-sunday-service.md`

5. After spawning a child agent, WAIT for the completion event. Do NOT poll. Do NOT call sessions_list. The completion event arrives automatically as a message in your session. After it arrives, continue to the next step.
6. After copying the artifact back to repo root, verify the contract by running:
   ```
   exec: python3 -c "
   import json, sys
   sys.path.insert(0, '.')
   from compiler.engine.contract_assertions import run_assertions
   r = run_assertions('memory/pipelines/newsletter-YYYY-MM-DD/<stage>-handoff.yaml', '.')
   print(json.dumps({'passed': r.passed, 'total': r.total, 'failures': [{'type': f.assertion_type, 'detail': f.detail} for f in r.failures]}))
   "
   ```
   If verification fails (passed=false), STOP the pipeline and notify the operator with the specific failures.
   Do NOT proceed to the next stage if any assertion fails.
7. Update pipeline state after each stage completes and emit a governance event to Paperclip (non-fatal — pipeline continues even if Paperclip is offline):
   ```bash
   python3 scripts/paperclip-event.py stage newsletter-YYYY-MM-DD <from_stage> <to_stage> --agent "<agent-name>"
   ```
   Replace `YYYY-MM-DD` with the run date, `<from_stage>/<to_stage>` with the stage names (e.g., `brief→draft`, `draft→gate`, `gate→deliver`), and `<agent-name>` with the spawned sub-agent's Paperclip display name (e.g., "Marketing Copywriter").

8. **State file format**: New pipelines MUST write `state.yaml` using `schema_version: 2` format:
   - Pre-populate ALL stages as `status: pending` at pipeline creation time
   - Mark guarded stages with `approval_guard` where appropriate (e.g., `outbound_send` on the `deliver` stage)
   - Set `guards.outbound_send: false` by default — requires fresh current-session approval from the operator before the deliver stage proceeds
   - Pass `pipeline-state: memory/pipelines/<id>/state.yaml` in every `sessions_spawn` task string alongside the existing `handoff-contract:` reference
   - Example stage entry in `state.yaml`:
     ```yaml
     schema_version: 2
     stages:
       brief:
         status: pending
       draft:
         status: pending
       gate:
         status: pending
       deliver:
         status: pending
         approval_guard: outbound_send
     guards:
       outbound_send: false
     ```

## Step 0 — Resume Check

Before starting a new pipeline, invoke `/resume-pipeline newsletter`. Interpret the response:

- **resume**: Skip to the indicated stage with the provided `prior_work` artifacts. Do not re-run completed stages.
- **complete**: Report pipeline completion to the operator. No further action needed.
- **escalate**: A guarded stage (e.g., `outbound_send` for deliver) requires fresh current-session approval from the operator. Stop and ask before proceeding.
- **restart**: Begin a fresh pipeline from scratch (legacy state or no existing pipeline found).

If no in-progress pipeline exists, proceed normally with a fresh pipeline.

## Multi-Turn Execution Flow

This pipeline runs as a MULTI-TURN conversation, not a single-turn command. The flow is:

1. **Turn 1**: Setup contracts, run trend brief, run content brief, spawn copywriter → YIELD (wait for copywriter completion event)
2. **Turn 2** (copywriter completion event arrives): Read the draft artifact, spawn brand guardian → YIELD (wait for brand guardian completion event)
3. **Turn 3** (brand guardian completion event arrives): Read brand guardian results, write gate_status + Brand Gate checklist back to the draft file using the write tool, run assertion verification, post to Slack for approval → STOP before deliver

CRITICAL: After spawning each child, your turn ENDS. You will get the child's result as a new message. When that message arrives, CONTINUE the pipeline from where you left off. Track your progress in the pipeline state file so you know which step to resume.

Do NOT try to complete the entire pipeline in a single turn. Each `sessions_spawn` + `sessions_yield` ends your current turn. Resume when the completion event arrives.

## Sub-Skill Invocation Order

0. `trend-intelligence` — runs Friday 7 AM MT (automatic) or on-demand
1. `newsletter/sub-skills/segment` — resolve journey stages and suppression list
2. `newsletter/sub-skills/brief` — assemble content brief (events, testimonials, signals, trend brief, prior performance)
3. `newsletter/sub-skills/draft` — Chain-of-Draft copy generation; calls `subject-line` internally
4. `newsletter/sub-skills/gate` — brand kill list, link audit, Godin filter, humanizer
4.5. **Email E2E gate** — render draft to HTML, invoke `email-e2e` wrapped in `retry-gate` (see below); only after PASSED does pipeline proceed to step 4b
4b. **QA orchestrator** — dispatch `qa-engineer` and `qa-content` sub-agents for 7-check suite (mobile, deliverability, Gmail clipping, dark mode, links, images-off, accessibility) + brand content gate; fix-loop max 3 iterations routing to Nova/Forge/Quill; must achieve passing score before proceeding; results persisted to `qa_results` table via `POST /api/qa-results`
5. **Slack approval gate** — post to #lumina-bot; wait for [Approve] / [Edit] / [Cancel]; include QA score in the approval post
6. `newsletter/sub-skills/deliver` — render, outbound.submit via mailchimp channel, Postgres record, Attio log
7. `newsletter/sub-skills/re-engage` — post-send cleanup of inactive subscribers
8. `newsletter/sub-skills/analytics` — run 48h after deliver; feeds performance table back to brief

## Design Constraints

- Single-column layout, 600px max width
- 70/30 text-to-image ratio
- Mobile-first: 16px+ body font, 22-26px headers
- Tap targets: 44x44px minimum, 10px spacing between interactive elements
- Above-fold content (first 300-500px): must contain headline + primary CTA
- Total rendered height: under 2000px

## Compliance (CAN-SPAM — mandatory every send)

- Physical address in footer: [organization registered address]
- Unsubscribe link in every email — no exceptions
- Context line: "You're receiving this because you subscribed at [the organization's domain]"
- Do not send to any address not in the verified subscriber list

## Bounce Handling

- Hard bounce: set `status = 'hard_bounce'` in Postgres immediately; remove from Resend audience; never send again
- Soft bounce: retry after 24h; after 3 consecutive soft bounces set `status = 'soft_bounce_max'` and suppress
- On any 4xx/5xx from Resend during a batch: STOP immediately, log partial results, notify the operator in Slack

## Step 4.5 — Email E2E Gate (before Slack approval)

**Required for all newsletter types, including auto-pilot mode.** E2E must pass before Slack approval appears or auto-pilot sends.

Invoke `email-e2e` wrapped in `retry-gate`:

```yaml
retry-gate:
  operation: "exec python3 skills/qa/email-e2e/scripts/run_e2e.py --subject '${SUBJECT}' --html-file '${HTML_PATH}'"
  workflow: newsletter
  step: email-e2e
  routing:
    content: copywriter
    engineering: forge
```

Steps:
1. Render the gate-approved draft to an HTML file at `/tmp/newsletter-e2e-YYYY-MM-DD.html`
2. Invoke retry-gate with the rendered HTML and expected subject line
3. **On PASSED**: proceed to step 5 (Slack approval gate) or auto-pilot deliver
4. **On EXHAUSTED**: do NOT send. Notify the operator via iMessage. Halt this newsletter cycle.

**Auto-pilot constraint**: E2E MUST run even when Slack approval is skipped (Sunday 6 AM MT auto-send).
A failing E2E blocks auto-pilot and triggers escalation to the operator — auto-pilot does NOT bypass this gate.

## Approval Gate (before deliver)

1. Post full draft to Slack #lumina-bot: subject line options, preview text, full body, segment count
2. Wait for the operator's explicit response: [Approve] / [Edit] / [Cancel]
3. On [Edit]: apply feedback, re-run gate, re-run E2E (step 4.5), repost for approval
4. On [Cancel]: archive draft to `memory/drafts/cancelled/`, skip this issue; emit rejection to Paperclip:
   ```bash
   python3 scripts/paperclip-event.py approval newsletter-YYYY-MM-DD gate --rejected --approver austin
   ```
5. If no response within 2 hours before scheduled send window: skip this week, notify the operator
6. On [Approve]: emit approval to Paperclip (audit log only — Slack is authoritative):
   ```bash
   python3 scripts/paperclip-event.py approval newsletter-YYYY-MM-DD gate --approved --approver austin
   ```

## Auto-Pilot Mode (no-reply fallback)

When the operator does not reply to the Friday trend brief by Sunday 6 AM MT:
1. The brief sub-skill reads the latest trend brief at `memory/logs/trend-briefs/YYYY-MM-DD.md` without the operator's annotations
2. The draft sub-skill auto-selects the top 1-2 Content Opportunities from the trend brief as the Teaching angle and opening hook
3. The gate sub-skill runs all quality checks as normal — auto-pilot does NOT skip brand gate
4. The approval gate is SKIPPED — proceed directly to deliver
5. The deliver sub-skill sends with a note in the send log: `approval_mode: auto-pilot (no the operator reply by cutoff)`
6. Post to Slack after send: "Sunday Service sent in auto-pilot mode — [subject line]. the operator did not reply to Friday's trend brief by 6 AM MT cutoff."

Auto-pilot constraints:
- ONLY applies to Sunday Service newsletter type. All other types (Integration Dispatch, Science Brief, Community Letter, Threshold Letter) always require manual approval.
- CTA defaults to "Book a Connection Call" pointing to `/book` in auto-pilot mode (no campaign-specific CTA without the operator's input)
- Any trend with a "Caution" flag is excluded from auto-pilot content selection — only High Signal or Mixed trends without caution flags may be used
- If ALL top trends have caution flags: skip auto-pilot, notify the operator that no safe auto-content was available

## Adding a New Newsletter Type

1. Define: name, schedule, audience, purpose, persona, template name
2. Write the section-by-section template with word count targets in `newsletter/sub-skills/draft`
3. Register the `templateName` for `templates/email/render.ts` and create the React Email template via `email-design-system` skill
4. Set the idempotency key pattern: `[type]/YYYY-MM-DD`
5. Add the type to the Newsletter Type Registry table above
6. All 8 sub-skills apply unchanged — only draft section structure varies by type

## Error Handling

- Content brief finds no events: use pure-reflection format (Section 1 expanded 200-250 words; omit Section 3)
- Gate fails: list all flags; do not proceed to Slack approval until resolved
- Subscriber list empty: notify the operator; do not attempt send
- Slack approval times out: skip this issue; notify the operator
- Resend batch fails mid-send: log delivery IDs of successful sends; notify the operator; do not retry without instruction
