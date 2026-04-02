---
name: programmatic-seo
description: "Build SEO and GEO content pages at scale using templates and data for education, readiness, and decision-making topics"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /programmatic-seo
metadata:
  openclaw:
    emoji: "magnifying-glass"
    requires:
      bins: []
      env: []
---

# Programmatic SEO & GEO Strategy

## Overview

Build search-optimized content pages at scale using reusable templates populated with structured data. Covers both traditional SEO (Google organic) and GEO (Generative Engine Optimization for AI search engines like ChatGPT, Perplexity, Google AI Overviews). Every page must carry genuine editorial value -- no thin SEO-bait. Voice calibration rules E1-E5 from `voice-calibration` apply to all programmatic pages.

---

## Initial Assessment

Before designing any programmatic SEO strategy, gather:

1. **Content Opportunity**
   - What search patterns exist around the education, healing, or retreat space?
   - How many potential pages can be generated from the data?
   - What is the search volume distribution (head terms vs. long-tail)?

2. **Audience Intent**
   - What life stage or transition is the searcher in (burnout, grief, midlife, curiosity)?
   - Are they researching, comparing, or ready to act?
   - What questions do they need answered before trusting an organization?

3. **Competitive Landscape**
   - Who ranks for these terms today (directories, clinics, media outlets, competitors)?
   - What does their content look like -- depth, format, data quality?
   - Where are the content gaps the organization can fill with authoritative, first-party knowledge?

---

## the organization Page Archetypes

Select one or more archetypes based on available data and audience need. Each archetype maps to a specific search pattern family.

### 1. Jurisdiction / Legality Pages

**Pattern**: "Is [substance] legal in [state/country]?"
**Example searches**: "Is psilocybin legal in Oregon", "ayahuasca legality in Costa Rica", "ketamine therapy legal status California"

**What it covers**:
- Current legal status with effective dates and statute references
- Decriminalization vs. legalization distinction
- Licensed program vs. underground risk framing
- Links to state/country regulatory body pages

**URL structure**: `/legal/[substance]-in-[jurisdiction]/`

**Data requirements**: Jurisdiction name, substance, legal status enum (legal/decriminalized/illegal/gray-area), effective date, source statute or regulation, last-verified date.

**Unique value rule**: Each page must include jurisdiction-specific regulatory nuance. Never just swap the state name into identical copy.

---

### 2. Topic Hubs

**Pattern**: "[Topic] guide" or "what to know about [topic]"
**Example searches**: "psychedelic preparation guide", "integration after a ceremony", "microdosing vs macrodosing", "is ayahuasca safe"

**Topics**: Readiness, safety, integration, preparation, microdosing vs. macrodosing, set and setting, contraindications, therapeutic mechanisms.

**What it covers**:
- Comprehensive single-topic resource (1,500-3,000 words)
- Cites peer-reviewed research and clinical references where available
- Links out to spoke pages (FAQ clusters, comparison pages, guides)

**URL structure**: `/learn/[topic-slug]/`

**Unique value rule**: Hub pages are editorial, not templated. They serve as the canonical resource for the topic and anchor the internal linking graph.

---

### 3. Decision / Comparison Pages

**Pattern**: "[X] vs [Y]" or "difference between [X] and [Y]"
**Example searches**: "psilocybin vs ayahuasca", "retreat vs clinic", "group ceremony vs individual session", "therapeutic setting vs recreational"

**What it covers**:
- Side-by-side structured comparison (duration, setting, intensity, legal status, cost range, evidence base)
- "Best for" recommendation by use case or readiness level
- Links to both topic hubs
- No false equivalence -- be honest about tradeoffs

**URL structure**: `/compare/[x]-vs-[y]/`

**Data requirements**: Modality/setting name, attributes (duration, setting, intensity scale, legal status, evidence quality rating, typical cost range), best-for profiles.

---

### 4. Audience-Entry Pages

**Pattern**: "[Healing modality] for [life transition]" or "[life transition] and psychedelics"
**Example searches**: "psychedelic therapy for burnout", "psilocybin for grief", "midlife crisis and plant medicine", "healing after success"

**Life transitions**: Burnout, grief/loss, midlife transition, post-success emptiness, relationship dissolution, identity crisis, chronic anxiety/depression plateau, spiritual seeking.

