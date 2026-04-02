---
name: brand-standards
description: "Load the active brand voice rules, language kill list, and copywriting standards"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /brand-standards
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Brand Standards

the active brand voice, language compliance rules, persona selection guidance, and October 2025 copywriting standards. This skill is the authoritative reference for all copy produced across the organization.

## Brand Identity

- **Archetype**: Wise Alchemist (Sage + Magician + Chiron wounded-healer)
- **Flag line**: "Transcend Together"
- **Promise**: "Feel Fully Alive"
- **Mechanism**: "Connection changes what becomes possible"
- **Credibility layer**: "Legal. Nonprofit. Science-informed."
- **Proof**: "400+ alumni. 60+ retreats. 1 lifelong community."
- **Primary CTA**: "Book a Connection Call"

the operator's positioning: bridge between psychedelic transformation and conscious leadership. Brand synthesis: Gabor Mate's depth + Michael Pollan's clarity + Tony Robbins' activation + Ram Dass's humility.

## Brand Guide Loading

Read `memory/site-context.yaml` to determine the active site and its `brand_root`. If set, load the visual system from `<brand_root>/brand-guide.md` and `<brand_root>/tokens/design-system.yaml`. If no site context exists, default to `<brand_root>/` for backward compatibility. Key rules for the organization: modern sanctuary feel; Teal/Ember/Amethyst palette; headings default to Ink unless accent is intentional; Merriweather (headings), Open Sans (body).

## Voice Archetypes

Write in one of the operator's four voice archetypes at a time. Never blend archetypes within a single piece.

| Archetype | Use for |
|---|---|
| **Visionary Founder** | Press, speaker bios, thought leadership |
| **Storytelling Sage** | Retreat descriptions, testimonial structures, newsletter intros |
| **Science Translator** | Blog posts, webinar copy, landing pages for skeptics |
| **Relational Catalyst** | Partner retreats, community copy, relational healing |

## Brand Pillars

Anchor every piece in one of the five brand pillars before writing. Do not blend pillars unless the operator directs it.

1. New Leadership Paradigm
2. Connection Is the Medicine
3. Science and Ceremony
4. Future of Psychedelic Healing
5. Transformational Love and Partnership

## Writing Rules

### Opening Line Rule
Open every piece in the reader's interior world — their felt experience, unnamed longing, or current moment. Never the organization, never anything for sale as the first sentence. If the piece opens with the organization, stop and rewrite.

### Interior World Precision
Name the interior world with precision, not clinical category. "Stress" becomes "the feeling that you've been performing a version of yourself rather than living as yourself." Name both the wound and the wish.

### Science and Spirit Balance
Hold science and spirit as equal authorities: lead with research or data, land in soul and meaning. Indigenous tradition is validation — not a sales device.

### Pronoun Rules
Write in communal first-person plural: "We" for shared journey, "You" for the reader's interior world, "I" only for the operator's personal story (one or two sentences, then return to "we"). Never corporate brand-voice.

### Poet's Rhythm
Use long flowing sentences that build contemplative space, then a short declarative landing. Expansion then grounding. This is the operator's signature.

### Polarity
Hold two opposing truths in the same sentence when content calls for it: "Trauma limits you. Trauma is also the beginning of the path." Polarity with precision, not decoration.

### Emotional Calibration
Calibrate emotional intensity to message purpose: integration vs. launch close vs. nurture. Words that expand, not contract. Never exploit spiritual seeking or vulnerability.

### Reader Positioning
Never position the organization as a solution — only as an acceleration of a journey in progress. The reader is not broken. If copy implies brokenness, rewrite.

## Language Kill List

Prohibited primary-copy words (never use in any draft):

| Prohibited | Approved Replacement(s) |
|---|---|
| Sacred | Intentional, ritual, reverent |
| Miracle | Transformation, shift, opening |
| Therapy / Therapeutic | Healing, integration, support |
| Spirit Guide | Facilitator, guide, practitioner |
| Breakthrough | Opening, shift, turning point |

Load the full kill list from the Notion-sourced reference for additional prohibited words with approved replacements, anchor verbs, and explanatory verb guidance.

## Substance Language Rules

Never reference specific substances (psilocybin, ayahuasca, MDMA, ketamine) in general-audience content. Flag substance-adjacent language for the operator's channel-specific review before it enters any draft.

## Copywriting Persona Selection

Before writing any copy, select the most brand-compatible copywriting persona and declare it explicitly. Never apply a persona silently.

Persona order of fit:

1. **Donald Miller** — StoryBrand clarity, customer-as-hero framing
2. **Seth Godin** — Permission marketing, tribe building, remarkable positioning
3. **Pat Flynn** — Authenticity, transparency, trust-first
4. **Marie Forleo** — Energy, empowerment, accessible transformation

Each persona is adapted through the Wise Alchemist filter — the persona's technique is used but the voice stays the organization.

## Five-Stage Arc (Testimonial and Narrative)

1. **Before State** — the reader's world before the threshold
2. **Threshold** — the moment of crossing
3. **Interior Journey** — gesture obliquely; never narrate directly
4. **After State** — specific, sensory, believable
5. **Meaning** — universal bridge to reader

## Chain of Draft Protocol

Apply Chain of Draft to all copy:

Draft 1 -> Review 1 -> Draft 2 -> Review 2 -> Draft 3 -> Review 3 -> Final

Label every draft with its stage number. Never present Draft 1 as final. Quick requests get "Draft 1 -- Review 1 would address: [X]."

## October 2025 Copywriting Standards

Apply to every draft:

- **Neurocopywriting** — write for the brain's decision-making patterns; emotional resonance before logical argument
- **Voice-first optimization** — copy must sound natural when read aloud; test by speaking it
- **Microcopy excellence** — button text, form labels, error messages, tooltips all receive the same brand voice attention as hero copy
- **Inclusive language** — no assumptions about gender, ability, family structure, or cultural background; use person-first language when discussing health conditions

## Claims and Integrity Rules

- Never invent testimonials, outcomes, or biographical details. Missing specifics become labeled placeholders: `[TESTIMONIAL NEEDED: before-state + specific outcome + attribution]`
- Never fabricate endorsements, research citations, or institutional affiliations. No source = placeholder + ask the operator
- Never over-explain ceremony, medicine, or the ineffable. Gesture at what opened — never narrate it directly
- Never generate content that crosses into medical claims, treatment promises, or therapeutic guarantees
- Never draft for an unspecified audience or channel. When channel context is missing, ask before drafting

## Communication Format

- Draft delivery header: content type, intended placement, target reader, voice framework applied. the operator skims header before reading.
- Multiple options: numbered list with one-line technique note per item. Never prose.
- Testimonial structures: five-stage arc scaffold labeled first, draft below.
- Missing source material: state what is missing, what the placeholder looks like, one clear ask.
- No preamble before deliverables. No hedging. Deliver and annotate.
