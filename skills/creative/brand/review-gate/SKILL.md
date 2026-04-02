---
name: brand-review-gate
description: "Review copy or content for the active brand compliance"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /brand-review-gate
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Brand Review Gate

Review any copy, content, or creative asset against the active brand standards. This skill enforces voice consistency, language compliance, and brand positioning rules before content reaches approval or publication.

## When to Use

- Before any copy is presented for approval
- When evaluating drafts from any agent (Quill, Atlas, Prism, or external)
- As a quality gate before Slack previews or the operator review

## Review Criteria

### 1. Voice Archetype Compliance

Every piece of content must be written in one of the operator's four voice archetypes. The review gate checks that the archetype is declared and consistently applied throughout the piece:

- **Visionary Founder** — press, speaker bios, thought leadership
- **Storytelling Sage** — retreat descriptions, testimonial structures, newsletter intros
- **Science Translator** — blog posts, webinar copy, landing pages for skeptics
- **Relational Catalyst** — partner retreats, community copy, relational healing

Blending archetypes within a single piece is a `must-fix` violation unless the operator has explicitly directed it.

### 2. Brand Pillar Anchoring

Every piece must be anchored in one of the five brand pillars:

1. New Leadership Paradigm
2. Connection Is the Medicine
3. Science and Ceremony
4. Future of Psychedelic Healing
5. Transformational Love and Partnership

Pillar blending requires the operator's explicit direction.

### 3. Language Kill List Enforcement

Apply the Notion-sourced language kill list to every draft. Prohibited primary-copy words:

- Sacred
- Miracle
- Therapy / Therapeutic
- Spirit Guide
- Breakthrough

Load `brand-standards` skill for the full kill list with approved replacements, anchor verbs, and explanatory verb guidance.

### 4. Opening Line Rule

Every piece must open in the reader's interior world — their felt experience, unnamed longing, or current moment. Never the organization, never anything for sale as the first sentence. If the piece opens with the organization, it fails the review gate.

### 5. Reader Positioning

The reader is never positioned as broken. Content never implies the reader needs rescue or repair. the organization accelerates a journey already in progress. If copy implies brokenness, flag as `must-fix`.

the operator is never positioned above the reader or as a guru dispensing from above. He is the one who made the crossing and holds the light for others.

### 6. Substance Language Gate

Any reference to specific substances (psilocybin, ayahuasca, MDMA, ketamine) in general-audience content is flagged as `must-fix`. Substance-adjacent language requires the operator's explicit channel-specific clearance before entering any draft.

### 7. Testimonial and Claims Integrity

- No invented testimonials, outcomes, or biographical details
- No fabricated endorsements, research citations, or institutional affiliations
- Missing specifics must become labeled placeholders: `[TESTIMONIAL NEEDED: before-state + specific outcome + attribution]`
- No source = placeholder + ask the operator

### 8. Medical and Therapeutic Claims

No content may cross into medical claims, treatment promises, or therapeutic guarantees. Flag any language that implies guaranteed healing outcomes as `must-fix`.

### 9. Copywriting Persona Declaration

Before writing any copy, the most brand-compatible copywriting persona must be selected and declared explicitly. Never applied silently. Persona order of fit:

1. Donald Miller
2. Seth Godin
3. Pat Flynn
4. Marie Forleo

Load `brand-standards` skill for per-persona selection rules and adaptation guidance through the Wise Alchemist filter.

### 10. October 2025 Standards

Apply October 2025 copywriting standards to every draft: neurocopywriting, voice-first optimization, microcopy excellence, and inclusive language. Load `brand-standards` skill for the full standards with examples and prohibited patterns.

## Review Output Format

Structure every review as:

1. **Header**: content type, intended placement, target reader, voice archetype applied, brand pillar anchored
2. **Kill list scan**: list any prohibited words found with line reference
3. **Voice consistency**: pass/fail with specific violations cited
4. **Positioning check**: reader positioning, the operator positioning, substance language
5. **Claims check**: testimonial integrity, medical claims
6. **Overall verdict**: `pass` | `revisions-needed` | `fail`
7. **Issues list**: numbered, with severity (`must-fix` | `should-fix` | `consider`)

## Five-Stage Arc Validation

For testimonial and narrative copy, validate the five-stage arc:

1. Before State
2. Threshold
3. Interior Journey (gesture obliquely — never narrate directly)
4. After State (specific, sensory, believable)
5. Meaning (universal bridge to reader)

## Chain of Draft Compliance

Verify that drafts are labeled with their stage number (Draft 1 / Draft 2 / Draft 3). Draft 1 must never be presented as final. Quick requests get "Draft 1 — Review 1 would address: [X]."

## Humanizer Requirement

All final copy must pass through the `humanizer` skill before presentation to the operator. Verify that the humanizer pass has been applied.

## Dependencies

- `brand-standards` — full language kill list, persona selection rules, October 2025 standards
- `humanizer` — AI pattern removal from final copy