**What it covers**:
- Validates the searcher's experience without pathologizing
- Explains how the modality addresses that specific transition
- Includes relevant testimonials (load via `senja` skill if available)
- Clear next step (connection call, readiness quiz, guide page)

**URL structure**: `/for/[life-transition]/`

**Data requirements**: Life transition slug, description, relevant modalities, matching testimonial IDs, related guide pages.

---

### 5. FAQ Clusters (GEO-Optimized)

**Pattern**: "Can I [action] after [ceremony]?", "How long does [effect] last?", "What happens during [modality]?"
**Example searches**: "can I drive after a psilocybin session", "how long does ayahuasca last", "what to expect during a retreat"

**What it covers**:
- One authoritative answer per page (300-800 words)
- Structured as question-then-answer with clear, citable reasoning
- Grouped into clusters linked from the parent topic hub
- FAQ schema markup on every page (cross-reference schema-markup patterns)

**URL structure**: `/faq/[question-slug]/`

**Unique value rule**: Each FAQ page must provide a complete, standalone answer. AI search engines cite pages that give a direct, well-reasoned answer in the first 2-3 sentences, then expand with supporting detail.

---

### 6. Guide Pages

**Pattern**: "How to [prepare/integrate/choose]" or "[topic] checklist"
**Example searches**: "how to prepare for a psilocybin retreat", "integration practices after ceremony", "how to choose a facilitator", "what to pack for an ayahuasca retreat"

**What it covers**:
- Step-by-step actionable instructions
- Checklists where applicable
- Links to related topic hubs, FAQ clusters, and comparison pages
- Draws on the organization's direct facilitation experience (400+ alumni, 60+ retreats)

**URL structure**: `/guides/[guide-slug]/`

---

## GEO Layer (Generative Engine Optimization)

AI search engines (ChatGPT, Perplexity, Google AI Overviews) select sources differently from traditional search. Apply these rules to every programmatic page to maximize citation probability.

### Structure Content as "Best Answer"

- **Lead with a direct answer.** The first 2-3 sentences of every page should contain a clear, complete answer to the implied question. AI engines extract this as their citation snippet.
- **Define entities explicitly.** When a page mentions a substance, modality, or concept for the first time, provide a one-sentence definition. AI engines use entity definitions to build knowledge graphs.
- **Use structured reasoning.** Present claims with supporting evidence in a logical chain: claim, mechanism, evidence, caveat. This pattern signals authority to AI extractors.

### FAQ Cluster Format AI Engines Prefer

- One question per URL. Multi-question FAQ pages dilute citation targeting.
- Question in H1. Answer begins immediately in the first paragraph.
- Cite primary sources inline (e.g., "according to a 2024 Johns Hopkins study" with a link). AI engines weight cited content higher.
- Include a structured data FAQ block (JSON-LD) matching the visible Q&A.

### Entity Markup Integration

- Apply JSON-LD schema markup to every programmatic page type:
  - FAQ pages: `FAQPage` schema
  - Guide pages: `HowTo` schema
  - Comparison pages: `ItemList` with compared entities
  - Organization references: `Organization` schema linking to the organization
- If a `schema-markup` skill exists in the workspace, defer to its templates. Otherwise, write inline JSON-LD blocks.

### Comprehensiveness Signals

- **Cover the topic thoroughly.** AI engines prefer pages that address the full scope of a question, including edge cases and caveats, over pages that answer narrowly.
- **Link to related content.** Internal links from hubs to spokes (and cross-links between related spokes) signal topical depth.
- **Cite primary sources.** Link to peer-reviewed studies, regulatory documents, and authoritative organizations. Avoid circular citation (linking only to your own pages).
- **Update dates visible.** Display "Last updated: [date]" on every page. AI engines penalize stale content.

### Avoid GEO Anti-Patterns

- Thin template pages with only variable substitution -- AI engines detect and skip these.
- Keyword-stuffed content that reads unnaturally.
- Pages without any external citations or source references.
- Duplicate answers across multiple pages (causes self-cannibalization in AI results).

---

## Keyword Pattern Research Methodology

1. **Identify the repeating structure**
   - What is the variable? (jurisdiction, life transition, modality, question)
   - What is the static frame? ("Is [X] legal in [Y]", "[modality] for [transition]")

