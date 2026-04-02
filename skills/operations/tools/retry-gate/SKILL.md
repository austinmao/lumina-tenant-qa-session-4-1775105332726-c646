---
name: retry-gate
description: "Bounded retry with failure classification for any workflow step"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /retry-gate
metadata:
  openclaw:
    emoji: "🔁"
    requires:
      bins:
        - python3
---

# Retry Gate Skill

## Overview

General-purpose bounded retry skill. Wraps any workflow step with configurable max attempts, failure classification into 7 types, per-class routing to fixer agents, and escalation to the operator on exhaustion. State is persisted to disk as Markdown with YAML frontmatter (`memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md`), providing a full audit trail.

Use for any step where a failure should route to a fixer, retry, and only escalate after exhaustion.

## Invocation Interface

Parameters passed by the calling skill:

```yaml
retry-gate:
  operation: <string>           # Required. The exec command or skill to retry.
  workflow: <string>            # Required. Workflow identifier (used in state file naming).
  step: <string>                # Required. Step identifier (used in state file naming).
  max_attempts: <integer>       # Optional. Overrides config/org.yaml retry_gate.max_attempts.
  cooldown_seconds: <integer>   # Optional. Overrides config/org.yaml retry_gate.cooldown_seconds.
  escalation_channel: <string>  # Optional. Overrides config/org.yaml retry_gate.escalation_channel.
  escalation_target: <string>   # Optional. Overrides config/org.yaml retry_gate.escalation_target.
  routing:                      # Required. Maps failure classes to fixer agents.
    content: <agent-name>       # Agent to route content failures to.
    engineering: <agent-name>   # Agent to route engineering failures to.
    validation: <agent-name>    # Optional. Agent to route validation failures to.
    data: <agent-name>          # Optional. Agent to route data failures to.
```

## Retry Gate Protocol

### Step 1 — Resolve Configuration

Read `config/org.yaml` to get global defaults. Apply workflow-level overrides if provided in the invocation:

| Parameter | Source (priority order) |
|---|---|
| max_attempts | invocation override → `retry_gate.max_attempts` in config → 3 |
| cooldown_seconds | invocation override → `retry_gate.cooldown_seconds` in config → 0 |
| escalation_channel | invocation override → `retry_gate.escalation_channel` in config → imessage |
| escalation_target | invocation override → `retry_gate.escalation_target` in config → austin |

### Step 2 — Check for Existing State File

