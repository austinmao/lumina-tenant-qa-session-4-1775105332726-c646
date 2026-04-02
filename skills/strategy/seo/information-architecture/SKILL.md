---
name: information-architecture
description: "Translate business goals into website strategic briefs and requirements"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /information-architecture
metadata:
  openclaw:
    emoji: "🧭"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Information Architecture

Translate business goals into website requirements, producing strategic briefs that ground every downstream decision -- from research to architecture to design. This skill works at the very beginning of the website lifecycle (Discovery phase), defining what the site needs to achieve before any building begins.

## When to Use

- Starting a new website initiative and defining the strategic brief
- Translating business objectives into specific website requirements
- Defining target audience segments and success metrics for a site
- Providing the strategic foundation that informs all downstream work

## Context Loading

Before producing any strategic artifact:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/brand-guide.md` for positioning, audience, and brand voice
3. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Strategic Brief Structure

Every website initiative requires a strategic brief before any downstream work begins. The brief includes:

### 1. Business Objectives
- What the website (or section) must achieve
- How it connects to broader business goals
- Priority ranking of objectives

### 2. Target Audience Segments
- Who the site serves (grounded in brand guide audience data)
- Segment characteristics and needs
- Journey stage at point of site entry
- No audience segments invented without evidence

### 3. Success Metrics
- Measurable success criteria for every objective
- Baseline values (if available) for comparison
- Measurement methodology and tools
- Reporting cadence

### 4. Competitive Positioning
- How this site differentiates from alternatives
- Competitive advantages to emphasize
- Positioning gaps to address

### 5. Content Priorities
- What content types are most important
- Content hierarchy and emphasis
- Content gaps that need to be filled
- Content that can be repurposed or retired

## Output Format

- Lead with the business objective, then audience segments, then success metrics, then content priorities
- Strategic briefs are written to `docs/website/<site>/` as Markdown files with clear section headings
- When identifying a gap in brand positioning or audience understanding: state the gap, explain why it matters for the website, and recommend a specific research question
- Direct, no filler. One brief per initiative unless alternatives are requested

## Strategy as Testable Outcomes

Every objective in a brief has a measurable success criterion. Reject vague aspirations:

- Bad: "Improve the website experience"
- Good: "Increase application-to-enrollment conversion rate from 12% to 20% by reducing the application form to 3 steps"

- Bad: "Build trust with visitors"
- Good: "Achieve 60-second average time-to-first-CTA-click on the landing page by leading with social proof above the fold"

## Boundaries

- Never produce design artifacts, wireframes, or code. Output is strategic briefs and requirements documents only.
- Never finalize a strategic brief without user review and approval. The brief shapes everything downstream.
- Never invent market data, competitor analysis, or audience statistics. If data is lacking, state the gap and recommend how to collect it.

## Dependencies

- `keyword-research` -- search demand data to inform content priorities
- `site-architecture` -- the brief feeds into sitemap and page specification creation
- `ux-research` -- the brief becomes the research brief for user study design

## State Tracking

- `strategicBriefs` -- keyed by initiative slug: title, site, status (`draft` | `review` | `approved`), approval date
- `openQuestions` -- strategic questions awaiting input or research
- `audienceInsights` -- validated audience segments and positioning decisions with rationale
