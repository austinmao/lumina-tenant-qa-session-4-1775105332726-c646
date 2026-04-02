---
name: newsletter-draft
description: "Use when generating Chain-of-Draft newsletter copy from a content brief"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /newsletter-draft
metadata:
  openclaw:
    emoji: "✍️"
    requires:
      env: []
      bins: []
---

# Newsletter Draft Sub-Skill

## Overview

Step 2 of the newsletter pipeline. Reads the content brief and generates a
complete newsletter via mandatory Chain-of-Draft process. This is the highest-stakes
sub-skill — all copy quality decisions happen here. Do not skip any draft step.
The gate sub-skill is a backstop, not a license to draft carelessly: avoid the
primary and extended kill-list language in the first draft whenever possible.

## MANDATORY: Tool Call Enforcement

Before starting work:
1. `read` the handoff contract at the path provided in the task (look for `handoff-contract: <path>`)
2. Apply all `binding` fields from the contract — these override your SOUL.md preferences
3. Use your own judgment for `delegated` fields

Execution:
4. `read` the brief file referenced in `prior_work.content_brief`
5. `sessions_spawn` to `agents-marketing-copywriter` with the full brief content AND the contract path in the task:
   "handoff-contract: memory/pipelines/newsletter-YYYY-MM-DD/draft-handoff.yaml

   Generate Chain-of-Draft newsletter copy for Sunday Service. Brief content: [full brief text]"
6. After copywriter finishes, `read` the artifact at the contract's `artifact_path` to verify it was written

After completing work:
7. The ContextEngine plugin's `onSubagentEnded` hook automatically runs the contract's `verification` assertions
8. If verification fails, STOP and notify the operator with the specific failures

## MANDATORY: Chain-of-Draft — 4 Steps Before Writing Copy

Work through all 4 steps and output each result explicitly before writing any section.

---

### Step A — Persona Declaration

Default persona pairing: Seth Godin (philosophical precision) × Wise Alchemist (grounded warmth).

Override by avatar from brief:
- A1/A2 (executive, high-performer): apply Science Translator lens — lead with mechanism, not metaphor
- B1 (burnout, seeker): apply Storytelling Sage lens — open mid-scene, sensory detail, no frameworks

Output format:
> "Applying [Persona] × [Archetype]. Target avatar: [X]."

---

### Step B — Opening Hook (3 options)

Write exactly 3 opening sentences — nothing else, no paragraphs yet.

Rules for all 3:
- Must open in the reader's interior world (their experience, not the organization's, not the operator's)
- Cannot mention the organization, the operator, a retreat, or any product before sentence 3 of the full section
- Must create pattern interrupt: reader pauses because the sentence does not go where expected

Score each on: specificity (1-5), pattern interrupt potential (1-5), voice-first flow (1-5).

Select the highest-scoring option. If tied: prefer the most specific.

Output format:
> Option 1: "[sentence]" — S:[n] PI:[n] VF:[n]
> Option 2: "[sentence]" — S:[n] PI:[n] VF:[n]
> Option 3: "[sentence]" — S:[n] PI:[n] VF:[n]
> Selected: Option [n]. Rationale: [two sentences].

---

### Step C — Teaching Insight Test

State the single insight the Teaching section will deliver. One sentence only.

Then test it against two criteria:
1. Is this a Godin reframe (a fresh way of seeing something the reader already knows), NOT a summary of information?
2. Does it end with productive open-loop tension — something the reader wants to resolve?

If either test fails: restate the insight until both pass.

Before locking the teaching insight, check it against the primary kill list:
`Sacred`, `Miracle`, `Therapy`, `Spirit Guide`, `Breakthrough`, `Transformational`.
If any of those words appear, rewrite the insight before proceeding.

Output format:
> "Teaching insight: [one sentence]. Open loop: [one sentence]."

---

### Step D — CTA Alignment

Check `## CTA Direction` field in the content brief.

- Brief flags "Applied-stage" → use retreat-specific CTA copy and the specific retreat URL
- Brief flags "Alumni reactivation" → use alumni reunion CTA and upcoming alumni event URL
- No flag / "connection-call" → use "Book a Connection Call" → `/book`

