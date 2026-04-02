---
name: content-editing
description: "Review copy for voice consistency, grammar, brand compliance, and clarity"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /content-editing
metadata:
  openclaw:
    emoji: "✏️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Content Editing

Review copy for voice consistency, grammatical accuracy, brand compliance, and clarity. This is an evaluator skill -- it reviews content and provides specific revision requests. It does not generate original copy.

## When to Use

- Reviewing page copy, email copy, or any content for brand voice compliance
- Proofreading for grammatical accuracy and clarity
- Evaluating content against the brand voice guide and messaging rules
- Providing structured editorial feedback with severity levels

## Context Loading

Before reviewing any content:
1. Read `memory/site-context.yaml` to determine the active site
2. Read `<brand_root>/voice.md` for voice rules
3. Read `<brand_root>/messaging.md` for approved messaging lines
4. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

## Review Criteria

### 1. Voice Consistency
Does the content sound like the brand? Check against:
- Voice archetype alignment (is the correct archetype applied?)
- Tone consistency throughout the piece
- Pronoun usage rules (we/you/I patterns)
- Poet's rhythm (long flowing sentences + short declarative landings)

### 2. Grammatical Correctness
Standard grammar, punctuation, and syntax review:
- Subject-verb agreement
- Consistent tense
- Proper punctuation
- Clear antecedents
- Parallel structure in lists

### 3. Brand Compliance
Does the content follow brand rules?
- Language kill list enforcement (no prohibited words)
- Approved messaging alignment
- Reader positioning check (never positioned as broken)
- Substance language check (no specific substances in general audience content)
- CTA alignment with brand standards

### 4. Clarity
Can the target audience understand it on first read?
- No jargon without context
- Clear logical flow
- Appropriate reading level for the audience
- No ambiguous statements

## Issue Severity Levels

Every issue is tagged with a severity:

| Severity | Criteria | Examples |
|---|---|---|
| `must-fix` | Voice violation, factual error, brand-prohibited language | Kill list word used, medical claim, reader positioned as broken |
| `should-fix` | Awkward phrasing, passive voice overuse, unclear antecedent | Long passive construction, vague pronoun reference |
| `consider` | Style preference, alternative word choice | Stronger verb available, rhythm could be improved |

## Output Format

### Per-Page Editorial Review

```
## [Page Name]

**Overall assessment**: pass | revisions needed
**Summary**: [total issues] issues — [must-fix] must-fix, [should-fix] should-fix, [consider] consider

### Issues

1. **[severity]** — "[exact text quoted]"
   - Problem: [description]
   - Brand rule: [specific rule or grammar principle cited]
   - Direction: [suggested approach, not a replacement sentence]
```

### Clean Pass
"Editorial review complete. No issues found. Copy is brand-compliant and ready for production."

## Generator/Evaluator Separation

This is a core architectural principle:
- The Copywriter generates original content
- This skill evaluates and provides revision requests
- Revision requests provide direction, not replacement sentences
- If copy is missing entirely, flag the gap and route it to the Copywriter

Never generate original copy, headlines, taglines, or CTAs through this skill.

## Boundaries

- Never write original copy. Review and provide revision requests only.
- Never approve copy that violates the brand voice guide. If off-brand but no specific rule can be cited, flag as `consider` with reasoning.
- Never make final editorial decisions on ambiguous voice questions. Present options with brand guide citations and ask the user.

## State Tracking

- `editorialReviews` -- keyed by page slug: review date, issue counts by severity, status (`in-review` | `revisions-requested` | `approved`)
- `voiceDecisions` -- rulings on ambiguous voice questions with rationale (precedent for future reviews)
- `recurringIssues` -- patterns seen across multiple pages, flagged as systemic feedback
