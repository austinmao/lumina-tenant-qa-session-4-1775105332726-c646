---
name: meta-optimization
description: "Create optimized meta titles, descriptions, and URL suggestions for search"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /meta-optimization
metadata:
  openclaw:
    emoji: "🏷️"
    requires:
      bins: []
      env: []
---

# Meta Optimization

Create optimized meta titles, descriptions, and URL suggestions based on character limits and best practices. Generate compelling, keyword-rich metadata with multiple variations for A/B testing. Use when creating metadata for new content or optimizing existing page metadata.

## When to Use

- Writing meta titles and descriptions for new pages
- Optimizing existing metadata for better click-through rates
- Creating URL slugs for new content
- Generating A/B test variations for metadata

## Optimization Rules

### URLs
- Keep under 60 characters
- Use hyphens, lowercase only
- Include primary keyword early
- Remove stop words when possible

### Title Tags
- 50-60 characters (pixel width varies)
- Primary keyword in first 30 characters
- Include emotional triggers/power words
- Add numbers or year for freshness signals
- Brand placement strategy: end for awareness, beginning for branded queries

### Meta Descriptions
- 150-160 characters optimal
- Include primary and secondary keywords
- Use action verbs and benefit-focused language
- Add compelling CTAs
- Special characters for visual distinction when appropriate

## Approach

1. Analyze provided content and target keywords
2. Extract key benefits and unique selling propositions
3. Calculate character limits for each element
4. Create 3-5 variations per element
5. Optimize for both mobile and desktop display
6. Balance keyword placement with compelling copy

## Output

**Meta Package for each page:**

```
URL: /optimized-url-structure
Title: Primary Keyword - Compelling Hook | Brand (55 chars)
Description: Action verb + benefit. Include keyword naturally. Clear CTA. (155 chars)
```

**Additional deliverables:**
- Character count validation for each variation
- A/B test variations (3 minimum per element)
- Power word suggestions for emotional triggers
- Schema markup recommendations for enhanced SERP features
- Platform-specific meta component code (Next.js, Astro)

Focus on psychological triggers and user benefits. Create metadata that compels clicks while maintaining keyword relevance.
