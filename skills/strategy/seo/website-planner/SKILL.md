---
name: website-planner
description: "Plan the website / audit the site / generate sitemap / create page brief for [slug] / create full spec for [slug] / snapshot the blueprint"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /plan-website
metadata:
  openclaw:
    emoji: "🗺️"
    requires:
      bins: ["curl", "jq", "python3"]
      os: ["darwin"]
---

# Website Planner Skill

Orchestrates the full Blueprint workflow: site audit from 8 data sources, conversational sitemap ideation, layered page brief and full spec generation, blueprint snapshots, and redirect map production. All output written to `docs/website/blueprint.md` and `docs/website/audit/`.

## Trigger Phrases

- "plan the website"
- "audit the site"
- "generate sitemap"
- "create page brief for [slug]"
- "create full spec for [slug]"
- "snapshot the blueprint"
- `/plan-website [optional: path/to/export.xml]`

**Export file path** (if provided) is used for blog URL inventory during the audit. It is supplied as a trigger parameter and never hardcoded.

---

## State Detection

Before taking action, determine current state by reading `MEMORY.md` and `docs/website/blueprint.md`:

| State | Condition | Action |
|---|---|---|
| **No audit** | `audit_date` in blueprint frontmatter is empty | Run full site audit (Algorithm A) |
| **Audit done, no sitemap** | Audit exists, `sitemap: []` in blueprint | Propose sitemap (Algorithm B) |
| **Sitemap approved, missing briefs** | Pages in `proposed` status with no brief section | Generate briefs (Algorithm C) |
| **Brief approved, no full spec** | Pages in `brief-approved` with no spec section | Generate full spec on request (Algorithm D) |
| **Snapshot only** | Trigger was "snapshot the blueprint" | Run snapshot only (Algorithm E) |

---

## Algorithm A — Full Site Audit

**Trigger**: No existing audit, or explicit "audit the site" trigger.

### Step 1 — Crawl 8 data sources

Query each data source and collect findings:

1. **Google Analytics** (`google-analytics` skill): page-level traffic, bounce rate, session duration for all URLs in the past 90 days
2. **Senja** (`senja` skill): fetch all testimonials; note which pages are referenced
3. **Airtable retreats** (`airtable-retreats` skill): current retreat dates, capacity, waitlist status
4. **Chroma corpus** (`chroma` skill): query `austin_teachings` for frequently cited topics, teaching themes
5. **Campaign API** (`campaign-api` skill): list all campaigns; note which landing pages exist and their conversion data
6. **Brand standards** (`brand-standards` skill): load brand vocabulary — words to use and words to avoid; messaging hierarchy
7. **Compliance audit** (`compliance-audit` skill): load compliance rules; flag pages with policy-sensitive content
8. **Programmatic SEO** (`programmatic-seo` skill): keyword gap analysis; pages with SEO potential not yet built

### Step 2 — Parse Squarespace export (if path provided)

If an export file path was provided at trigger time:
- Invoke `blog-migration` skill's parse step (Step 1-3 only — no file writes yet)
- Extract all page URLs from `<item>` elements with `wp:post_type = page`
- Extract all blog post URLs from `<item>` elements with `wp:post_type = post`
- Build a complete URL inventory: pages list + blog posts list + attachment count

If no export path provided:
- Note in audit: "Squarespace export not provided — blog post count and exact page URLs estimated from GA4 data"

### Step 3 — Classify all pages

For each page found in the export or GA4 data, classify:

| Status | Criteria |
|---|---|
| `keep` | High traffic (>500 sessions/month) AND content is current AND brand-compliant |
| `update` | Has traffic but content is stale, outdated pricing, or has brand violations |
| `merge` | Low traffic (<100 sessions/month) AND content overlaps with another page |
| `cut` | No meaningful traffic AND content is redundant, outdated, or off-brand |

Flag each page with:
- `content_freshness`: `current` | `stale` | `outdated`
- `brand_violations`: list any messaging inconsistencies
- `gap_flag`: true if this page represents a topic that doesn't exist yet in the sitemap

### Step 4 — Write audit report

Write to `docs/website/audit/site-audit-YYYY-MM-DD.md` (immutable once written):

