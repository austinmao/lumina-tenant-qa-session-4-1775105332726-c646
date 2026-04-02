---
name: brand-strategy
description: "Develop brand strategy, positioning, and identity direction"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /brand-strategy
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Brand Strategy

Develop and refine brand strategy, positioning, and identity direction. This skill covers strategic brand decisions — not visual design (use `brand-identity-design`) or copy review (use `brand-review-gate`).

## When to Use

- Defining or refining brand positioning for a new site or sub-brand
- Developing brand messaging hierarchy and value propositions
- Evaluating competitive positioning and differentiation
- Informing upstream strategy that guides all downstream creative and content work

## Core Approach

### Be Resourceful Before Strategic

Before proposing any brand strategy, read existing brand context:
- `memory/site-context.yaml` to determine the active site
- `<brand_root>/brand-guide.md` for current positioning
- `<brand_root>/tokens/design-system.yaml` for visual identity context

Ground every recommendation in existing brand assets and documented audience data. Never invent audience segments or market positions without evidence.

### Strategy Over Tactics

Brand strategy is about positioning decisions that persist across campaigns, channels, and seasons. Focus on:

- **Brand positioning**: How the brand is perceived relative to alternatives
- **Audience understanding**: Who the brand serves and what they need
- **Messaging hierarchy**: Which messages lead, which support, which are tertiary
- **Differentiation**: What makes this brand the only logical choice for its audience
- **Brand architecture**: How multiple offerings or sub-brands relate to the master brand

### Multi-Brand Architecture

When managing multiple brands or sub-brands, apply the 80/20 rule: 80% master brand cohesion, at most 20% accent energy from the sibling. Flag any strategy recommendation that would violate this balance.

## Deliverable Format

- **Strategy briefs**: Lead with the strategic recommendation, then the evidence, then the implications for downstream work
- **Positioning statements**: Use the format: For [audience], [brand] is the [category] that [differentiator] because [reason to believe]
- **Messaging hierarchies**: Numbered priority list with primary message, supporting messages, and proof points
- **Competitive analysis**: Table format with competitors, their positioning, and the strategic gap the brand occupies

## Boundaries

- Brand strategy recommendations are proposals only. All strategic decisions route through user approval before becoming operational.
- Never fabricate market data, competitor analysis, or audience statistics. If data is unavailable, state the gap and recommend how to collect it.
- Never make brand strategy decisions that contradict the existing brand guide without explicit approval.

## Dependencies

- `brand-standards` — current brand voice and messaging rules
- `brand-review-gate` — validates that strategic outputs comply with brand standards

## Note on Source Agent

This skill was absorbed from the `marketing/brand` agent. The original agent used a generic SOUL.md template without specialized brand strategy knowledge. This skill defines the brand strategy capability as specified in the Lumina OS hierarchy design.
