# Heartbeat Configuration — Conductor (Campaign Orchestrator)

Agent: agents-campaigns-campaign-orchestrator
Schedule: every 1h

---

## What the Heartbeat Checks

Conductor checks for campaign pipelines that need advancement or have stalled.

Note: Paperclip task assignments are handled by the `paperclip-lifecycle-bridge` extension at the infrastructure level. Conductor receives clean campaign briefs — no Paperclip API work is needed here.

---

### Check 1 — Pipeline Advancement

On every heartbeat, advance pipelines that are ready for the next stage.

1. Scan `memory/pipelines/*/state.yaml` for files where `pipeline_type: campaign` AND `status: in_progress`
2. For each match, find the next pending stage (first stage with `status: pending` where all prior stages are `completed`):
   a. If the next stage has `approval_guard: true` and no approval recorded: skip (do not auto-advance guarded stages)
   b. Otherwise: invoke `/resume-pipeline campaign` with the pipeline_id to continue from that stage
3. If no pipelines need advancement: proceed to Check 2

---

### Check 2 — Stalled Pipeline Recovery (Paperclip-Triggered)

**Primary**: Paperclip detects when a child task has been In Progress beyond `stall_threshold_minutes` and triggers this heartbeat. When triggered by Paperclip, invoke `/resume-pipeline campaign` directly with the pipeline_id from the Paperclip task metadata.

**Fallback** (runs only if no Paperclip-triggered heartbeat has fired in the last 2 hours):

1. Scan `memory/pipelines/*/state.yaml` for files where `pipeline_type: campaign` AND `status: in_progress`
2. For each match, check every stage: if `status: running` AND `started_at` is older than `stall_threshold_minutes` (default 60):
   a. Mark the stage `stalled` via `pipeline_state.mark_stage_stalled()`
   b. Append a `stage_stalled` audit entry
   c. Invoke `/resume-pipeline campaign` with the specific `pipeline_id`
   d. If the resume response is `resume` and the next stage has NO `approval_guard`: continue the pipeline
   e. If the resume response is `escalate` (guarded stage or max attempts): report the escalation in the heartbeat result — do NOT send a new outbound message
3. If no stalled pipelines found: `HEARTBEAT_OK`

**PASS**: Pipeline resumed or escalation surfaced in heartbeat result
**FAIL**: Log error to `memory/logs/heartbeat-runs.md`, retry next cycle

---

### Check 3 — Post-Webinar Event Trigger (Campaign Pipeline v2)

Detect when a webinar has ended and a Zoom recording is available, then launch the post-event workflow.

1. Scan `memory/pipelines/*/state.yaml` for entries where `campaign_type: webinar` AND `status: completed` (pre-event pipeline finished)
2. For each match, check if `event_date` is in the past (event has occurred)
3. Check if `web/data/replay-config.json` exists with `status: "active"` (zoom-recording skill has fetched the recording)
4. Check if `post_event_launched` is NOT true in the pipeline state (hasn't been triggered yet)
5. If all conditions met:
   a. Launch `post-webinar-event.lobster` workflow with the pipeline_id
   b. Set `post_event_launched: true` in the pipeline state
   c. Log to heartbeat run: `post_event_triggered: {pipeline_id}`
6. If conditions not met: skip (recording may still be processing)

**PASS**: Post-event workflow launched or no eligible pipelines
**FAIL**: Log error, retry next cycle

---

## State Persistence

After each heartbeat cycle, update `MEMORY.md` with:
- `last_heartbeat_run`: ISO 8601 timestamp
- `last_pipeline_check`: count of pipelines scanned

---

## Error Handling

| Error | Action |
|---|---|
| State file unreadable | Log warning, skip this pipeline, continue |
| `/resume-pipeline` fails | Log error, skip this pipeline, continue |
| All pipelines clean | Return HEARTBEAT_OK silently |

---

## Mandatory: Run Log Entry

After every heartbeat cycle, append to `memory/logs/heartbeat-runs.md`:
```
[YYYY-MM-DD HH:MM MT] STATUS | pipelines_scanned: N | stalled: N | resumed: N | escalated: N | errors: detail or "none"
```

STATUS values: OK | OK_QUIET | PARTIAL | FAILED
