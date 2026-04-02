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

## Copy Deck Format (for the `run-pages-v2` stage)

The `run-pages-v2` Lobster stage calls `scripts/build-page-specs-from-copy-deck.py` which parses the copy deck markdown. Quill's copy deck output MUST follow this exact format or the pipeline will fail at the pages stage.

### Page Structure

Each page starts with a `### Page Name` heading (H3):

```
### Registration Page
### Thank You
### Replay
```

The page slug is derived from the page name (lowercased, spaces → hyphens). The slug must match the event slug stored in the database (e.g., `have-a-good-trip-v2`).

### Fields

Standard fields use bold label + colon + value on the same line:

```markdown
**Title:** Have a Good Trip: The Science of Safer, Smarter Psychedelic Experiences
**Subtitle:** A free 60-minute live webinar for curious, thoughtful adults
**CTA:** Reserve Your Free Spot
**CTA URL:** https://live.example.org/have-a-good-trip-v2
```

### Body / Long-Form Text

Body sections use one of these two formats (both are accepted):

**Format A — bold label with colon, then content on following lines:**
```markdown
**Body:**
Full paragraph text goes here. Can span
multiple lines. Ends when the next **Field:** is encountered.
```

**Format B — bold label without colon (standalone on its own line), then content:**
```markdown
**Body**
Full paragraph text goes here.
```

Both formats are parsed identically. Use Format A for consistency.

### Bullet Lists

Bullet or numbered list items are collected as arrays:

```markdown
**What You'll Learn:**
- The neuroscience of why set and setting determine outcomes
- How to assess a provider's safety protocols
- What integration actually looks like in practice
```

### Named Sections

Section blocks use `**Section: Name**` to start a named content block:

```markdown
**Section: Social Proof**
Content for this section goes here.
```

Or inner `### Heading` inside a page block triggers a named section:

```markdown
### Credibility / Trust Bar
650+ people facilitated · 96% most transformative experience · TedX Boulder
```

Recognized section heading labels: `credibility / trust bar`, `social proof`, `what you'll learn`, `what you'll leave with`, `included resources`, `next steps`, `who this is for`, `footer microcopy`, `next actions`, `key takeaways`, `what happens on the call`, `reassurance copy`.

### Required Pages for Webinar Campaigns

The pipeline expects these exact page names (case-insensitive):
- `Registration Page` (or `Registration`)
- `Thank You`
- `Replay` (optional — only if replay URL is known)

Missing required pages cause a `ValueError` at the pages stage and halt the pipeline.

### Copy Deck Validation Rule for Quill

When Quill generates copy deck output for a campaign, it MUST:
1. Use `### Page Name` H3 headings for each page
2. Use `**Field:** value` for all single-line fields
3. Use `**Body:**` followed by body paragraphs (not `**Body** value` on one line)
4. NOT use H1 or H2 headings inside page blocks — these break section parsing
5. Include at minimum: Title, Subtitle, Body, CTA, CTA URL for each page

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
