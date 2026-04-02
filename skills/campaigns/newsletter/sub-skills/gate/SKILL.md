---
name: newsletter-gate
description: "Use when running the brand gate and quality checks on a newsletter draft"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /newsletter-gate
metadata:
  openclaw:
    emoji: "🚦"
    requires:
      env: []
      bins: []
---

# Newsletter Gate Sub-Skill

## Overview

Step 3 of the newsletter pipeline. Runs all brand, quality, and compliance checks
on the draft before Slack approval is requested. Gate must PASS before proceeding.
A single unresolved FLAG blocks the send.

## MANDATORY: Tool Call Enforcement

Before starting work:
1. `read` the handoff contract at the path provided in the task (look for `handoff-contract: <path>`)
2. Apply all `binding` fields — the gate checks listed in `binding.gate_checks` are mandatory

Execution:
3. `read` the draft file at the contract's `artifact_path` (the draft to be gated)
4. `sessions_spawn` to `agents-marketing-brand` with the draft content AND the contract path:
   "handoff-contract: memory/pipelines/newsletter-YYYY-MM-DD/gate-handoff.yaml

   Run the newsletter brand gate on the draft below. For each check in binding.gate_checks, report PASS or FAIL with details. Return your results as structured text. Draft content: [full draft text]"
5. After brand guardian returns its results, YOU (the orchestrator) MUST `write` the gate results back to the draft file. The brand guardian returns results as text — it does NOT write to the file. You MUST:
   a. Prepend `gate_status: PASSED` (or FAILED) as the first line of the draft file
   b. Append a `## Brand Gate` section with checked boxes for each gate check:
      ```
      ## Brand Gate
      - [x] kill list — passed
      - [x] extended kill list — passed
      - [x] link audit — passed
      - [x] Wise Alchemist checklist — passed
      - [x] Seth Godin filter — passed
      - [x] post-click consistency — passed
      - [x] voice-first test — passed
      ```
   c. Use the `write` tool to save the updated draft file. This step is NOT optional.

After writing gate results:
6. Run contract assertion verification:
   `exec: python3 -c "from compiler.engine.contract_assertions import run_assertions; import json; r = run_assertions('<contract_path>', '.'); print(json.dumps({'passed': r.passed, 'failures': [{'type': f.assertion_type, 'detail': f.detail} for f in r.failures]}))"`
   If verification fails, STOP and notify the operator.
7. `message` to Slack #lumina-bot with the gate result and draft summary for approval

## Brand Kill List Check

Scan the full draft body for each prohibited word or phrase. If found, insert
`[FLAG: kill-list — "[matched text]"]` inline at the exact location.

Primary kill list:
- Sacred, Miracle, Therapy, Spirit Guide, Breakthrough, Transformational

Extended newsletter kill list (additional phrases prohibited in newsletters):
- "This week's newsletter"
- "I hope this finds you well"
- "As we enter [season]"
- "In today's busy world"
- "Now more than ever"
- "Join me on this journey"
- "Deep dive"
- "Game-changer"
- "I wanted to reach out"
- "Unpacking"
- "In conclusion"
- "Stay tuned for more"
- "Thank you for being part of our community"
- "We are excited to share"

## Link Audit

1. Extract every `href` value from the draft body
2. Exclude from audit: unsubscribe link, physical address anchor, footer social icon links
3. All remaining links must resolve to the SAME destination URL

If 2 or more different destination URLs are found in the body:
`[FLAG: link-audit — multiple destinations found: [URL1], [URL2]]`

Do not attempt to resolve this flag automatically. Stop and list the conflicting URLs for the operator.

## Wise Alchemist Checklist

Review the draft body against these 5 criteria. Check any that are met. At least 2 of 5 must be checked for gate to pass on this criterion.

- [ ] the operator is positioned as a fellow pilgrim, not as a guru or authority above the reader
- [ ] A bridge between science/mechanism and spirit/meaning is present
- [ ] The reader's interior world is named with specificity — not category words (not "stress", "anxiety", "burnout" as bare nouns)
- [ ] The reader is positioned as already on the journey, not as broken and needing fixing
- [ ] Communal "we" is used for shared human experience, not as company voice

If fewer than 2 are checked: `[FLAG: wise-alchemist — [count] of 5 criteria met, minimum 2 required]`

## Seth Godin Filter

All 5 criteria must be met for gate to pass on this criterion.

- [ ] The newsletter's main idea is statable in one sentence (can you?)
- [ ] No sentence in the Teaching section exceeds 25 words
- [ ] No hedging language present: "perhaps", "might be", "in some cases", "it could be argued", "some would say"
- [ ] The Teaching section ends with an observation or question, not a recommendation or directive
- [ ] The newsletter could stand alone as a blog post if the CTA section were removed

For each unchecked item: `[FLAG: godin-filter — "[criterion description]"]`

## Post-Click Consistency Check

1. Extract the subject line (recommended variant from draft)
2. Extract the CTA destination URL
3. Evaluate: does the promise implied by the subject line match what a reader would find at the destination?

If mismatch detected: `[FLAG: post-click — subject promise "[subject]" does not align with destination "[URL]"]`

## Voice-First Test

Read the draft aloud mentally, sentence by sentence through Section 1 and Section 2.
Flag any sentence where:
- Register shifts abruptly (e.g., warm/personal → corporate/formal)
- Sentence rhythm breaks (e.g., too many clauses in sequence without a short sentence)
- Structure feels mechanical or templated (e.g., "Firstly... Secondly... In conclusion...")

Mark: `[FLAG: voice-first — "[flagged sentence]" — reason: [register shift | rhythm break | mechanical structure]]`

Maximum 3 voice-first flags before requiring full redraft. If >3: stop, notify the operator for redraft.

## Humanizer Step

After all checks above: invoke the `humanizer` skill on the full draft body.

Apply humanizer output. Update the draft file with the humanized version.

If `humanizer` skill is not available in this workspace: note "Humanizer not available — manual review required" and continue.

## Gate Result

After all checks:

If any `[FLAG: ...]` remains unresolved in the draft:
- List all flags with their location and type
- Output: "GATE FAILED — [N] flags unresolved. Resolve all flags before Slack approval."
- Do NOT proceed to Slack approval or deliver sub-skill

If zero flags remain:
- Update the Brand Gate checklist in the draft file (check all boxes)
- Write `gate_status: PASSED` at the top of the draft file
- Output: "GATE PASSED. Sending draft to the operator for approval in #lumina-bot."
- Proceed to the Slack approval step in the parent `newsletter` skill

## Error Handling

- Draft file not found: stop, notify the operator
- Humanizer skill unavailable: note in gate result, continue — do not block on missing optional skill
- Gate fails with >3 voice-first flags: stop, notify the operator for full redraft — do not iterate further
- File write fails after humanizer: notify the operator, provide humanized draft inline in Slack instead