Determine state file path: `memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md`
(Use today's date — `YYYY-MM-DD` in local timezone.)

Run `read_state.py`:
```bash
python3 skills/retry-gate/scripts/read_state.py \
  --workflow <workflow> \
  --step <step>
```

- If `exists: false`: This is the first invocation. Generate a `run_id` (uuid4) for this session. Proceed to Step 3.
- If `status: PASSED` or `status: EXHAUSTED`: State is terminal. Return the existing result. Do not re-execute.
- If `status: IN_PROGRESS`: Resume from where it left off. Use the existing `run_id` from the state file.

### Step 3 — Execute the Operation

Run the operation specified in `operation`. This is typically:
- A Python script invocation: `python3 skills/qa/email-e2e/scripts/run_e2e.py ...`
- An exec command: `exec false`
- Any shell command the calling skill provides

Capture stdout (result data) and exit code:
- Exit 0 → operation passed. Proceed to Step 4a (PASS path).
- Exit 1 → operation failed. Parse stdout for failure classification. Proceed to Step 4b (FAIL path).
- Exit 2 or unhandled error → classify as `engineering`. Proceed to Step 4b (FAIL path).

### Step 4a — PASS Path

Write state file with status PASSED and this attempt's result:
```bash
python3 skills/retry-gate/scripts/write_state.py \
  --workflow <workflow> \
  --step <step> \
  --run-id <run_id> \
  --max-attempts <max_attempts> \
  --cooldown-seconds <cooldown_seconds> \
  --escalation-channel <escalation_channel> \
  --escalation-target <escalation_target> \
  --attempt-result PASS \
  --status PASSED
```

Return:
```yaml
result: PASSED
run_id: <uuid4>
attempts: <n>
state_file: memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md
```

Proceed with the calling workflow.

### Step 4b — FAIL Path

**Classify failures**: Parse the operation's stdout. Failures output by the operation use `failure_class` fields per the email-e2e assertion contract, or the calling skill provides failure classification in the routing map. If no classification is available, default to `engineering`.

**Failure class behavior**:

| Class | Retryable | Backoff | Route To | Escalation |
|---|---|---|---|---|
| content | yes | none | routing.content agent | on exhaust |
| engineering | yes | none | routing.engineering agent | on exhaust |
| validation | yes | none | routing.validation agent | on exhaust |
| data | yes | none | routing.data agent | on exhaust |
| infrastructure | yes | cooldown × attempt_n | (no routing) | on exhaust |
| external | yes | cooldown × attempt_n | (no routing) | on exhaust |
| permissions | NO | N/A | (no routing) | IMMEDIATE |

**Permissions failure**: Escalate immediately to the operator via the escalation channel. Do NOT retry. Write state with status EXHAUSTED and return.

**For all other failure classes**:

1. Write updated state file with this attempt's result:
```bash
python3 skills/retry-gate/scripts/write_state.py \
  --workflow <workflow> \
  --step <step> \
  --run-id <run_id> \
  --max-attempts <max_attempts> \
  --cooldown-seconds <cooldown_seconds> \
  --escalation-channel <escalation_channel> \
  --escalation-target <escalation_target> \
  --attempt-result FAIL \
  --failures '[{"class": "<class>", "detail": "<detail>", "routed_to": "<agent>"}]' \
  --attempt-number <n> \
  --status IN_PROGRESS
```

2. **Check attempt count**: If attempt_n >= max_attempts, skip routing and go to Step 5 (Exhaust).

3. **Route to fixer agent**: Send to the agent specified in `routing.<class>`. Message format:
   > "Retry gate: attempt <n>/<max> failed for `<workflow>/<step>`.
   > Failure: [<class>] <detail>
   > Please fix and reply when ready. The retry will execute on your confirmation."

4. **Apply cooldown** (if infrastructure or external class): Wait `cooldown_seconds × attempt_n` seconds before Step 5.

5. **Wait for fixer confirmation** before proceeding to next attempt.

6. **Record remediation note**: Ask fixer agent what was fixed. Pass as `--remediation` to next `write_state.py` call.

7. **Return to Step 3** for the next attempt.

### Step 5 — Exhaustion

All attempts consumed. Write final state:
```bash
python3 skills/retry-gate/scripts/write_state.py \
  --workflow <workflow> \
  --step <step> \
  --run-id <run_id> \
  --max-attempts <max_attempts> \
  --cooldown-seconds <cooldown_seconds> \
  --escalation-channel <escalation_channel> \
  --escalation-target <escalation_target> \
  --attempt-result FAIL \
  --failures '<failures_json>' \
  --attempt-number <n> \
  --status EXHAUSTED
```

**Escalate to the operator** via the configured escalation channel:
> "Retry gate exhausted: `<workflow>/<step>` failed after <max_attempts> attempts.
> Final failure: [<class>] <detail>
> State file: memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md
> Action required."

Return:
```yaml
result: EXHAUSTED
run_id: <uuid4>
attempts: <max_attempts>
state_file: memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md
failures: <list of failures from final attempt>
```

Do NOT proceed with the calling workflow. The calling workflow must halt until the operator intervenes.

## State File Lifecycle

```
(created) → IN_PROGRESS
IN_PROGRESS → PASSED       (operation succeeds on any attempt)
IN_PROGRESS → EXHAUSTED    (attempts >= max_attempts, all failed)
```

State files are written atomically (temp file + `os.replace()`) to prevent corruption from interrupted writes.

## Retention

State files are cleaned up by `cleanup_retention.py` (run via coordinator heartbeat):
- PASSED files: deleted after `retention_days` days (default: 30)
- EXHAUSTED files: deleted after `retention_exhausted_days` days if `retention_keep_exhausted: true` (default: 90)

## Return Contract

```yaml
# PASSED
result: PASSED
run_id: <uuid4>
attempts: <integer>
state_file: <path>

# EXHAUSTED
result: EXHAUSTED
run_id: <uuid4>
attempts: <integer>
state_file: <path>
failures: <list>
```

## Error Handling

- If `config/org.yaml` is unreadable: use hardcoded defaults (max_attempts: 3, cooldown: 0, escalation: imessage → austin)
- If `write_state.py` fails (disk full, permissions): notify the operator immediately; do not silently swallow
- If routing agent is unavailable: log to state file body; proceed to next attempt anyway; escalate on exhaust
