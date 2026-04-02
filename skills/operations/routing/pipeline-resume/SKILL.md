---
name: pipeline-resume
description: "Resume pipeline that was interrupted mid-execution"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /resume-pipeline
metadata:
  openclaw:
    emoji: "▶"
---

## Overview

Resume an interrupted multi-stage pipeline (`newsletter`, `campaign`, or `website`) from the last completed stage. Returns a structured response telling the caller what to do next — resume, complete, restart, or escalate.

## Steps

1. **Find** — Scan `memory/pipelines/*/state.yaml` for files matching the requested `pipeline_type` (or `pipeline_id` if given directly) with `status: in_progress` or `status: stalled`. If no match is found, return `{action: restart, reason: "no in-progress pipeline found"}`. If multiple matches exist, select the one with the most recent `updated_at` timestamp.

2. **Migrate check** — Inspect `schema_version` in the matched state file.
   - If `schema_version` is absent or less than 2, return `{action: restart, reason: "legacy state format"}` without modifying the file.
   - Proceed only when `schema_version` is 2 or higher.

3. **Validate completed** — For every stage with `status: completed` that has a `contract` path, re-run contract assertions against the stage's `artifact` via `compiler/engine/contract_assertions.py`:
   - If assertions pass: leave the stage as completed and continue.
   - If assertions fail (artifact missing or assertion failure): mark the stage `failed` with the assertion failure message in `error_detail`, write state, and treat the stage as the candidate for retry in step 5.

4. **Reset guards** — Call `reset_guards(state)` to set every key in `guards` to `false`. A session boundary has been crossed; all external-write approvals from the prior session are invalid.

5. **Find next** — Walk `stages` in order and locate the first stage that qualifies for execution:
   - `status: pending` — ready to run.
   - `status: failed` with `attempt < max_attempts_per_stage` — eligible for retry.
   - If no qualifying stage is found, go to step 9 (complete or escalate).

6. **Block guarded stages** — If the next stage has an `approval_guard` value and the corresponding guard in `guards` is `false`:
   - Append a `pipeline_escalated` audit entry with `actor: pipeline-resume` and `detail` indicating which guard is required.
   - Write state.
   - Return `{action: escalate, stage: <name>, reason: "approval required for <guard_name>"}`.

7. **Detect stall** — Before committing to resume, inspect all stages with `status: running`:
   - If `started_at` is older than `stall_threshold_minutes`, call `mark_stage_stalled(state, stage_name, actor="pipeline-resume")`.
   - After marking stalled, if that stage is the current candidate, re-evaluate from step 5 (stalled stages do not qualify as "next").
   - Write state after any stall marks.

8. **Increment attempt** — If the next stage has `status: failed`:
   - The `mark_stage_running` helper in `pipeline_state.py` will increment `attempt` automatically when called.

9. **Return** — Determine the response:
   - **All stages terminal (completed/skipped/failed)** — if any stage is `failed`, return `{action: escalate, reason: "pipeline failed: max attempts exceeded on <stage>"}`. Otherwise return `{action: complete}`.
   - **Next stage found and not guarded** — call `mark_stage_running(state, next_stage_name, actor="pipeline-resume")`, append a `stage_resumed` audit entry, write state, then return:
     ```
     {
       action: resume,
       stage: <next_stage_name>,
       agent: <next_stage_agent>,
       contract: <next_stage_contract>,
       prior_work: {<completed_stage_name>: <artifact_path>, ...}
     }
     ```

## Output

One of four structured responses:

| action | When | Required fields |
|---|---|---|
| `resume` | Next actionable stage found | `stage`, `agent`, `contract`, `prior_work` |
| `complete` | All stages in terminal status, none failed | — |
| `restart` | Legacy schema or no matching pipeline | `reason` |
| `escalate` | Guarded stage, max attempts exceeded, or pipeline failed | `reason` |

`prior_work` is a map of `stage_name → artifact_path` for every completed stage with an artifact. Callers use this to skip re-running completed work.

## Error Handling

- If `memory/pipelines/` does not exist or contains no state files: return `{action: restart, reason: "no pipeline state found"}`.
- If a state file cannot be parsed as YAML: log the error and skip that file; continue scanning remaining files.
- If `compiler/engine/contract_assertions.py` is unavailable: skip re-validation (step 3) and log a warning; do not fail the resume.
- If `pipeline_type` and `pipeline_id` are both omitted: return `{action: restart, reason: "pipeline_type or pipeline_id required"}`.
