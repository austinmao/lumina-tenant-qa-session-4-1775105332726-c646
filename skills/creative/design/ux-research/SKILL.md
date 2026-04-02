---
name: ux-research
description: "Conduct user research and produce personas, journey maps, and evidence-based insight reports"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /ux-research
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# UX Research

Conduct user research, analyze site analytics, and produce evidence-based artifacts -- personas, journey maps, and insight reports -- that inform architecture and design decisions.

## When to Use

- Creating user personas from audience data and brand research
- Building journey maps with touchpoints, emotions, and opportunity areas
- Producing evidence reports with findings and confidence levels
- Informing information architecture and design with validated user understanding

## Context Loading

Before any research work:
1. Read `memory/site-context.yaml` to determine the active site and its analytics property. If it does not exist, prompt: "No active site set. Run `/site <name>` first."
2. Read `<brand_root>/brand-guide.md` for audience context

## Core Artifact Types

### 1. User Personas
Structured profiles grounded in evidence:
- **Name** -- archetype label (not a real person)
- **Role archetype** -- the persona's relationship to the product/service
- **Goals** -- what they are trying to achieve
- **Frustrations** -- current pain points and blockers
- **Key behaviors** -- observable patterns in how they research, decide, and act
- **Preferred channels** -- where and how they engage

### 2. Journey Maps
Stage-based analysis of the user experience:

| Stage | User Action | Touchpoint | Emotion | Opportunity |
|---|---|---|---|---|
| [stage] | [action] | [touchpoint] | [emotion] | [opportunity] |

### 3. Evidence Reports
Structured findings with:
- **Finding** -- the specific insight
- **Evidence source** -- where the data came from
- **Confidence level** -- High (multiple data sources corroborate), Medium (single source or small sample), Low (informed hypothesis needing validation)
- **Downstream impact** -- what this means for architecture, design, or content decisions
- **Recommendation** -- specific action to take based on the finding

## Research Principles

- Ground every finding in evidence: analytics data, user research, or documented brand audience profiles. Never fabricate user quotes, personas, or behavioral data.
- Always state confidence levels on findings.
- If data is unavailable, state the gap and recommend how to collect it. Never fill gaps with speculation presented as fact.

## Output Format

- When delivering research: lead with the key finding, then the evidence, then the confidence level, then the implication for downstream work
- Personas: structured profiles with all fields filled
- Journey maps: stage-based table format
- When identifying a data gap: state what is missing, why it matters, and the specific data collection method recommended
- Direct, evidence-first. No speculation presented as fact.

## Boundaries

- Never fabricate research data, user quotes, or analytics numbers
- Never produce design artifacts, wireframes, or code. Output is research documents only.
- Never finalize personas or journey maps without user review. These artifacts shape the entire downstream pipeline.

## State Tracking

- `personas` -- keyed by persona slug: name, archetype, status (`draft` | `validated`), last updated
- `journeyMaps` -- keyed by journey slug: stages, status, associated persona
- `researchFindings` -- array of findings with evidence source, confidence level, and downstream impact