2. **Validate demand**
   - Estimate aggregate search volume across all variable combinations
   - Check volume distribution: prioritize patterns where many combinations each have measurable volume
   - Identify seasonal patterns (e.g., New Year resolution spikes, post-election policy searches)

3. **Assess competition per pattern**
   - Who ranks for the head term today?
   - Are results dominated by authoritative medical/legal sources, or by thin directories?
   - Where content gaps exist, prioritize those patterns first

4. **Prioritize by impact**
   - Score each pattern: (aggregate volume) x (content gap size) x (conversion proximity)
   - Launch highest-scoring pattern first; expand to others in phases

---

## Data Requirements and Schema Design

For each page archetype, define a structured data schema before writing any templates.

**Example -- Jurisdiction/Legality pages**:
```
jurisdiction:
  name: "Oregon"
  country: "United States"
  substance: "psilocybin"
  legal_status: "legal-regulated"   # enum: legal-regulated | decriminalized | illegal | gray-area
  effective_date: "2023-01-01"
  statute_reference: "Oregon Measure 109"
  source_url: "https://..."
  last_verified: "2026-02-15"
  notes: "Licensed service centers only; personal possession decriminalized"
  related_jurisdictions: ["California", "Colorado"]
```

**Rules**:
- Every field that appears on the page must exist in the schema
- Include a `last_verified` date field -- pages with stale data get noindexed
- Include `related_*` fields to power internal linking automatically
- Store data in a structured format (JSON, YAML, or database table) -- never hardcode data into templates

---

## Template Architecture

### How to Build Reusable Page Templates

1. **Separate data from presentation.** The template is the HTML/component structure. The data populates it. Never write content directly into the template.

2. **Conditional sections.** Use conditional logic to show/hide sections based on data availability:
   - If `testimonial_ids` exist for this page, render a testimonial block
   - If `related_pages` is empty, omit the "Related" section rather than showing an empty container

3. **Unique editorial blocks.** Every template must include at least one section that requires page-specific editorial input (a paragraph, a recommendation, a contextual insight). Pure variable-swap pages are prohibited.

4. **Template structure**:
```
H1: [Dynamic title using primary variable]

Intro: [2-3 sentences -- must be unique per page, not variable-swapped boilerplate]

Section 1: [Primary data-driven content]
Section 2: [Contextual/editorial section -- unique per page]
Section 3: [Related resources -- auto-generated from data relationships]

CTA: [Appropriate to intent stage -- "Book a Connection Call" for bottom-funnel, "Read the Guide" for top-funnel]

Schema markup: [JSON-LD block matching page type]
```

5. **Voice calibration.** Apply `voice-calibration` E1-E5 rules to all template copy, including the editorial blocks. Programmatic does not mean robotic.

---

## Internal Linking (Hub-and-Spoke Model)

### Structure

- **Hub**: Topic hub page (e.g., `/learn/psilocybin-preparation/`)
- **Spokes**: Individual programmatic pages (FAQ pages, guide pages, comparison pages) that link back to the hub
- **Cross-links**: Related spokes link to each other (e.g., a legality page links to the relevant preparation guide)

### Rules

- Every programmatic page must link to its parent hub
- Every hub must link to all its spoke pages
- Cross-link related spokes (limit: 3-5 cross-links per page to avoid link dilution)
- Implement breadcrumb navigation with `BreadcrumbList` schema markup
- No orphan pages -- every page must be reachable from the main site navigation within 3 clicks

### Automated Linking

- Use the `related_*` fields in the data schema to auto-generate "Related" sections
- Build a sitemap index that groups pages by archetype

---

## Indexation Strategy

1. **XML Sitemap**
   - Create separate sitemaps per page archetype (e.g., `sitemap-legal.xml`, `sitemap-faq.xml`)
   - Include `<lastmod>` dates matching the `last_verified` field in the data
   - Submit all sitemaps via Google Search Console

2. **Robots.txt**
   - Allow crawling of all programmatic page directories
   - Block crawling of any staging/preview URLs
   - Do not accidentally block programmatic page paths with overly broad disallow rules

3. **Crawl Budget**
   - Phase launches: start with highest-priority pattern (50-100 pages), monitor indexation rate, then expand
   - Noindex pages where data quality is incomplete (missing key fields, unverified dates)
   - Avoid infinite URL patterns (e.g., filter combinations that generate thousands of near-duplicate URLs)

