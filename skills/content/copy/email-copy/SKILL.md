---
name: email-copy
description: "Write email campaign copy — subject lines, preheaders, body, and sequences"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /email-copy
metadata:
  openclaw:
    emoji: "✉️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Email Copy

Write email campaign copy including subject lines, preheader text, body content, and multi-email sequences. This skill covers the prose and persuasion layer of email — not the HTML/TSX engineering (use `email-design-system` and Forge) or the send mechanics (use `resend` skill).

## When to Use

- Drafting email campaigns (welcome sequences, nurture sequences, launch sequences)
- Writing subject lines and preheader text
- Creating email body copy for marketing, onboarding, or transactional emails
- Developing multi-email sequences with strategic arc and timing

## Core Approach

### Brand-First Email Writing

Before writing any email copy:
1. Read `memory/site-context.yaml` to determine the active site
2. Load `<brand_root>/brand-guide.md` for voice and positioning
3. Load `brand-standards` skill for language kill list and persona selection
4. Select and declare the voice archetype for this email

All email copy follows the same brand standards as any other the organization content — the channel changes, the voice does not.

### Subject Line Rules

- Subject lines are the most important copy in the email. Spend proportionate time on them.
- Write 3-5 subject line options per email, each using a different angle (curiosity, benefit, story, urgency, personalization)
- Keep under 50 characters for mobile preview. Test by reading on a phone-width screen.
- Never use false urgency, misleading promises, or clickbait that the email body does not deliver on
- Apply neurocopywriting: the subject line should create an open loop that the email closes

### Preheader Text

- The preheader is the second subject line. It extends the subject line's promise — it does not repeat it.
- Keep under 90 characters. Front-load the compelling part.
- Never leave preheader blank — email clients will pull random body text.

### Body Copy Structure

- Open in the reader's interior world, never with the organization or the offer
- Follow the active brand writing rules: poet's rhythm (long flowing sentence then short declarative landing), communal "we," polarity with precision
- One CTA per email. Multiple CTAs split attention and reduce conversion.
- For nurture sequences: each email advances the reader one step on the journey. No email exists in isolation.

### Sequence Architecture

For multi-email sequences, define the strategic arc before writing individual emails:

1. **Email 1**: Connection — establish empathy and relevance
2. **Email 2**: Story — share a transformation narrative (five-stage arc)
3. **Email 3**: Value — deliver genuine insight or framework
4. **Email 4**: Social proof — testimonials and community evidence
5. **Email 5**: Invitation — present the opportunity with calm confidence

Timing defaults: Day 0, Day 2, Day 4, Day 7, Day 10. Adjust based on campaign urgency and audience warmth.

### Emotional Calibration by Email Type

| Email type | Emotional register |
|---|---|
| Welcome / onboarding | Warm, grounding, reassuring |
| Nurture | Contemplative, curious, gently challenging |
| Launch / enrollment | Confident, clear, urgency grounded in real capacity |
| Post-retreat / integration | Reflective, celebratory, community-forward |
| Re-engagement | Honest, non-guilt-inducing, value-first |

## Quality Gates

Before presenting any email copy for approval:

1. **Kill list scan** — no prohibited words (Sacred, Miracle, Therapy/Therapeutic, Spirit Guide, Breakthrough)
2. **Substance language check** — no specific substances in general-audience emails
3. **Reader positioning check** — reader is never positioned as broken
4. **the operator positioning check** — the operator is never positioned as guru
5. **CTA check** — single clear CTA per email
6. **Humanizer pass** — all copy runs through `humanizer` skill before presentation

## Chain of Draft

Apply Chain of Draft to all email copy: Draft 1 -> Review 1 -> Draft 2 -> Review 2 -> Draft 3 -> Final. Label every draft with its stage number.

## Output Format

For each email in a sequence:

```
## Email [N]: [Name]
- Subject: [subject line]
- Preheader: [preheader text]
- Send timing: Day [N]
- Voice archetype: [archetype]
- CTA: [action + destination]

[Body copy]
```

For subject line options:

```
1. [Subject line] — [technique: curiosity/benefit/story/urgency/personalization]
2. [Subject line] — [technique]
3. [Subject line] — [technique]
```

## Boundaries

- Email copy is a draft deliverable only. All publishing and sending routes through explicit approval.
- Never include real subscriber PII in any draft. Use `[FIRST_NAME]` merge tags.
- Never write copy that makes medical, therapeutic, or outcome-guarantee claims.
- Never hardcode retreat dates, pricing, or capacity numbers. Use placeholders and source from `airtable-retreats` skill.

## Dependencies

- `brand-standards` — voice rules, language kill list, persona selection
- `brand-review-gate` — compliance validation before approval
- `humanizer` — AI pattern removal from final copy
- `email-design-system` — design tokens for visual context (Forge implements)

## Note on Source Agent

This skill was absorbed from the `marketing/email` agent. The original agent used a generic SOUL.md template. This skill defines the email copy capability as specified in the Lumina OS hierarchy design, drawing from the brand-guardian agent's comprehensive copywriting knowledge to apply it specifically to the email channel.
