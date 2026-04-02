---
name: competitor-seo
description: "Analyze competing pages to identify keyword overlap and cannibalization issues"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /competitor-seo
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: []
      env: []
---

# Competitor SEO Analysis

Analyze multiple provided pages to identify keyword overlap, potential cannibalization issues, and competitive differentiation opportunities. Use when reviewing similar content across a site, comparing against competitor pages, or planning content differentiation strategy.

## When to Use

- Reviewing similar content pages for keyword cannibalization
- Comparing page targeting against competitors
- Planning content differentiation strategy
- Auditing internal content overlap after migration or growth

## Cannibalization Detection

### Overlap Types

**Title/Meta Overlap:**
- Similar page titles targeting the same primary keyword
- Duplicate or near-duplicate meta descriptions
- Same target keyword across multiple pages

**Content Overlap:**
- Similar topic coverage and content depth
- Duplicate sections or paragraphs
- Same search intent served by multiple pages

**Structural Issues:**
- Identical heading patterns across pages
- Similar content depth and word counts
- Overlapping topical focus without differentiation

## Prevention Strategy

1. **Clear keyword mapping** — one primary keyword per page
2. **Distinct search intent** — each page serves a different user need
3. **Unique angles** — different perspectives or depth levels
4. **Differentiated metadata** — unique titles and descriptions
5. **Strategic consolidation** — merge pages when appropriate

## Analysis Approach

1. Analyze keywords across all provided pages
2. Identify topic and keyword overlap percentage
3. Compare search intent targets for each page
4. Assess content similarity and differentiation
5. Find opportunities for unique positioning
6. Suggest consolidation where pages compete

## Output

**Cannibalization Report:**

```
Conflict: [Keyword]
Competing Pages:
- Page A: [URL] — Primary keyword, current focus
- Page B: [URL] — Overlapping keyword, similar intent

Resolution Strategy:
- Consolidate into single authoritative page, OR
- Differentiate with unique angles and distinct intent, OR
- Implement canonical from weaker to stronger page
- Adjust internal linking to signal primary page
```

**Deliverables:**
- Keyword overlap matrix
- Competing pages inventory with severity ranking
- Search intent analysis per page
- Resolution priority list (critical, high, medium, low)
- Consolidation recommendations with redirect mapping
- Internal linking cleanup plan
- Prevention framework for future content planning