```markdown
# Site Audit — YYYY-MM-DD

## Summary
- Total pages audited: N
- Keep: N | Update: N | Merge: N | Cut: N
- Gaps identified: N
- Blog posts inventoried: N

## Data Sources
- Google Analytics: queried YYYY-MM-DD (90-day window)
- Senja: N testimonials fetched
- Airtable: N retreat dates retrieved
- Campaign API: N campaigns referenced
- Squarespace export: [path or "not provided"]

## Page Classification

| URL | Title | Status | Traffic/mo | Freshness | Brand Violations | Notes |
|---|---|---|---|---|---|---|

## Gap Analysis

Pages that should exist but don't:
| Recommended Slug | Purpose | Priority | Evidence |
|---|---|---|---|

## Blog Posts
- Total posts in export: N
- Recommended migration: all | selective (list)

## Competitive Analysis Observations
[Findings from chroma corpus research]

## Analytics Summary
[Top 10 pages by traffic, top exit pages, top landing pages]
```

### Step 5 — Snapshot blueprint

Update `docs/website/blueprint.md` frontmatter:
- `audit_date`: today's date (ISO)
- `updated`: today's date (ISO)
- `created`: today's date (ISO) if previously empty

Notify the operator via iMessage:
> "Blueprint: Audit complete. [N] pages classified (keep: N, update: N, merge: N, cut: N), [N] gaps found. Ready to ideate sitemap — reply 'generate sitemap' to proceed."

---

## Algorithm B — Sitemap Ideation

**Trigger**: Audit exists, sitemap is empty or "generate sitemap" trigger.

### Step 0 — Discovery gate (MANDATORY — do not skip)

Before proposing anything:

**1. Read the brand guide:**
`<brand_root>/brand-guide.md`

This file already answers: primary audience, emotional sequence, primary CTA, positioning,
differentiators, voice, and tone. Do NOT ask the operator about any of these — they are decided.

**2. Check whether a discovery brief exists:**
`docs/website/discovery-brief.md`

**If the brief does NOT exist** → invoke `website-discovery` skill.

The skill will:
- Auto-populate brand context from BRAND-GUIDE.md (no interview needed for those)
- Ask the operator only the four website-specific questions it cannot answer:
  1. Starting point: fresh IA or existing structure?
  2. Must-have pages
  3. Gap confirmation (from audit)
  4. URL/campaign/content constraints

Do not proceed to Step 1 until the brief is written and the operator confirms it.

**If the brief already exists** → read it, then confirm with the operator:
> "I have a discovery brief from [date]. Should I use it as-is, or update any answers first?"

**Never proceed to Step 1 without a confirmed discovery brief.**

---

### Step 1 — Propose sitemap tree

Build the proposed sitemap using **the discovery brief as the primary input**.
The audit is a content inventory and traffic reference — not the structural blueprint.

Design the IA around:
- The primary audience and their journey (from discovery brief)
- The primary CTA and conversion path (from discovery brief)
- The emotional experience (from discovery brief)
- Must-have pages (from discovery brief)
- Confirmed gaps (from discovery brief + audit)

Then cross-reference the audit to determine:
- Which existing pages map to nodes in the new IA (`keep` / `redesign` / `merge`)
- Which existing pages have no place in the new IA (`cut` → redirect map)
- Which nodes in the new IA need net-new content (`new`)

Organize into logical hierarchy driven by user journey, not by what currently exists.

### Step 2 — Present to the operator

Present the proposed sitemap as a hierarchical tree:

```
/ — Home
  /about — About the organization
  /journeys — Our Journeys
    /journeys/awaken — Awaken Retreat (redesign — maps to existing)
    /journeys/colorado — Psilocybin Retreats in Colorado (new — gap)
  /blog — Blog (migrated)
  /connect — Connect (redesign — replaces /start/*)
```

Each page includes:
- Slug (proposed)
- Purpose (1 sentence, grounded in discovery brief)
- Recommendation: `new` | `redesign` | `keep-as-is`
- Source: discovery gap | audit-keep | audit-update | audit-merge | audit-cut-repurposed

Request approval:
> "Proposed sitemap above — built around [primary audience] with [primary CTA] as the conversion goal. Reply 'approve sitemap' to advance all pages to brief stage, or 'revise [slug]: [notes]' for specific changes."

### Step 3 — On approval: write to blueprint.md

Update the Sitemap section in `docs/website/blueprint.md` with the approved structure. Set all pages to `proposed` status.

