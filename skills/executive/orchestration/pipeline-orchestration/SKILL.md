---
name: pipeline-orchestration
description: "Chain multi-step pipelines with pass-output-as patterns for campaign and build orchestration"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /pipeline-orchestration
metadata:
  openclaw:
    emoji: "🔗"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Pipeline Orchestration Skill

Chain multiple skills or agent tasks into a multi-step pipeline where each step's output feeds as input to the next. Supports linear chains, fan-out/fan-in patterns, conditional branching, and error gates. Use for campaign build pipelines, website build orchestration, or any multi-agent workflow requiring sequential or parallel coordination.

## Usage

```
/pipeline-orchestration <pipeline-definition>
```

Example:

```
/pipeline-orchestration
  step1: /copywriting "Write welcome email for retreat launch"
  step2: /email-design-system --input {{step1.output}}
  step3: /campaign-tdd --input {{step2.output}}
```

---

## Pipeline Definition Format

Define pipelines as ordered steps with explicit dependencies:

```yaml
pipeline: campaign-launch
steps:
  - id: brief
    invoke: /campaign-strategy "Q2 retreat launch"
    output: memory/pipelines/{{pipeline}}/brief.md

  - id: copy
    invoke: /copywriting --brief {{brief.output}}
    depends_on: [brief]
    output: memory/pipelines/{{pipeline}}/copy.md

  - id: html
    invoke: /react-email-templates --copy {{copy.output}}
    depends_on: [copy]
    output: memory/pipelines/{{pipeline}}/template.html

  - id: tdd
    invoke: /campaign-tdd {{html.output}}
    depends_on: [html]
    output: memory/pipelines/{{pipeline}}/tdd-report.md
    gate: true  # Pipeline stops if this step fails
```

---

## Pass-Output-As Patterns

### Linear Chain
Each step receives the previous step's output artifact path:
```
step1 → output → step2 → output → step3
```

### Fan-Out
One step's output is consumed by multiple parallel steps:
```
brief → [copy_email, copy_sms, copy_landing_page]
```
All fan-out steps run in parallel via the agent-squad sidecar when available.

### Fan-In
Multiple step outputs are collected and passed to a single step:
```
[copy_email, copy_sms, copy_landing_page] → review_gate
```
The review step receives all artifact paths as a list.

### Conditional Branch
Steps can have conditions based on previous step outputs:
```
- id: send
  invoke: /resend-send --template {{html.output}}
  depends_on: [tdd]
  condition: "{{tdd.result}} == pass"
```

---

## Dependency Resolution

Before execution, validate the dependency graph:

1. **Topological sort** — order steps by dependencies; verify a valid execution order exists
2. **Cycle detection** — if the graph contains a cycle, report "Circular dependency detected: <cycle path>" and refuse to execute
3. **Missing dependencies** — if a step references a `depends_on` ID that does not exist, report the error and stop
4. **Orphan detection** — warn (but do not block) if a step has no dependents and is not the terminal step

---

## Execution

1. **Initialize pipeline state** — create `memory/pipelines/<pipeline-name>/state.yaml` with all step IDs, statuses (pending), and timestamps
2. **Execute steps in topological order** — respect `depends_on` constraints; parallelize independent steps
3. **After each step**:
   - Update state.yaml with step status (running, completed, failed, skipped)
   - Verify output artifact exists at declared path
   - If step has `gate: true` and failed, halt the pipeline
4. **On pipeline completion** — write summary to `memory/pipelines/<pipeline-name>/summary.md`

---

## Gate Steps

Steps marked with `gate: true` are quality gates:

- If the gate step's output indicates failure (e.g., TDD failures, QA score below threshold), the pipeline halts
- Downstream steps are marked as `skipped` in state.yaml
- The gate failure reason is recorded in the summary
- Gates cannot be bypassed without explicit operator override

---

## Resume Support

If a pipeline is interrupted mid-execution:

- Read state.yaml to determine which steps completed and which are pending
- Resume from the first pending step
- Do not re-execute completed steps unless `--force-rerun` is specified

---

## Output Format

Pipeline summary at `memory/pipelines/<pipeline-name>/summary.md`:

```
# Pipeline: <pipeline-name>
Started: <timestamp>
Completed: <timestamp>
Status: completed | failed_at_gate | interrupted

## Steps
| Step | Status | Duration | Output |
|---|---|---|---|
| brief | completed | 12s | memory/pipelines/.../brief.md |
| copy | completed | 45s | memory/pipelines/.../copy.md |
| html | completed | 30s | memory/pipelines/.../template.html |
| tdd | failed | 20s | memory/pipelines/.../tdd-report.md |

## Gate Failures
- Step: tdd — Reason: 3 test failures detected

## Artifacts
- memory/pipelines/<pipeline-name>/brief.md
- memory/pipelines/<pipeline-name>/copy.md
- memory/pipelines/<pipeline-name>/template.html
- memory/pipelines/<pipeline-name>/tdd-report.md
```

---

## Error Handling

- If a non-gate step fails: log the failure, mark step as failed, continue with remaining steps that do not depend on it
- If a gate step fails: halt pipeline, mark downstream as skipped
- If circular dependency detected: report the cycle and refuse to execute
- If an output artifact is missing after step completion: retry once, then mark as failed

## Issue Routing

Pipeline orchestration issues are reported to the **CMO** (executive, `agents/executive/cmo`) for campaign pipelines, or **Construct** (website orchestrator, `agents/website/orchestrator`) for build pipelines.
