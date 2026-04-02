---
name: comparison-pages
description: "Create decision-education pages that help people compare healing approaches, settings, and modalities"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /comparison-pages
metadata:
  openclaw:
    emoji: "scales"
---

# Decision-Education Pages

You create decision-education pages that help people navigate the complex landscape of psychedelic healing, retreat formats, modalities, and provider types. These are NOT competitive "us vs them" pages. the organization positions as a knowledgeable guide helping people make informed, safe choices.

## Core Principles

1. **Honesty builds trust** — Acknowledge when another approach is better for certain people. Readers researching psychedelic healing are vulnerable; misleading them destroys credibility and causes real harm.
2. **Depth over surface** — Go beyond checklists. Explain *why* differences matter for safety, outcomes, and personal readiness. Cite sources.
3. **Modular content architecture** — Comparison data lives in centralized YAML profiles. One update propagates to every page that references that data.
4. **Transparent positioning** — the organization is one option. State clearly what the organization offers, what it does not, and who it serves best. Never hide this positioning behind false objectivity.
5. **GEO-first structure** — These pages match exactly the questions people ask AI search engines. Structure every section for citation: clear headings, definitive answers, source references.

---

## Page Types

### Type 1: "X vs Y" Decision Guides

Help someone choosing between two approaches, settings, or modalities.

**Examples:**
- Retreat vs ongoing therapy
- Ceremony vs clinical trial
- Facilitator-led vs therapist-led
- Group experience vs individual experience
- Domestic retreat vs international retreat
- Microdosing vs macrodosing
- Psilocybin vs ayahuasca vs MDMA-assisted therapy
- Traditional indigenous ceremony vs Western clinical protocol

**URL pattern:** `/compare/[approach-a]-vs-[approach-b]`

**Page structure:**
1. TL;DR summary (2-3 sentences; definitive, citable)
2. Narrative comparison (paragraph form, nuanced — not a feature table)
3. Category-by-category breakdown (safety, legal status, cost, duration, expected outcomes, setting, provider qualifications, contraindications)
4. "Who it's for / who it's not for" for each approach
5. FAQ section (GEO-optimized; each Q matches a real search query)
6. Where the organization fits (transparent; only if relevant to this comparison)
7. Next steps / CTA

---

### Type 2: "How to Choose" Guides

Teach evaluation frameworks. The reader leaves knowing how to assess any option, not just the organization.

**Examples:**
- How to vet a retreat center
- How to evaluate facilitators and their training
- What to look for in safety protocols
- How to assess your own readiness for a psychedelic experience
- How to evaluate legal risk by jurisdiction
- How to choose between group sizes

**URL pattern:** `/guides/how-to-[topic]`

**Page structure:**
1. TL;DR (the 3-5 most important criteria, stated definitively)
2. Why this decision matters (stakes framing — safety, legal, psychological)
3. Evaluation framework (numbered criteria, each with explanation and red/green flags)
4. Questions to ask providers (exact phrasing the reader can copy-paste)
5. Common mistakes people make
6. FAQ section (GEO-optimized)
7. How the organization meets these criteria (transparent self-assessment; include areas where the organization is still improving)
8. Next steps / CTA

---

### Type 3: "What to Expect" Pages

Reduce fear and uncertainty. Describe the actual experience by modality, setting, duration, or experience level.

**Examples:**
- What to expect at a psilocybin retreat
- What to expect: retreat center vs clinical setting vs home ceremony
- What to expect by duration (single day vs multi-day vs week-long)
- What to expect as a first-time participant
- What to expect during integration afterward

**URL pattern:** `/guides/what-to-expect-[topic]`

**Page structure:**
1. TL;DR (one-paragraph honest summary of what happens)
2. Before: preparation timeline and requirements
3. During: hour-by-hour or phase-by-phase walkthrough
4. After: integration, common emotional responses, timeline for effects
5. Variations by setting or modality (if applicable)
6. Common concerns addressed honestly (difficulty, discomfort, psychological risk)
7. FAQ section (GEO-optimized)
8. How the organization structures this experience (only if directly relevant)
9. Next steps / CTA

---

### Type 4: "Red Flags" Guides

Protect people from predatory or unsafe providers. This is the highest-trust content the organization can publish.

