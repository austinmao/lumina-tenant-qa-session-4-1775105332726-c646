---
name: seo-strategy
description: "Develop SEO and content strategy for funnel pages and site architecture"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /seo-strategy
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# SEO Strategy

Develop SEO strategy for funnel pages, landing pages, and site architecture. This skill covers the strategic planning layer of SEO — keyword targeting, content strategy for search, site audit planning, and analytics-informed recommendations. For technical SEO implementation, use `seo-monitoring`. For keyword research, use `keyword-research`.

## When to Use

- Planning SEO strategy for a new funnel or site section
- Developing content strategy informed by search demand
- Auditing existing site strategy for SEO alignment
- Integrating SEO considerations into campaign planning

## Core Approach

### Brand-First SEO

Before any SEO strategy work:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/brand-guide.md` for positioning and audience context
3. Read `<brand_root>/messaging.md` for keyword context and content patterns

SEO is a constraint that improves user experience, not a trick. Every recommendation must serve both search engines and human visitors. Reject any technique that degrades user experience for ranking gain.

### Strategy Layers

1. **Keyword strategy**: Map search intent to content pages. Every page targets a primary keyword and 2-3 secondary keywords aligned with the page's purpose.

2. **Content gap analysis**: Identify search demand not currently served by existing content. Prioritize gaps by search volume, intent alignment with business goals, and competitive difficulty.

3. **Site architecture for SEO**: URL taxonomy, internal linking structure, and content hierarchy designed to build topical authority. URL structures must be human-readable, SEO-friendly, and stable.

4. **Competitive positioning**: Analyze competitor content strategies, identify positioning gaps, and recommend differentiation angles grounded in the brand's unique strengths.

5. **Measurement framework**: Define KPIs, tracking requirements, and reporting cadence for SEO initiatives. Every strategy recommendation has a measurable success criterion.

### Funnel SEO Integration

For campaign funnels (webinar-to-retreat, application, lead magnet):
- Ensure landing pages target relevant search intent even if primary traffic is paid or email
- Include schema markup recommendations for rich results (FAQ, Event, Course)
- Align page copy keyword density with target terms without compromising brand voice
- Plan post-campaign SEO value: can the landing page rank organically after the campaign window closes?

## Output Format

### SEO Strategy Brief
- **Objective**: What search outcomes this strategy serves
- **Target keywords**: Table with keyword, search volume, difficulty, intent type, recommended page, priority
- **Content gaps**: Prioritized list of unserved search demand with recommended content type
- **URL taxonomy**: Hierarchical list with rationale for each level
- **Competitive analysis**: Key competitors, their SEO positioning, and the strategic gap
- **Measurement**: KPIs, tracking setup, reporting cadence

### Page-Level SEO Recommendations
- Primary keyword and intent match
- Title tag recommendation (with character count)
- Meta description recommendation (with character count)
- Schema markup type recommendation
- Internal linking targets

## Boundaries

- SEO strategy recommendations are advisory. All implementations route through the appropriate agent (Frontend Engineer for technical changes, Copywriter for content).
- Never recommend keyword stuffing, cloaking, link schemes, or any technique that violates search engine guidelines.
- Never fabricate search volume data, ranking positions, or competitive metrics. If data is unavailable, state the gap and recommend the data source.
- Never write primary page copy. Provide keyword targets and structure recommendations; the Copywriter writes the copy.

## Dependencies

- `keyword-research` — detailed keyword analysis and opportunity scoring
- `seo-monitoring` — technical SEO audit and ongoing tracking
- `information-architecture` — site structure and URL taxonomy
- `brand-standards` — ensures SEO recommendations align with brand voice
