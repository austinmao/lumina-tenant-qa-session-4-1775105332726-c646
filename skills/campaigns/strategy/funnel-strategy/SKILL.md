---
name: funnel-strategy
description: "Design conversion funnels and run CRO analysis for high-ticket offers"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /funnel-strategy
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Funnel Strategy

Design conversion funnels for high-ticket offers and run 8-pass CRO analysis on existing pages. This skill covers funnel architecture, persona selection, urgency calibration, and strategic analysis for retreat enrollments ($5k-$25k), mastermind applications, and webinar-to-retreat journeys.

## When to Use

- Designing a new funnel (webinar-to-retreat, application, VSL, launch sequence, tripwire, lead magnet, challenge, product launch)
- Running a CRO audit on an existing page or funnel
- Selecting and applying a funnel persona to a campaign
- Calibrating urgency language against real capacity data

## Funnel Personas

Select and declare which of the ten funnel personas to apply before beginning any funnel design. State reasoning in one sentence. Never blend personas silently mid-design. If the brief calls for a hybrid approach, name both personas and draw an explicit boundary between where each applies.

Available personas (select one per design):

1. **Jeff Walker (PLF)** — Product Launch Formula; sequential seed-launch-open pattern
2. **Ryan Deiss (CVJ)** — Customer Value Journey; 8-stage awareness-to-advocacy
3. **Russell Brunson (DotCom Secrets)** — Value ladder, tripwire-to-high-ticket
4. **Frank Kern (Intent-Based)** — Intent-based branding, results-in-advance
5. **Amy Porterfield (Webinar)** — Webinar-to-course conversion
6. **Dean Graziosi (Mastermind)** — High-ticket mastermind enrollment
7. **Stu McLaren (Membership)** — Membership and recurring revenue
8. **Todd Brown (E5)** — Unique mechanism marketing
9. **Pedro Adao (Challenge)** — Challenge-to-offer conversion
10. **Vishen Lakhiani (Masterclass)** — Education-forward enrollment

## 8-Pass CRO Analysis Framework

Apply all 8 passes to every page or funnel audit. Never deliver a partial audit. If a subset cannot be completed given available context, state which passes are incomplete and why.

### Pass 1: Page Intention / Awareness Level
- What is the page trying to achieve?
- What awareness level is the visitor at? (Unaware, Problem-Aware, Solution-Aware, Product-Aware, Most-Aware)
- Does the messaging match the awareness level?

### Pass 2: Information Architecture / Attention Ratio
- What is the attention ratio? (number of links / number of desired actions)
- Is the page focused or scattered?
- Does the information hierarchy guide the eye to the CTA?

### Pass 3: CTA Analysis
- How many CTAs are on the page? (one is ideal)
- Is the CTA language specific and benefit-driven?
- Is the CTA visible above the fold and repeated at natural decision points?
- Does the CTA match the visitor's awareness level?

### Pass 4: Value Proposition and Messaging
- Is the value proposition clear in the first 5 seconds?
- Does the headline address the reader's interior world, not the product?
- Is the messaging specific (numbers, outcomes) or vague?

### Pass 5: Persuasion Techniques
- What social proof is present? (testimonials, logos, stats)
- What urgency mechanisms are used? (Are they genuine?)
- What risk-reversal is offered? (guarantees, framing)

### Pass 6: Visual and UX Alignment
- Does the visual design match the brand system?
- Is the page mobile-first?
- Are there friction points in the user flow?

### Pass 7: Funnel and Flow Assessment
- What happens after the CTA? (thank-you page, email sequence, call booking)
- Is the post-conversion experience designed or abandoned?
- Are there re-engagement paths for non-converters?

### Pass 8: Overall Grade and Recommendations
- Grade: A-F on Clarity / Persuasion / Flow / CTA
- Prioritized recommendations: Quick Wins, Strategic Changes, Longer-Term Tests

## Urgency Rules

Use only genuine urgency grounded in real program structure: actual retreat spot counts, actual enrollment windows, actual application deadlines confirmed by the operator. Never fabricate countdown timers, artificial closing dates, or "only N spots left" language without confirmed capacity numbers.

When urgency language is needed but real numbers are unavailable, write the copy with a clearly labeled placeholder: "REQUIRES REAL CAPACITY DATA FROM AUSTIN BEFORE PUBLISH."

## High-Ticket Funnel Principles

- Never apply high-pressure tactics that contradict the Wise Alchemist archetype: no false scarcity, no fake countdown timers, no shame-based urgency, no pain-amplification that exploits spiritual seeking or psychological vulnerability
- Never position the reader as broken. The reader is already on the journey; the offer accelerates it
- Never invent testimonials, social proof, enrollment numbers, or retreat outcomes. Every specific claim either comes from confirmed source material or carries a clearly labeled placeholder
- Never make medical, therapeutic, or outcome-guarantee claims
- For high-ticket offers ($10k+), cold traffic funnels, or complex multi-step journeys, use extended thinking during Design and Validate stages

## Chain of Draft

Apply Chain of Draft to all funnel designs: Draft -> Review -> Refine -> Validate. Label each stage. Do not deliver a first draft as final without indicating it is Draft 1 awaiting review.

## Output Format

### Funnel Design Delivery
Lead with: funnel slug, target segment, persona applied and rationale, and draft stage (Draft 1 / Draft 2 / Final) before the design itself.

### CRO Audit Delivery
Present all 8 passes as labeled sections with a summary grade (A-F on Clarity / Persuasion / Flow / CTA) at the top. Follow the grade summary with the full 8-pass analysis and a prioritized recommendation list (Quick Wins -> Strategic Changes -> Longer-Term Tests).

### Funnel Persona Options
Present as a numbered list with one sentence per persona on why it fits or does not fit the brief. Never bury persona rationale in prose.

## Humanizer Requirement

Run all final written copy (page headlines, body copy, CTA text, funnel narrative) through the `humanizer` skill before presenting for approval.

## Dependencies

- `brand-standards` — language kill list, persona selection rules, October 2025 standards
- `humanizer` — AI pattern removal from final copy
- `airtable-retreats` — live retreat dates, pricing, seat availability (always fetch before drafting urgency copy)
- `senja` — testimonials from Senja.io by tag, rating, or type
- `photo-semantic-search` — funnel page section image selection

## State Tracking

Track the following per funnel:

- `funnelSlug` — short identifier (e.g., `spring-retreat-2026-webinar-funnel`)
- `funnelType` — webinar-to-retreat, application-funnel, VSL, launch-sequence, tripwire, lead-magnet, challenge, product-launch
- `personaApplied` — which of the 10 funnel personas governs this design
- `targetSegment` — journey stage and audience cluster
- `draftStatus` — ideation, draft-1, review-1, draft-2, review-2, validated, pending-approval, approved, live
- `croAuditGrade` — overall grade from 8-pass analysis (A/B/C/D/F), or null if not yet audited
- `substanceLanguageFlagged` — boolean: true if draft contains substance-adjacent language
- `urgencyDataConfirmed` — boolean: true only if the operator has provided real capacity/deadline numbers

Save funnel designs to `memory/drafts/funnel/YYYY-MM-DD-[slug].md`.
Save CRO audits to `memory/drafts/funnel/audits/YYYY-MM-DD-[slug]-audit.md`.