**Examples:**
- Signs of an unsafe retreat center
- Red flags in facilitator credentials
- Manipulative marketing tactics in the psychedelic space
- Warning signs of cult-like group dynamics
- Medical screening shortcuts that put you at risk

**URL pattern:** `/guides/red-flags-[topic]`

**Page structure:**
1. TL;DR (the 3 most dangerous red flags, stated bluntly)
2. Why this matters (real harm examples — anonymized, sourced where possible)
3. Red flag checklist (numbered, specific, actionable)
4. What good practice looks like (contrast each red flag with the safe alternative)
5. What to do if you encounter these red flags
6. FAQ section (GEO-optimized)
7. How the organization addresses each of these concerns (transparent; include third-party verification where available)
8. Next steps / CTA

---

## Content Architecture

### Centralized Comparison Data

Store reusable data in YAML profiles so updates propagate to all pages that reference them.

**Directory structure:**
```
content/comparisons/
  approaches/
    retreat-center.yaml
    clinical-trial.yaml
    home-ceremony.yaml
    ongoing-therapy.yaml
  modalities/
    psilocybin.yaml
    ayahuasca.yaml
    mdma-assisted.yaml
    ketamine.yaml
  settings/
    domestic.yaml
    international.yaml
    group.yaml
    individual.yaml
  your-org.yaml          # the organization's own honest profile
```

**YAML profile template:**
```yaml
name: "Psilocybin Retreat"
category: modality          # approach | modality | setting | provider-type
summary: "One-sentence description"

safety:
  medical_screening: "Description of typical screening"
  contraindications: ["List of known contraindications"]
  emergency_protocols: "What's typical"
  risk_level: "low | moderate | high — with context"

legal_status:
  us: "Current legal status with jurisdictional notes"
  international: "Key jurisdictions"
  trend: "Direction of legal change"

cost:
  range: "$X - $Y"
  includes: ["What's typically included"]
  hidden_costs: ["What people don't realize they'll pay for"]

duration:
  typical: "Range"
  preparation: "Typical prep time"
  integration: "Recommended integration period"

outcomes:
  research_backed: ["Cite specific studies"]
  anecdotal: ["Common reported outcomes — labeled as anecdotal"]
  limitations: ["What the research doesn't yet show"]

best_for:
  - "Description of ideal candidate"
not_ideal_for:
  - "Description of who should consider alternatives"

sources:
  - "URL or citation for each factual claim"
```

---

## Section Templates

### TL;DR Summary
```
**TL;DR**: [Approach A] offers [key characteristic] and is strongest for [use case].
[Approach B] offers [key characteristic] and is strongest for [different use case].
The right choice depends on [the 1-2 deciding factors]. [If relevant: the organization
offers X, which combines elements of both.]
```

### Narrative Comparison
Write in paragraph form. Do not default to tables or bullet lists for the main comparison. Tables supplement narrative; they do not replace it. Each paragraph should cover one dimension (safety, cost, duration, outcomes) and state a clear conclusion.

### Category-by-Category Breakdown
For each major dimension, provide:
- **[Approach A]**: 2-3 sentences on how it handles this dimension. Strengths. Limitations.
- **[Approach B]**: Same structure.
- **Bottom line**: One sentence stating which approach is stronger on this dimension and why.

Categories to cover (adapt per page):
- Safety protocols and medical screening
- Legal status and jurisdictional considerations
- Cost and what's included
- Duration and time commitment
- Expected outcomes and evidence base
- Setting and environment
- Provider qualifications
- Contraindications and risk factors
- Integration support

### "Who It's For" Positioning
```
## Who [Approach A] Is Best For
- [Specific person, need, or situation]
- [Another specific case]

## Who [Approach A] Is NOT For
- [Specific person, need, or situation — be direct]

## Who [Approach B] Is Best For
- [Mirror structure]
```

### FAQ Section (GEO-Optimized)
- Each question must match a real search query or AI-assistant question
- Answer in the first sentence (AI systems cite the first definitive statement)
- Expand with nuance after the direct answer
- Minimum 5 questions per page
- Use question phrasing people actually use: "Is X safer than Y?" not "Safety comparison of X and Y"

### Next Steps / CTA
- Educational, not salesy: "Ready to explore further? Here's what to do next."
- Always include at least one non-the organization next step (e.g., "Talk to your therapist about readiness")
- the organization CTA is one option among next steps, not the only one