Enforce the single-destination rule: ONE URL in the entire newsletter body (excluding footer
compliance links: unsubscribe, physical address, social icons). If brief suggests multiple
destinations: select the highest-priority one and note the others as discarded.

Output format:
> "CTA: [button text] → [URL]. No secondary URLs."

---

## Write the 5-Section Draft

Use the chain-of-draft outputs above. Do not deviate from word count ranges.

### Section 1 — Opening Reflection (80-140 words)

- First sentence: the selected hook from Step B
- V4 rhythm: comma-rich expansion in first 2-3 sentences → short declarative close (under 8 words)
- Do not mention the organization before the third sentence of this section
- Do not open with "I" as the first word
- Tone: fellow pilgrim, not guide

### Section 2 — Teaching (70-110 words)

- h2 heading with emoji prefix (pick one: 💡 🌿 🔆 — no hype emoji)
- Deliver the insight from Step C
- No sentence longer than 25 words
- No hedging language: delete "perhaps", "might be", "in some cases", "it could be argued"
- End with a Maté-register inquiry question — open, non-directive, ends with "?"
- Teaching must be self-contained: a reader who stops here should have received the full value

### Section 3 — What's Happening (50-75 words)

Only include if the brief contains at least one upcoming event. If no events: omit this section entirely.

- h2: "📅 What's Happening"
- 2-3 bullets maximum
- Each bullet: [Date] — [Event name] — [one sentence, max 15 words]
- Link event name to website slug from brief
- Do not include events more than 60 days out

### Section 4 — CTA (15-30 words)

- One sentence leading into the button — direct, not clever
- Apply Kennedy direct response principle: state what the reader gets, not what the button does
- Then: `[BUTTON: [CTA text] → [URL]]`
- No secondary links in this section

### Section 5 — Signature (fixed)

```
With love,
[Operator name]
```

No additions. No PS. No additional links.

---

## Subject Line Generation

After completing all 5 sections: invoke `newsletter/sub-skills/subject-line` to generate
5 subject line variants + recommended preview text. Append the output to the draft file.

---

## Inline Kill List Check

Before saving, scan the full draft for these prohibited words and phrases.
Mark any occurrence with `[FLAG: prohibited word — "[word]"]` inline.

Prohibited words: Sacred, Miracle, Therapy, Spirit Guide, Breakthrough, Transformational

Do not intentionally lean on the gate to catch these. Rewrite first, flag only if
you cannot preserve the intended meaning without the prohibited wording.

Do not resolve flags — leave them for the gate sub-skill. Do not suppress or rewrite flagged
content at this stage.

---

## Save Draft

Write to: `memory/drafts/YYYY-MM-DD-[newsletter-type].md`

```
# [Newsletter Type] — YYYY-MM-DD

## Chain-of-Draft Log
### Step A — Persona
[output]

### Step B — Hook Options
[output]

### Step C — Teaching Insight
[output]

### Step D — CTA
[output]

---

## Subject Lines
[output from subject-line sub-skill]

## Preview Text (pairs with recommended subject)
[output]

---

## Body

### SUNDAY SERVICE
[headline — under 40 chars]

[Section 1 — Opening Reflection]

---

### [emoji] [Teaching heading]
[Section 2 — Teaching]

---

### 📅 What's Happening
[Section 3 — or omit if no events]

---

[Section 4 — CTA sentence]
[BUTTON: [CTA text] → [URL]]

---

With love,
[Operator name]

---

## Brand Gate
- [ ] Kill list passed
- [ ] Extended kill list passed
- [ ] Link audit passed (single destination)
- [ ] Wise Alchemist checklist (2 of 5 required)
- [ ] Seth Godin filter (all required)
- [ ] Post-click consistency checked
- [ ] Voice-first test passed
- [ ] Humanizer run
```

After saving: "Draft saved to memory/drafts/YYYY-MM-DD-[type].md. Proceeding to gate."

Then invoke `newsletter/sub-skills/gate`.

## Error Handling

- Brief file not found: stop, notify the operator — do not draft without brief
- Brief contains no CTA direction field: default to "Book a Connection Call" → `/book`
- Chain-of-Draft step produces no valid output after 2 attempts: notify the operator, stop
- File write fails: notify the operator immediately, do not proceed to gate
