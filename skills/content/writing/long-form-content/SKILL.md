---
name: long-form-content
description: >
  Write long-form content end-to-end: research, outline, draft, edit, and
  optimize. Use when creating blog posts, guides, whitepapers, case studies,
  or any content piece over 1500 words.
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /long-form-content
metadata:
  openclaw:
    emoji: "scroll"
    requires:
      bins: []
      env: []
---

# Long-Form Content

## Overview

Create long-form content through a structured pipeline: topic research,
outline creation, first draft, substantive editing, and SEO/readability
optimization. This skill produces publication-ready content pieces (blog
posts, guides, whitepapers, case studies) with consistent quality. Every
piece goes through at least two revision passes before delivery.

## Content Quality Standards

- **No filler.** Every paragraph advances the reader's understanding or
  motivates action. Remove any sentence that could be deleted without losing
  meaning.
- **Specificity over generality.** Use concrete examples, data points, and
  named references instead of vague claims. "Studies show" is not specific
  enough — name the study or remove the claim.
- **Voice consistency.** Match the active brand voice throughout. Reference
  the brand guide (`brands/*/brand-guide.md`) for tone, vocabulary, and
  language constraints.
- **Structural clarity.** Use headings (H2/H3), bullet lists, and short
  paragraphs (3-5 sentences max) to support scanning. The reader should
  grasp the key takeaway from headings alone.

## Steps

1. **Receive brief.** Confirm the content type (blog, guide, whitepaper,
   case study), target audience, primary keyword/topic, desired word count,
   and publication timeline. If any of these are missing, ask before
   proceeding.

2. **Research.** Gather supporting material:
   - Review existing content in the corpus for related topics (avoid
     duplication and self-cannibalization).
   - Identify 3-5 authoritative sources to reference.
   - Note key statistics, quotes, or examples to include.
   - If SEO keywords are provided, review SERP intent and competing content.

3. **Create outline.** Produce a structured outline:
   - Title (working — may change after drafting).
   - Introduction hook (1-2 sentences summarizing the angle).
   - H2 sections with 2-3 bullet points each describing the content.
   - Conclusion with CTA.
   - Estimated word count per section.
   - Present outline for approval before drafting.

4. **Write first draft.** Following the approved outline:
   - Write in the brand voice.
   - Include all researched sources with proper attribution.
   - Write the introduction last (after the body is complete).
   - Target the specified word count (+/- 10%).
   - Save draft to `memory/drafts/YYYY-MM-DD-[slug].md`.

5. **Substantive edit.** Review the draft for:
   - Logical flow: does each section build on the previous?
   - Argument strength: are claims supported with evidence?
   - Audience fit: is the language appropriate for the target reader?
   - Redundancy: are any points repeated unnecessarily?
   - Missing content: are there gaps the outline covered but the draft skipped?
   - Apply revisions directly in the draft.

6. **Optimize.** Final pass for:
   - SEO: primary keyword in title, H2, first 100 words, and meta description.
   - Readability: Flesch-Kincaid grade level appropriate for audience
     (typically grade 8-10 for general audiences).
   - Formatting: consistent heading hierarchy, no orphan headings, lists
     formatted consistently.
   - CTA: clear next step for the reader at the end.
   - Meta description: 150-160 characters summarizing the piece.

7. **Deliver.** Present the final piece with:
   - Title and meta description.
   - Word count.
   - Primary keyword and secondary keywords used.
   - Sources referenced.
   - Recommended publication date (if time-sensitive content).

## Output

A **publication-ready content document** saved to `memory/drafts/` with:
- Title, meta description, and slug
- Full content body with headings and formatting
- Word count and readability score
- SEO keyword summary
- Source attribution list

## Error Handling

- If the content brief is incomplete: ask the operator for the missing
  elements before starting research.
- If no brand guide is available: ask the operator for tone/voice guidance
  or proceed with neutral professional tone, flagging the gap.
- If the topic duplicates existing content in the corpus: notify the operator
  and recommend either updating the existing piece or choosing a
  differentiated angle.
- If the requested word count is under 1500 words: recommend using the
  standard `copywriting` skill instead, which is optimized for shorter-form
  content.
