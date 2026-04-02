---
name: trend-score
description: "Cluster, deduplicate, and rank trend findings by signal quality"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /trend-score
metadata:
  openclaw:
    emoji: "📈"
    requires:
      env: []
      bins: []
---

# Trend Score Sub-Skill

## Overview

Step 2 of the trend intelligence pipeline. Reads raw scan findings, clusters related
items into themes, scores each theme using `references/scoring-rubric.md`, and produces
a ranked list.

## Steps

### 1. Read Raw Scan

Load `memory/logs/trend-scans/YYYY-MM-DD-raw.md` (today's date).

### 2. Cluster into Themes

Merge findings about the same underlying topic into a single theme. A "theme" is one
trend, not one headline. Group by shared subject matter, not by source type.

### 3. Score Each Theme

Apply the 4 weighted dimensions from `references/scoring-rubric.md`:

| Dimension | Weight |
|---|---|
| Momentum | 30% |
| Breadth | 25% |
| Significance | 25% |
| the organization relevance | 20% |

Score each dimension on a 1-5 scale. Compute weighted total.

### 4. Assign Signal Labels

Label each theme: **High Signal** / **Mixed** / **Hype-Driven** / **Polarizing**

Use definitions from scoring rubric.

### 5. Apply the organization Positioning Guardrails

Check each theme against the mandatory flags table in `references/scoring-rubric.md`.
Add caution flags where any topic type matches:
- Therapeutic/clinical claims: "Caution: framing risk"
- Peyote / indigenous medicine: "Caution: stewardship sensitivity"
- Safety incidents: "Caution: sensitive"
- Legal gray areas: "Caution: legal framing"
- Competitor controversies: "Caution: positioning"

### 6. Rank Themes

Sort by weighted score, highest first.

### 7. Identify Early Signals

Flag 2-5 themes that did not make the top 5-10 but show emerging momentum worth watching.

### 8. Save Scored Results

Write to `memory/logs/trend-scans/YYYY-MM-DD-scored.md`:

```
# Trend Scores — YYYY-MM-DD

## Ranked Themes

### 1. [Theme title] — [Signal label] — the organization relevance: [high/medium/low]
- Momentum: [score/5] | Breadth: [score/5] | Significance: [score/5] | Relevance: [score/5]
- Weighted: [total]
- Caution flags: [none / list]
- Sources: [URLs]
- Why it matters: [1 sentence]
---

## Watchlist
- [Early signal 1]: [1 sentence]
- [Early signal 2]: [1 sentence]
```

### 9. Confirm and Proceed

Output: "Scoring complete. [N] themes ranked. [M] caution flags applied. Proceeding to brief."

Then invoke `trend-intelligence/sub-skills/brief`.

## Error Handling

- Raw scan file not found: stop, notify the operator
- Fewer than 3 themes after clustering: note "Low-activity week" and proceed — a short briefing is better than none