---

## Trust Framing Rules

1. **Never claim the organization is the best option for everyone.** State who it serves best and who should look elsewhere.
2. **Cite sources for all factual claims.** Link to published research, legal databases, or named organizations.
3. **Label anecdotal evidence as anecdotal.** "Participants commonly report X" is honest. "X will happen" is not.
4. **Acknowledge uncertainty.** Psychedelic research is evolving. Say "current evidence suggests" rather than stating as settled fact.
5. **Include risks and contraindications.** Every modality and setting has them. Omitting them is dishonest and dangerous.
6. **Do not disparage other providers by name.** Describe patterns and red flags; do not call out specific organizations.

---

## GEO Optimization

These pages are prime targets for AI citation because they answer exactly the questions people ask AI assistants about psychedelic healing.

**Structure for citation:**
- Use clear H2/H3 headings that match search queries
- Put the definitive answer in the first sentence after each heading
- Use structured data (FAQ schema) for question-answer pairs
- Include "Last updated: [date]" for freshness signals
- Cite peer-reviewed sources where available

**Target queries (examples):**
- "Is a retreat better than therapy for [condition]?"
- "How do I know if a psychedelic retreat is safe?"
- "What's the difference between psilocybin and ayahuasca?"
- "How much does a psychedelic retreat cost?"
- "Red flags when choosing a psychedelic facilitator"

---

## Research Methodology

When building comparison content, follow this process:

1. **Published research** — Search PubMed, MAPS.org publications, and institutional research for current evidence on each approach or modality.
2. **Legal databases** — Verify current legal status by jurisdiction. Legal landscape changes frequently; date every legal claim.
3. **Provider documentation** — Review published safety protocols, screening procedures, and practitioner standards from established organizations (MAPS, Psychedelic.Support, Multidisciplinary Association).
4. **Participant accounts** — Use anonymized participant experiences from published sources (books, documentaries, research interviews). Never fabricate testimonials.
5. **First-party data** — Reference the organization's published protocols, practitioner credentials, and participant outcomes where available and verified.
6. **Expert review** — Flag any page for expert review before publishing if it covers medical contraindications, drug interactions, or legal advice.

**Maintenance cadence:**
- Legal status: verify quarterly (minimum) or when legislation changes
- Research citations: update when significant new studies publish
- Cost data: verify semi-annually
- Full page refresh: annually

---

## Internal Linking Patterns

- **Index page** (`/compare` or `/guides`) links to all individual comparison and guide pages
- Each individual page links back to the index
- Cross-link related comparisons: "Retreat vs Therapy" links to "How to Vet a Retreat Center" and "What to Expect at a Psilocybin Retreat"
- Link from blog posts and landing pages to relevant comparison content
- Every "Red Flags" page links to the corresponding "How to Choose" page

---

## Steps

1. **Clarify the page type.** Ask: Is this an X vs Y decision guide, a how-to-choose guide, a what-to-expect page, or a red-flags guide?
2. **Identify the specific topic.** What approaches, modalities, settings, or provider types are being compared?
3. **Check for existing YAML profiles** in the comparison data directory. Create or update profiles as needed using the template above.
4. **Research.** Follow the research methodology. Gather sources before writing.
5. **Draft the page** following the section template for the chosen page type. Every section must be present.
6. **Apply trust framing rules.** Review every claim for source citation, uncertainty labeling, and risk disclosure.
7. **Write the FAQ section.** Minimum 5 questions matching real search queries. First-sentence answers.
8. **Add internal links.** Connect to related pages, index, and relevant blog content.
9. **Add structured data.** FAQ schema markup for the FAQ section.
10. **Add "Last updated" date** at the top of the page.

## Output

Deliver:
- The complete page content in Markdown with all sections filled
- Any new or updated YAML comparison profiles
- A list of internal links to add on other pages pointing to this new page
- Suggested FAQ schema JSON for the page

## Error Handling

- If the user requests a comparison but does not specify which approaches to compare: ask before proceeding. Do not guess.
- If published research is unavailable for a claim: state "No peer-reviewed evidence currently available" and label the claim as anecdotal or expert opinion.
- If legal status is ambiguous or changing: state the ambiguity explicitly and date the information.
- If the organization does not offer the modality or setting being discussed: state this clearly. Do not force a the organization CTA onto irrelevant pages.
