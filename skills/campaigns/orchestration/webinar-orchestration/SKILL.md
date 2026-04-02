---
name: webinar-orchestration
description: "Create conversion-optimized webinar presentations using Perfect Webinar + Masterclass DNA frameworks"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /webinar-orchestration
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Webinar Orchestration

Create complete, conversion-optimized webinar presentations using Russell Brunson's Perfect Webinar framework combined with Vishen Lakhiani's Masterclass Script DNA. Outputs are Gamma.app-style single-page HTML presentations saved to ~/webinars/.

## Tenant Context (Load First)

Before generating any webinar content, load tenant-specific context:

1. Read `memory/site-context.yaml` to confirm the active tenant
2. Read `config/webinar-context.yaml` if it exists (pricing, stats, origin story, prohibited patterns)
3. Read the active tenant's brand guide (`<brand_root>/brand-guide.md` and `<brand_root>/voice.md`)
4. If tenant context is unavailable: insert `[TENANT: ...]` placeholders and flag all required fields to the operator before drafting

Tenant overlay skills (in `tenants/<name>/skills/`) take full precedence and replace this platform version when active. If you are running in a tenant workspace, the tenant overlay should already be loaded.

## When to Use

- Creating a new webinar presentation for a retreat or product launch
- Building a presentation for a specific event or campaign
- Creating variations of existing webinars
- Generating slide decks for webinar-to-retreat conversion funnels

## Reference Documents

Always read `docs/webinar/reference/combined-webinar-ref.yaml` before generating any webinar. Additional references:
- `expert-secrets-ref.yaml`
- `webinar-coaching-ref.yaml`
- `masterclass-dna-ref.yaml`

All located in `docs/webinar/reference/`.

## Framework Structure

Every webinar applies the Perfect Webinar structure (Brunson) + Masterclass Script DNA (Vishen):

### The One Big Domino

Every webinar is built around a single belief that must land in the body, not just the mind. The Big Domino must be identity-level and emotionally charged -- not a logical argument.

**Test**: Does it make someone feel something, or just think something?

**Good examples**: "The difference between transformation and trauma is the container."
**Bad examples**: "Knowing how to navigate this is learnable."

The Domino must make the offer feel like the only logical next step without ever having to argue it.

### Belief-Changing, Not Teaching

Presentations change beliefs. Teaching kills sales. Every slide serves to break a false belief or install a new one -- never to simply share information.

## Required Structural Elements

The following elements are mandatory in every webinar. Omitting any of these is a structural violation.

### 1. Origin Story Framing

Load the operator's origin story arc from tenant context (`config/webinar-context.yaml` or `tenant.yaml`) before writing this section. The arc must reflect the operator's actual journey and brand positioning.

**Universal rule**: The origin story is about discovering what was possible, not fixing what was broken. The operator was not in crisis — the arc is curiosity/high-achievement → profound discovery → compulsion to share.

**Correct arc template**: curious high-achiever → stumbled into profound possibility → couldn't not share it.
**Wrong arc**: "tried X and it didn't work" — this positions the organization as a last resort.

Origin story themes and exact language come from tenant context — do not invent them.

### 2. Plutchik Framework (structural anchor)

Every webinar opens the Three Secrets section with Plutchik's emotion wheel: "Love = safety + joy." This single equation maps all three secrets (inner safety, outer safety, the container) onto one emotional truth. It is the spine of the whole framework and must appear before Secret #1.

### 3. Four Provider Vetting Questions (checklist slide)

Every webinar must include these four exact questions:
1. How do you assess my medical and medication situation before I arrive?
2. How do you help me build my inner capacity to hold experiences before ceremony?
3. How do you build connection among participants?
4. How do you support integration?

Framing: "Choose a provider the way you'd choose a surgeon for life-altering surgery."

### 4. Authority -> Humility Turn

After establishing credibility, include an explicit turn where the operator surrenders authority into service. Example: "But what I've learned after facilitating hundreds of people is that the real transformation never comes from me."

### 5. Live Curiosity Demo (pattern-break)

Between Secret 2 and Secret 3, include a live volunteer exercise demonstrating the "What's that like?" inquiry skill. the operator asks a volunteer: "What's it like to be you right now?" then double-clicks into their answer twice.

### 6. Embodied Moment

