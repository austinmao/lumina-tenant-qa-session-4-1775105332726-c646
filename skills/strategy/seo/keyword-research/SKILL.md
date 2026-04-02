---
name: keyword-research
description: "Research keywords, analyze search intent, and identify content opportunities"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /keyword-research
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Keyword Research

Conduct keyword research, analyze search intent, and produce evidence-based artifacts -- keyword maps, opportunity analyses, and search behavior reports -- that inform content strategy, site architecture, and SEO optimization.

## When to Use

- Researching keywords for a new page, site section, or content initiative
- Analyzing search intent for existing or planned content
- Identifying content gaps and opportunity areas based on search demand
- Providing keyword targets for the Copywriter and URL structure guidance for site architecture

## Context Loading

Before any research work:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/brand-guide.md` for audience context and positioning
3. Read `<brand_root>/messaging.md` and `<brand_root>/content-system.md` for keyword context and content patterns
4. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Research Deliverables

### 1. Keyword Table
Present as a structured table:

| Keyword | Search Volume | Difficulty | Intent Type | Recommended Page | Priority |
|---|---|---|---|---|---|
| [keyword] | [volume] | [difficulty] | [informational/navigational/transactional/commercial] | [page] | [high/medium/low] |

### 2. Intent Analysis
For each keyword cluster, analyze:
- **Search intent** -- what the searcher is trying to accomplish
- **Content format** -- what type of content satisfies this intent (guide, comparison, tool, list, etc.)
- **SERP features** -- what rich results appear (featured snippets, FAQs, videos, People Also Ask)
- **Competitive landscape** -- who currently ranks and with what content type

### 3. Content Gap Analysis
Identify search demand not currently served by existing site content:
- Keywords with volume but no matching page
- Keywords where competitors rank but the site does not
- Keywords aligned with brand positioning but missing from content strategy

Prioritize gaps by: search volume, intent alignment with business goals, and competitive difficulty.

### 4. Audience Search Behavior
When available from analytics:
- How users find the site (query data)
- What users search for on-site
- Landing page performance by organic search
- Search journey patterns (what do they search before and after)

## Research Principles

- Ground every recommendation in data: search volume, keyword difficulty, current rankings, or documented industry patterns. Never recommend keywords based on intuition alone.
- Treat SEO as a constraint that improves user experience, not a trick. Every keyword recommendation must serve both search engines and human visitors.
- State confidence levels: High = multiple data sources, Medium = single source, Low = informed hypothesis.
- Provide input to multiple downstream consumers: site architecture (URL taxonomy), copywriter (keyword targets and meta copy), and QA (SEO compliance checks).

## URL Taxonomy Input

When providing URL structure recommendations:
- Human-readable paths that include target keywords naturally
- Hierarchical structure reflecting content relationships
- Stable URLs that do not need to change as content evolves
- Redirect recommendations for any URL changes

## Cannibalization Detection

Check for pages competing for the same keywords:
- Identify overlapping keyword targets
- Recommend consolidation or differentiation
- Flag pages that are splitting ranking authority

## Output Format

- Keyword research: table format as shown above
- URL taxonomy: hierarchical list with rationale for each level
- Content gaps: prioritized list with search volume, recommended content type, and competitive difficulty
- When detecting cannibalization or SEO risk: state the issue, affected pages, impact, and recommended fix. Severity first.
- Direct, data-driven. No SEO jargon without definition.

## Boundaries

- Never write primary page copy or marketing content. Provide keyword targets and structure recommendations.
- Never modify page designs, wireframes, or production code. Advise; other agents implement.
- Never fabricate search volume data, ranking positions, or competitive metrics. If data is unavailable, state the gap and recommend the data source.

## State Tracking

- `keywordTargets` -- keyed by page slug: primary keyword, secondary keywords, search volume, last updated
- `contentGaps` -- array of unserved search demand with priority and recommended content type
- `cannibalizationRisks` -- pages competing for the same keywords with recommended resolution
