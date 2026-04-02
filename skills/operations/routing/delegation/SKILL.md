---
name: delegation
description: "Delegate a task to a specialist sub-agent using sessions_spawn with the registered local agent roster."
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /delegation
metadata:
  openclaw:
    emoji: "🔀"
---

# Sub-Agent Delegation

Use `sessions_spawn` to delegate a full task to a specialist agent. The result is announced back to the requesting channel when the sub-agent finishes.

## Critical runtime rule

**NEVER use `runtime: "acp"` for local the organization agents.** ACP is exclusively for external harnesses (codex, claude-code, gemini). Using it for local agents causes "Failed to spawn agent command" and will always fail.

**Correct call for local agents:**
```
sessions_spawn(
  agentId: "<agent-id>",   // from the table below -- no runtime field
  task: "<full task description>"
)
```

The `runtime` parameter defaults to `subagent` -- omit it entirely for local agents.

## Registered local agents

| agentId | Role |
|---|---|
| `agents-marketing-brand` | the active brand copy in the operator's voice -- retreat descriptions, newsletter intros, landing page copy, social posts, testimonial arcs |
| `agents-marketing-copywriter` | Chain-of-Draft newsletter copy, email copy, subject lines, CTAs -- all brand-governed writing |
| `agents-marketing-campaign-orchestrator` | Multi-channel campaign orchestration -- newsletter pipeline, landing page + email + SMS staging |
| `agents-marketing-email` | Email sequences, SMS campaigns, direct-response copywriting, campaign strategy |
| `agents-scaffold-interviewer` | Multi-turn scaffold adoption interviews -- start with `sessions_spawn` in normal run mode, preserve the returned `childSessionKey`, then forward follow-up answers with `sessions_send` until the interview finalizes |
| `agents-sales-director` | Lumina in sales-director mode -- pipeline triggers, deal management, Attio CRM writes, enrollment sequences |
| `agents-sales-enrollment` | Enrollment conversations, application follow-up |
| `agents-sales-lead-nurture` | Lead nurture sequences |
| `agents-sales-pricing-yield` | Pricing, yield optimization, retreat capacity |
| `agents-sales-coach` | Sales coaching and sequencing guidance |
| `agents-programs-onboarding-intake` | Intake coordination for new participants |
| `agents-programs-onboarding-screening` | Application screening |
| `agents-programs-onboarding-medical` | Medical screening |
| `agents-programs-prep-participant` | Participant preparation before retreat |
| `agents-finance-payroll` | Payroll, invoices, reimbursements, and Gusto-related finance operations |
| `agents-frontend-designer` | Frontend design specification and visual system work |
| `agents-frontend-engineer` | Frontend implementation for approved web and email experiences |
| `agents-operations-knowledge-sync` | Google Drive and Chroma knowledge-base synchronization |
| `agents-corpus-transcript-curator` | Transcript ingestion, corpus organization, and Chroma sync |

## Contract-Aware Delegation Pattern

When delegating within a multi-agent pipeline (newsletter, campaign, website), use **handoff contracts** to enforce binding constraints and verify sub-agent output:

1. Write a handoff contract to `memory/pipelines/<pipeline>-YYYY-MM-DD/<stage>-handoff.yaml`
2. Copy the contract INTO the sub-agent's workspace before `sessions_spawn`:
   ```
   exec: mkdir -p <agent-workspace>/memory/pipelines/<pipeline-dir>/
   exec: cp memory/pipelines/<pipeline-dir>/<stage>-handoff.yaml <agent-workspace>/memory/pipelines/<pipeline-dir>/
   ```
3. Include the contract path in the task string: `handoff-contract: memory/pipelines/<pipeline-dir>/<stage>-handoff.yaml`
4. After the sub-agent completes, copy the artifact back: `exec: cp <agent-workspace>/<artifact_path> <artifact_path>`
5. Run contract assertion verification via `compiler/engine/contract_assertions.py`

The ContextEngine plugin (`plugins/context-inject/`) injects the SOUL.md and IDENTITY.md of the sub-agent automatically — no need to include these in the task string.

**For parallel delegation** (campaign Phase 2 independent assets): use the `coordinate` skill instead of direct `sessions_spawn`. The `coordinate` skill dispatches multiple agents concurrently via the Agent Squad sidecar at `localhost:18790` and falls back to serial execution if the sidecar is unavailable.

## When to delegate vs. use a skill directly

- **Delegate** when the task needs the specialist's full context, persona, and memory (e.g., brand copy that must carry the operator's voice, or a sales sequence requiring Lumina's sales persona).
- **Use a skill directly** when the task is a narrow, tool-level operation (e.g., send an email via Resend, look up a participant in Airtable).
- **For interactive scaffold interviews**, keep the parent conversation as the host surface while the specialist child session does the interview work. Spawn `agents-scaffold-interviewer` once in normal run mode, preserve the returned `childSessionKey`, and route short follow-up replies (`y`, `k`, `keep`, edits, finalize requests) back to that same child with `sessions_send` until the run is complete.
- Do not rely on `mode: "session"` or thread binding for this workflow. Some channels and direct sessions do not support subagent session threads. The portable pattern is: `sessions_spawn` -> save `childSessionKey` -> `sessions_send` on each follow-up turn.
- **Do not send a placeholder acknowledgement for interactive scaffold interviews after spawn.** Wait for the child's first completion event, then relay that question to the user as the next turn.
- **If an active scaffold child session already exists in the current conversation, treat the next user reply as interview input first.** Forward it with `sessions_send` before doing any other interpretation or routing.
- **For interactive scaffold interviews, the usual "sub-agent runs are non-blocking" rule is suspended.** This workflow is a relay conversation: wait for the child result, relay it, then keep relaying follow-up answers until the interviewer finalizes.

## After spawning

The sub-agent run is non-blocking for ordinary specialist tasks. Interactive scaffold interviews are the exception: wait for the child completion event, relay the returned question or result, and continue the baton until the interview ends. Do not poll.
