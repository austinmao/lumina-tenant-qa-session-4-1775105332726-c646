---
name: site-architecture
description: "Define sitemaps, content models, page specifications, and URL structures for website projects"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /site-architecture
metadata:
  openclaw:
    emoji: "🗺️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Site Architecture

Define sitemaps, content models, page specifications, and URL structures that organize a website into a coherent, navigable system. This skill produces the site blueprint -- the single source of truth for what gets built.

## When to Use

- Creating a sitemap for a new website or site section
- Defining page specifications (purpose, audience, content sections, CTAs, success metrics)
- Designing URL taxonomy and redirect maps
- Building content models for CMS-driven pages
- Transforming strategic briefs into a buildable site structure

## Context Loading

Before producing any architectural artifact:
1. Read `memory/site-context.yaml` to determine the active site. If it does not exist, prompt: "No active site set. Run `/site <name>` first."
2. Read `<brand_root>/brand-guide.md` for positioning and audience context
3. Read any existing strategic brief from `docs/website/<site>/`

## Core Deliverables

### 1. Sitemap
Hierarchical page inventory with:
- Page name and URL
- Parent-child relationships
- Priority level
- Content type (landing page, content page, blog post, form, etc.)

### 2. Page Specifications
Every page in the blueprint has a specification:
- **Purpose** -- what the page achieves
- **Target audience** -- who this page serves
- **Content sections** -- ordered list of content blocks
- **CTAs** -- primary and secondary calls to action
- **Success metric** -- how to measure if the page is working
- **SEO target** -- primary keyword and search intent (informed by keyword research)

No page exists without a reason traceable to the strategic brief.

### 3. Content Model
For CMS-driven pages:
- Field definitions (type, required/optional, validation)
- Content relationships (references between content types)
- Reusable content blocks

### 4. URL Taxonomy
Human-readable, SEO-friendly, and stable URL structures:
- Hierarchical structure reflecting content relationships
- Keyword-informed paths (incorporating SEO strategist input)
- No date-based URLs for evergreen content
- Consistent casing and separator conventions

### 5. Redirect Map
Every URL change requires a corresponding redirect entry:
- Old URL to new URL mapping
- Redirect type (301 permanent, 302 temporary)
- Reason for redirect
- Implementation status

## Output Format

- **Sitemap**: hierarchical list or table with page count at top
- **Page specs**: consistent template per page (page name, URL, purpose, audience, content sections, primary CTA, success metric)
- **URL taxonomy**: hierarchical list with rationale for each level
- **Redirect map**: table format (old URL, new URL, type, reason, status)
- When discovering a gap in the strategic brief: state the gap, explain how it blocks a specific architectural decision, and name who can resolve it

## Boundaries

- Never produce design artifacts, wireframes, or code. Output is structural documents.
- Never finalize the blueprint without user approval. The blueprint governs everything that gets built.
- Never create pages that lack a traceable connection to the strategic brief's objectives.

## Dependencies

- `keyword-research` -- SEO input on URL structure and content hierarchy
- `information-architecture` -- strategic site structure decisions
- `content-freshness` -- monitoring for stale content post-launch

## State Tracking

- `blueprints` -- keyed by site slug: path, page count, status (`draft` | `review` | `approved`), approval date
- `pageSpecs` -- keyed by page slug: URL, status (`outlined` | `spec-complete` | `approved`), assigned phase
- `redirectMap` -- array of old URL to new URL mappings with reason
