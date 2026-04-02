---
name: newsletter-subject-line
description: "Use when generating newsletter subject line variants and preview text"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /newsletter-subject-line
metadata:
  openclaw:
    emoji: "✉️"
    requires:
      env: []
      bins: []
---

# Newsletter Subject Line Sub-Skill

## Overview

Generates exactly 5 subject line variants — one per formula — plus recommended
preview text. Called by the draft sub-skill after body copy is complete. Do not
call this sub-skill before the draft body exists; subject lines must emerge from
the actual content, not be written speculatively.

## The 5 Formulas

Write one subject line per formula. Do not reuse a formula.

### Formula 1 — Curiosity Gap

Structure: [Specific thing] + [withheld completion]
Test: the reader cannot predict the answer from the subject line alone.
The gap must be genuine — not manufactured vagueness.

Example: "What I got wrong about stillness"

### Formula 2 — Pattern Interrupt

Contradicts a common belief, drops the reader mid-scene, or uses unexpected
specificity that signals "this is different from other emails."

Examples: "Sunday, 6:43am" / "This is not a wellness email" / "Three things I stopped doing"

### Formula 3 — Benefit / Transformation (oblique)

Specific outcome stated without superlatives, hype words, or exaggeration.
Must be believable to a skeptical reader. Oblique means the benefit is implied,
not announced.

Example: "What happens when you stop optimizing"

### Formula 4 — Personal / Conversational

Reads like a message from the operator directly — not from a brand.
First-person or informal register. Could appear in a personal inbox without feeling out of place.

Examples: "honest question" / "something I've been sitting with" / "I almost didn't send this"

### Formula 5 — Question

Already exists in the reader's interior world, OR plants a productive uncertainty
they want to resolve. Never rhetorical (a question the reader can immediately dismiss).

Example: "Have you ever noticed how the body knows first?"

## Character Rules

- Optimal range: 28-40 characters (renders fully on iPhone SE without truncation)
- Hard maximum: 50 characters
- Count all characters including spaces
- Emoji rendering: treat each emoji as 2 characters (Gmail rendering standard)
- Count character total after applying the emoji rule

## Emoji Rules

- 0 or 1 emoji per subject line — never more
- Approved emoji set: 🌿 ✨ 💛 🔆
- Prohibited: 🔥 🚨 💥 and any emoji that signals urgency, alarm, or hype
- Placement: front of subject for F2/F4 (adds personality signal); end of subject for F3 (completes the thought's emotional arc)
- F1 and F5: emoji optional; use only if it genuinely adds to the reading experience

## Subject Line Kill List

Flag and discard any subject line containing:
- ALL CAPS words (except approved acronyms)
- The word "FREE" anywhere
- "Limited time" or "Don't miss"
- "Exciting", "Opportunity", "Urgent", "Act now"
- Exclamation marks
- The word "Newsletter" (readers know it's a newsletter)
- The event name as the opener (e.g., "Awaken Retreat — March 2026")
- A colon mid-subject
- An em-dash mid-subject
- Generic openers: "This week,", "In this issue,", "Join us,"

If a formula draft hits the kill list: discard and rewrite that variant.

## Preview Text Rules

- Length: 85-100 characters (including spaces)
- Must introduce NEW information not present in the subject line
- Subject line + preview text together = compound curiosity (two incomplete thoughts that
  pull the reader forward; neither one alone tells the full story)
- Compound curiosity test: read subject and preview together. If preview was predictable
  from the subject, rewrite the preview.
- Never start with: "This week,", "In this issue,", "Join us,", "You're invited,", "Read more"
- Never complete the subject line's thought — the preview extends or pivots, never resolves
- End with an open loop: a phrase, clause, or image the reader must open the email to close

## Output Format

```
Subject Lines:
1. [F1 — Curiosity Gap] — [char count]
2. [F2 — Pattern Interrupt] — [char count]
3. [F3 — Benefit Oblique] — [char count]
4. [F4 — Personal/Conversational] — [char count]
5. [F5 — Question] — [char count]

Recommended: [number] — [one sentence: why this variant wins for this issue]

Preview Text (pairs with recommended):
[85-100 chars — new information, open loop]
```

## Error Handling

- Draft body not available when called: stop, notify caller — cannot generate subject lines without body content
- All 5 formula drafts hit kill list on first attempt: notify the operator, provide raw variants with kill-list items marked for manual resolution
- Character count cannot be reduced below 50 while preserving meaning: notify the operator with the overlength variant and reason
