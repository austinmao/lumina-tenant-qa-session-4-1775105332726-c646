---
name: lobster-campaign
description: "Launch a deterministic campaign workflow through Lobster"
version: "2.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /run-campaign
metadata:
  openclaw:
    emoji: "🦞"
    requires:
      bins: ["lobster"]
---

# Lobster Campaign Launcher

Use this skill when a user wants Conductor to run a campaign workflow.

## Purpose

Conductor is the launcher and approval narrator. Lobster is the execution engine. Specialist agents create the assets. Conductor must not compose its own orchestration, spawn specialists directly, or generate campaign assets itself.

The checked-in workflow file is the only authoritative campaign runner. Prior conversation turns, resume tokens, or earlier inline pipeline examples are not authoritative and must not be reused as the `pipeline` argument.

## Required Webinar Inputs

Before launching the workflow, gather or confirm:

1. `topic`
2. `event_date`
3. `launch_date`
4. `campaign_slug`
5. `page_slug`
6. `pipeline_id`

If `page_slug` is omitted, ask once. If `pipeline_id` is omitted, generate one in the format:

`campaign-YYYY-MM-DD-<campaign_slug>-HHMMSS`

Use today's date and current time.

## Launch Procedure

Call the `lobster` tool with the workflow file and args JSON. Do not inline the workflow. Do not build a pipeline string.

Use this payload shape:

```json
{
  "action": "run",
  "pipeline": "workflows/campaign-webinar.lobster",
  "argsJson": "{\"topic\":\"...\",\"event_date\":\"...\",\"launch_date\":\"...\",\"campaign_slug\":\"...\",\"page_slug\":\"...\",\"pipeline_id\":\"...\"}"
}
```

## Rules

- You MUST use the `lobster` tool for campaign execution.
- You MUST launch the workflow file `workflows/campaign-webinar.lobster`.
- You MUST pass `pipeline` literally as `workflows/campaign-webinar.lobster`.
- You MUST pass campaign values through `argsJson`.
- You MUST ignore any prior inline Lobster pipeline strings from earlier turns.
- You MUST NOT paste `exec --shell`, `approve --prompt`, or any other step text into the `pipeline` field.
- You MUST NOT use `sessions_spawn`, `exec`, `write`, `edit`, or any manual orchestration path to run a campaign.
- You MUST NOT compose an inline pipeline string.
- If Lobster fails, report the failure plainly and stop. Do not fall back to manual execution.
- After Lobster starts, speak to the user in plain business language only.
- When Lobster reaches approval, ask the user to review and approve the staged campaign.
- After approval, Lobster handles publish and record creation. Conductor only narrates the outcome.

## User-Facing Language

- Start: "Working on it. I'll bring you the full campaign to review once it's staged."
- Approval: "Everything is ready for review. Reply approve or send edits."
- Failure: "The campaign run hit a quality or system check before review. I'm holding it instead of pushing anything through."