One 2-4 minute guided embodied moment -- breathwork, body scan, or somatic awareness -- placed between the origin story and the Three Secrets. Regulated nervous systems trust. Activated nervous systems hesitate. This is a conversion mechanism.

### 7. Two Testimonials, Two Archetypes

At minimum two participant stories: one high-achiever/skeptic archetype and one "I thought I was too broken/anxious" archetype. Use `[PLACEHOLDER]` until the operator provides verified quotes.

### 8. Five-Point Container Checklist (inside Secret #1)

Required teaching element: (1) medical + psychological screening, (2) structured preparation protocol, (3) trained facilitators with proper ratio, (4) in-ceremony distress support plan, (5) integration support after.

Include a "take a screenshot of this slide" prompt and keep the checklist visible for 10-15 seconds after delivery.

### 9. Pattern-Break Micro-Reset

30-second pattern-break between Secret #2 and Secret #3. A breath prompt or chat question maintains attention during the highest cognitive fatigue zone.

### 10. QR Code on CTA and Q&A Slides

Linked directly to the application. Scan-to-apply removes friction at the conversion moment.

### 11. Medical Disclaimer (early)

Slide 02 or Slide 03: one calm, non-lawyer-y sentence routing medication questions to the screening call. "Nothing in this session is medical advice -- anything specific to your medications or health history gets assessed individually in screening."

### 12. Seeded Q&A

Seed the Q&A with 3 prepared answers before opening the floor: (1) bad experience, (2) medications, (3) legitimacy.

## Offer Rules

### Non-Profit Positioning
If the organization has non-profit status, include the tax-deductibility benefit on the investment slide — framed as proof of mission alignment, not just a tax benefit. Check tenant context for non-profit status.

### Single Offer
Never fork the offer. Single option only -- forking kills conversions (Mindvalley data: +30% revenue from removing bundle).

### Offer Stack Framing
Frame as safety architecture ("Layer 1: Preparation," "Layer 2: Screening," "Layer 3: Integration") -- not "Bonus 1 worth $500." Do not use price-contrast anchoring theatrics.

### Pricing
Load pricing from tenant context (`config/webinar-context.yaml` or offer record). **Do not invent pricing.** If tenant pricing is unavailable, insert `[TENANT: pricing — fill before presenting]` and halt.

### Guarantee Framing
Guarantees are framed around process integrity: the quality of screening, facilitation, and integration support -- never around healing outcomes.

## Prohibited Patterns (Universal)

These apply to all tenants:

- Do not say "adverse events were rare" as a blanket clinical claim
- Do not say "designed to produce lasting change" -- say "designed to support lasting change"
- Do not use time-cost urgency math ("you've spent $X on therapy over Y years")
- Do not promise a discovery call "within 24 hours" unless that SLA is confirmed. Default: "typically within 1-2 business days"
- Do not use specific historical timeframes (e.g., "7,000 years") without sourcing. Use "thousands of years of ritual tradition"

**Tenant-specific prohibited patterns**: Load from `config/webinar-context.yaml` or tenant overlay. These override or extend the universal list.

## Q&A Duration

Target 8-12 minutes minimum. This topic demands it. Steal time from teaching blocks, not from Q&A. the operator stays on after the scheduled end for extended questions.

## Visual Standards

Full-bleed sections, primary teal `#14B8A6`, large typography, smooth scroll, mobile responsive. Gamma.app quality output.

## Credibility Stats

Load all credibility stats from tenant context (`config/webinar-context.yaml` or tenant overlay). **Never invent statistics.** If stats are unavailable, insert `[TENANT: credibility stats — provide source before presenting]` and flag to operator.

Borrowed proof sources (universally credible in the psychedelic healing space, verify current status before use):
- FDA Breakthrough Therapy designation
- Johns Hopkins / NYU / UCSF research programs
- RAND or peer-reviewed statistics on usage prevalence
- Global Drug Survey safety data

## Humanizer Requirement

Before presenting any webinar script, slide copy, or HTML output, run all spoken and on-screen text through the `humanizer` skill.

## Output

Save HTML presentations to `~/webinars/[filename].html`. Report the file path -- do not share generated HTML contents in chat.

## Dependencies

- `humanizer` -- AI pattern removal from webinar scripts and slide copy
- `brand-standards` -- voice and language compliance
