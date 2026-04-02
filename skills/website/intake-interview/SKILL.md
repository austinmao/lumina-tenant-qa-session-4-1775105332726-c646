---
name: intake-interview
description: "Run website intake interview to gather requirements before pipeline execution"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /intake-interview
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3"]
      env: []
      os: ["darwin", "linux"]
---

# Website Intake Interview

Run a structured multi-turn interview via the `clawinterview` gateway tool to gather operator requirements before starting a website build pipeline. This skill is the mandatory first step for every website build.

## When to Use

When you receive a website build request (homepage, landing page, full site build) — either directly from the operator or via a delegated Paperclip issue. You MUST complete the intake interview before invoking clawpipe.

## Steps

### 1. Start the interview

Invoke the `clawinterview` gateway tool with:

```json
{
  "action": "start",
  "pipeline_path": "pipelines/website/website-single-page-native.yaml",
  "pipeline_args": {
    "site_slug": "<tenant slug from issue context, e.g. acme-corp>",
    "page_slug": "<page slug from issue context, e.g. homepage>"
  }
}
```

Pre-fill `pipeline_args` with any values you can extract from the issue description or conversation context. The interview engine skips questions for pre-filled inputs.

The response is JSON:

```json
{
  "status": "awaiting_input",
  "run_id": "<uuid>",
  "turn": {
    "question": "<text>",
    "options": ["A", "B", "C"],
    "recommendation": "B"
  }
}
```

Save the `run_id` — you need it for every subsequent `respond` call.

### 2. Relay questions to the operator

Present the question from `turn.question` to the operator in their channel (Paperclip comment, iMessage, Telegram — whichever channel the conversation is on).

- Include the options if provided
- Include the recommendation if provided
- Wait for the operator's response

If you are running inside a Paperclip wake event: post the question as a comment on the current issue and wait for the operator to reply. The operator's reply will arrive as a new comment on the issue.

### 3. Advance the interview

When the operator responds, invoke `clawinterview` again:

```json
{
  "action": "respond",
  "run_id": "<run_id from step 1>",
  "response": "<operator's answer>"
}
```

The response is either:

**Another question** (`status: "awaiting_input"`):
- Go back to step 2 and relay the next question

**Interview complete** (`status: "complete"`):
- Extract the `brief` object from the response
- Proceed to pipeline execution (step 4)

### 4. Hand off to pipeline

Once the interview is complete and you have the brief, invoke the `clawpipe` gateway tool to start the build pipeline:

```json
{
  "action": "run",
  "pipeline_path": "pipelines/website/website-single-page-native.yaml"
}
```

The interview outputs are automatically available to the pipeline stages via the run state.

## Output

Report to the operator:
- Interview complete: N questions answered
- Brief compiled for: `<site_slug>/<page_slug>`
- Pipeline started: `<pipeline_id>`

## Error Handling

- If `clawinterview start` returns `status: "error"`: report the error to the operator and stop. Do not proceed to pipeline execution.
- If `clawinterview respond` returns `status: "error"`: report the error and ask the operator to rephrase their answer.
- If the operator says "skip" or "use defaults": pass "use recommendation" as the response — the interview engine applies its default recommendation.
- If the gateway tool is unavailable: report that the clawinterview plugin is not loaded and stop.

## Pipeline Config

- Pipeline: `pipelines/website/website-single-page-native.yaml`
- Interview contract: `pipelines/website/contracts/interview.yaml`
- Required inputs: `site_slug`, `page_slug`, `business_goals`, `target_audience`
- Optional inputs: `site_url`, `brand_guide_path`, `competitors`, `tone`, `cta_primary`