Update `MEMORY.md` Page Status Tracking table.

---

## Algorithm C — Page Brief Generation

**Trigger**: Sitemap approved, or "create page brief for [slug]" trigger.

For each page in `proposed` status (or the specified slug):

### Step 1 — Gather page data

Query relevant skills for this page:
- Traffic history (`google-analytics`)
- Relevant testimonials (`senja`)
- Relevant brand messaging (`brand-standards`)
- SEO opportunity (`programmatic-seo`)
- Existing campaign assets (`campaign-api`)

### Step 2 — Generate brief

```markdown
### /slug — Page Title

**Audience**: [Who is visiting this page and why]
**Purpose**: [What this page must accomplish]
**Key Sections**: [Ordered list of major content sections]
**Data Sources**: [Which skills/APIs will feed live data]
**Primary CTA**: [The one action we want visitors to take]
**Success Metric**: [How we'll know this page is working]
```

### Step 3 — Brand gate

Pass brief through `brand-standards` + `compliance-audit`. Revise if violations found.

### Step 4 — Present for approval

Present brief(s) and request approval:
> "Brief for /slug above. Reply 'approve brief /slug' or 'revise brief /slug: [notes]'."

On approval: update page status to `brief-approved` in blueprint.md and MEMORY.md.

---

## Algorithm D — Full Page Spec Generation

**Trigger**: "create full spec for [slug]" or page in `brief-approved` status with explicit the operator request.

For the specified page:

### Step 1 — Generate section-by-section spec

```markdown
### /slug — Full Spec

**Brief**: [Brief summary from brief-approved stage]

#### Section 1: [Section Name]
- **Component**: [Component type from the organization design system]
- **Photo Direction**: [Subject, mood, composition guidance]
- **Content Source**: [brand-ref.yaml field | senja testimonials | static | airtable-retreats]
- **Headline**: [Draft or placeholder with intent note]
- **Subheadline**: [Draft or placeholder]
- **CTA**: [Button label + destination]
- **Notes**: [Any special instructions for Canvas or Nova]

#### Section 2: ...
```

### Step 2 — Brand gate

Pass full spec through `brand-standards` + `compliance-audit`. Revise if violations found.

### Step 3 — Present for approval

On approval: update page status to `spec-complete` in blueprint.md and MEMORY.md.

---

## Algorithm E — Blueprint Snapshot

**Trigger**: "snapshot the blueprint" or after any status transition.

Read current state from MEMORY.md and update `docs/website/blueprint.md` frontmatter:
- `updated`: today's date (ISO)

Confirm:
> "Blueprint snapshot saved. Current state: [N] pages — [N] proposed, [N] brief-approved, [N] spec-complete, [N] handed-to-builder."

---

## Redirect Map Finalization

When all pages are at `spec-complete` or later:

1. Read all `cut` pages from audit report
2. Read all `merge` pages and their merge targets
3. Read all slug changes (old Squarespace slugs → new blueprint slugs)
4. Read blog post URL inventory from export

Generate redirect entries for all cases and write to `docs/website/blueprint.md` Redirect Map section.

Validation: every old URL from the Squarespace export must have a `new` target (even if it's the closest content match).

---

## Output Files

| File | When Written | Notes |
|---|---|---|
| `docs/website/blueprint.md` | Every algorithm | Sole writer (except the operator manual edits) |
| `docs/website/audit/site-audit-YYYY-MM-DD.md` | Algorithm A only | Immutable once written |
| `docs/website/audit/competitive-analysis.md` | Algorithm A | Summary of competitor observations |
| `docs/website/audit/analytics-summary.md` | Algorithm A | GA4 top pages and metrics |
| `docs/website/discovery-brief.md` | Algorithm B Step 0 | Written by website-discovery skill; required before sitemap proposal |

---

## Constitution Check

- **Principle I (Human-in-the-Loop)**: Approval gates at every layer. No status advances without the operator.
- **Principle II (Draft-First)**: All output staged in blueprint.md before any build.
- **Principle IV (Brand and Voice)**: brand-standards + compliance-audit on every brief and spec.
- **Principle V (Transparency)**: Audit reports are immutable snapshots; blueprint.md is version-tracked via git.
- **Principle VI (Silence Over Noise)**: Only runs when triggered.
