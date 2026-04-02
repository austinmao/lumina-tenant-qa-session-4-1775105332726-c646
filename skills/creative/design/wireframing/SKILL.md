---
name: wireframing
description: "Create structural wireframes, user flows, and interaction pattern specs for pages and components"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /wireframing
metadata:
  openclaw:
    emoji: "📐"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Wireframing

Create structural wireframes, user flows, and interaction pattern specifications. Wireframes define layout structure without visual styling -- they bridge information architecture with visual design. This skill produces UX artifacts only, not visual design or code.

## When to Use

- Creating layout wireframes for new pages or components before visual design
- Defining user flows (step-by-step task completion paths)
- Specifying interaction patterns (hover, focus, error, loading, empty states)
- Bridging the structural blueprint with visual design

## Context Loading

Before producing any wireframe:
1. Read `memory/site-context.yaml` to determine the active site. If it does not exist, prompt: "No active site set. Run `/site <name>` first."
2. Read `<brand_root>/brand-guide.md` for audience and positioning context
3. Read the blueprint at the path specified in `site-context.website.blueprint` for page specifications and sitemap

## Core Artifact Types

### 1. Wireframes
Grayscale structural layouts that define:
- Content block placement and hierarchy
- Navigation patterns and wayfinding
- CTA placement and prominence
- Content zones and their relative importance
- Responsive breakpoint behavior (always start mobile-first)

**Format**: ASCII by default. For complex components, break into labeled sub-wireframes.

### 2. User Flows
Step-by-step task completion paths:
- Numbered step sequences
- Decision points clearly marked
- Error and edge case paths
- Entry and exit points

### 3. Interaction Specs
State definitions for every interactive component:

| Component | Default | Hover | Focus | Active | Disabled | Error | Loading |
|---|---|---|---|---|---|---|---|
| [component] | [state] | [state] | [state] | [state] | [state] | [state] | [state] |

## Design Principles

- Design for the user's task, not for visual impact. Every wireframe element has a purpose tied to a user goal.
- Design mobile-first. Wireframes always start at the smallest breakpoint and expand. No desktop-only patterns that collapse poorly on mobile.
- Follow WCAG AA interaction patterns from the start: logical tab order, clear focus indicators, touch targets minimum 44x44px, no interaction requiring hover-only discovery.
- Every flow eliminates unnecessary steps. If a step does not serve the user's goal, remove it.

## Output Format

- Lead with page name and purpose, then the wireframe, then interaction states, then responsive breakpoint notes
- User flows: numbered step sequences with decision points marked
- When discovering a UX gap: state the gap, propose a solution grounded in user personas, and ask before proceeding
- One wireframe per message unless alternatives are requested

## Boundaries

- Never produce visual design (color, typography, imagery). Wireframes are grayscale structural layouts.
- Never write production code.
- Never hand off wireframes without explicit approval. The approval gate is non-negotiable.
- Never invent page structures that contradict the blueprint. If the spec is insufficient, flag it and request clarification.

## State Tracking

- `wireframes` -- keyed by page slug: page name, status (`draft` | `review` | `approved` | `handed-off`), approval date
- `userFlows` -- keyed by flow slug: task, steps count, status
- `interactionSpecs` -- keyed by component slug: states documented, status
- `openGaps` -- UX decisions awaiting input or clarification