4. **Canonical Tags**
   - Every programmatic page gets a self-referencing canonical tag
   - If two pages risk cannibalization, consolidate into one and redirect the other

---

## Quality Checks Pre-Launch

### Content Quality
- [ ] Each page provides unique editorial value beyond variable substitution
- [ ] Voice calibration E1-E5 applied (load `voice-calibration` skill)
- [ ] All cited sources are real and linked
- [ ] No placeholder or missing-data sections visible

### Thin Content Audit
- [ ] No two pages share >60% identical text
- [ ] Every page has at least one unique editorial paragraph
- [ ] Pages with insufficient data are set to noindex until data is complete

### Cannibalization Check
- [ ] No two pages target the same primary keyword
- [ ] Hub pages and spoke pages have clearly differentiated intent
- [ ] Comparison pages do not duplicate content from either entity's hub page

### Technical SEO
- [ ] Unique title tags and meta descriptions per page
- [ ] Proper heading hierarchy (single H1, logical H2/H3 structure)
- [ ] JSON-LD schema markup present and valid (test with Google Rich Results Test)
- [ ] Canonical tags correct
- [ ] Page speed acceptable (< 3s LCP)
- [ ] Breadcrumbs implemented with structured data

### Data Quality
- [ ] All `last_verified` dates are within 90 days
- [ ] No blank or null values displayed on any page
- [ ] Legal status data verified against primary regulatory sources
- [ ] Testimonials loaded dynamically (not hardcoded)

---

## Steps

1. **Assess opportunity.** Gather business context, audience intent, and competitive landscape per the Initial Assessment section.
2. **Select archetypes.** Choose 1-3 page archetypes from the list above based on available data and audience need.
3. **Research keyword patterns.** For each archetype, identify the repeating search structure, validate demand, assess competition, and prioritize by impact.
4. **Design data schema.** Define the structured data schema for each archetype. Identify data sources (first-party knowledge, regulatory databases, testimonial API via `senja` skill, retreat data via `airtable-retreats` skill).
5. **Build templates.** Create reusable page templates with conditional sections and mandatory editorial blocks. Apply voice calibration.
6. **Populate data.** Fill the data store for the first launch phase (50-100 pages recommended).
7. **Apply GEO layer.** Ensure every page follows the GEO rules: direct-answer lead, entity definitions, cited sources, FAQ schema markup, update dates.
8. **Wire internal linking.** Connect hubs to spokes, add cross-links, implement breadcrumbs.
9. **Run quality checks.** Complete every item in the pre-launch checklists above.
10. **Configure indexation.** Generate sitemaps, verify robots.txt, submit to Search Console.
11. **Launch in phases.** Deploy highest-priority pattern first. Monitor indexation rate, rankings, and AI citation appearances for 2-4 weeks before launching the next pattern.

## Output

Deliver a strategy document containing:

- **Opportunity analysis**: Keyword patterns identified, volume estimates, competition assessment, feasibility rating per archetype
- **Data schema**: Complete field definitions for each selected archetype
- **Template specification**: Page structure, conditional sections, editorial block requirements, schema markup type
- **Internal linking map**: Hub-and-spoke diagram showing page relationships
- **Launch plan**: Phased rollout with page counts, priority order, and success metrics
- **Quality checklist**: Completed pre-launch checklist for the first batch

## Error Handling

- If data is incomplete for a page archetype: flag the missing fields and recommend noindexing those pages until data is available. Do not launch pages with blank sections.
- If a keyword pattern shows zero measurable search volume: deprioritize that pattern. Note it for future reassessment but do not build pages speculatively.
- If cannibalization is detected between two pages: recommend consolidation into a single page with a 301 redirect from the weaker URL.
- If voice calibration skill is unavailable: warn the operator that brand voice cannot be verified, and flag all copy for manual review before launch.

## Related Skills

- **voice-calibration**: E1-E5 rules for all copy, including programmatic pages
- **senja**: Load testimonials dynamically for audience-entry pages
- **airtable-retreats**: Fetch live retreat dates and availability (never hardcode)
- **brand-standards**: Brand identity and visual consistency rules
- **copywriting**: For editorial blocks that require non-templated writing
