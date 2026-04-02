---
name: email-audit
description: "Audit an email template for technical compliance and strategy effectiveness"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /email-audit
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Email Audit Skill

Two-phase audit of an email template. Phase 1 checks technical compliance (HTML structure, rendering, accessibility). Phase 2 evaluates strategy effectiveness (subject line, CTA, copy persuasion, segmentation fit). Produces a weighted score and routes all issues to Forge (email engineer).

## Usage

```
/email-audit <path-to-template>
```

Example:

```
/email-audit templates/email/onboarding/WelcomeEmail.tsx
```

---

## Phase 1: Technical Compliance (50% weight)

### HTML Structure (15%)

- **DOCTYPE and lang attribute** — email has a valid HTML structure with `lang` attribute on `<html>`
- **Table-based layout** — email uses table-based layout for Outlook compatibility; flag CSS grid or flexbox used for structural layout
- **Inline styles** — critical styles are inlined; flag reliance on `<style>` blocks without inline fallbacks
- **Image dimensions** — all `<img>` tags have explicit `width` and `height` attributes
- **Alt text** — all images have descriptive `alt` attributes; flag empty or placeholder alt text
- **Link targets** — all `<a>` tags have `href` attributes; no `javascript:` or empty hrefs

Score this section 0-100.

### Rendering Compatibility (15%)

- **Dark mode support** — meta tag `<meta name="color-scheme" content="light dark">` present; CSS `prefers-color-scheme` media query present or colors work in both modes
- **Mobile responsiveness** — viewport meta tag present; media queries for max-width breakpoints; text readable without zooming at 320px
- **Font stack** — web-safe font stack declared; custom fonts have fallbacks
- **Max width** — email body constrained to 600px max-width
- **Preview text** — hidden preview/preheader text present after subject line

Score this section 0-100.

### Deliverability (10%)

- **Text-to-image ratio** — at least 60% text content; flag image-heavy emails
- **Unsubscribe link** — visible unsubscribe link present in footer
- **Physical address** — sender physical address present (CAN-SPAM compliance)
- **No spam trigger words** — flag known spam triggers in subject line or body (FREE, URGENT, ACT NOW, etc.)
- **Plain text version** — multipart email includes text/plain alternative

Score this section 0-100.

### Accessibility (10%)

- **Semantic role** — `role="presentation"` on layout tables
- **Color contrast** — text meets WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text)
- **Font size** — body text at least 14px; CTAs at least 16px
- **Link distinguishability** — links distinguishable by more than color alone (underline or other visual indicator)
- **Heading hierarchy** — if headings used, they follow logical order

Score this section 0-100.

---

## Phase 2: Strategy Effectiveness (50% weight)

### Subject Line & Preview (15%)

- **Length** — subject line 30-50 characters (mobile-friendly)
- **Personalization** — uses merge tags or personalization tokens where appropriate
- **Curiosity or benefit** — subject line creates curiosity, states a benefit, or both
- **Preview text alignment** — preview text complements (not repeats) the subject line
- **Spam score** — no all-caps, excessive punctuation, or spam trigger patterns

Score this section 0-100.

### CTA Effectiveness (15%)

- **Single primary CTA** — one clear primary call-to-action; secondary CTAs visually subordinate
- **CTA copy** — action-oriented verb + benefit (e.g., "Reserve Your Seat" not "Click Here")
- **CTA visibility** — primary CTA above the fold; button style with sufficient padding and contrast
- **CTA repetition** — primary CTA repeated at least twice for long emails
- **Landing page alignment** — CTA destination matches the promise in the email

Score this section 0-100.

### Copy & Persuasion (10%)

- **Opening hook** — first sentence creates engagement (question, story, surprising fact)
- **Benefit-focused** — body copy emphasizes benefits over features
- **Social proof** — testimonials, numbers, or credibility markers present where appropriate
- **Urgency/scarcity** — authentic urgency or scarcity element (if applicable to offer)
- **Voice consistency** — copy matches brand voice guidelines

Score this section 0-100.

### Segmentation Fit (10%)

- **Audience targeting** — content appropriate for the stated audience segment
- **Lifecycle stage** — email matches the recipient's position in the customer journey
- **Personalization depth** — dynamic content blocks or conditional sections for segments
- **Send timing** — recommended send time/day noted for the target segment

Score this section 0-100.

---

## Scoring

Calculate the overall audit score as a weighted sum:

| Section | Weight |
|---|---|
| HTML Structure | 15% |
| Rendering Compatibility | 15% |
| Deliverability | 10% |
| Accessibility | 10% |
| Subject Line & Preview | 15% |
| CTA Effectiveness | 15% |
| Copy & Persuasion | 10% |
| Segmentation Fit | 10% |

```
overall = (html * 0.15) + (rendering * 0.15) + (deliverability * 0.10) + (accessibility * 0.10) + (subject * 0.15) + (cta * 0.15) + (copy * 0.10) + (segment * 0.10)
```

**Score bands:**

| Score | Rating |
|---|---|
| 90-100 | Pass — ready to send |
| 75-89 | Pass with warnings — minor improvements recommended |
| 50-74 | Fail — remediation required before send |
| 0-49 | Critical — major rework needed |

---

## Output Format

Produce a structured audit report:

```
Email Audit: <template-path>
Date: <YYYY-MM-DD>
Overall Score: <score>/100 (<rating>)

=== Phase 1: Technical Compliance ===

[HTML Structure] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[Rendering Compatibility] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[Deliverability] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[Accessibility] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

=== Phase 2: Strategy Effectiveness ===

[Subject Line & Preview] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[CTA Effectiveness] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[Copy & Persuasion] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

[Segmentation Fit] <score>/100
  PASS/FAIL — <check>: <finding>
  ...

Blocking Issues:
  - <list or "None">

Recommended Actions:
  1. <highest priority>
  2. ...
```

Save the report to `memory/reports/email-audit-report.md`.

---

## Error Handling

- If the template file does not exist or path is invalid: report "Template not found at <path>" and stop
- If the file contains no HTML content (e.g., plain YAML or empty): report "No HTML content detected — cannot perform audit" and produce a partial report noting the issue
- If the template is a React Email `.tsx` file: audit the rendered output structure, not raw JSX

## Issue Routing

All issues identified by this audit are routed to **Forge** (email engineer, `agents/engineering/email-engineer`).

- Phase 1 (technical) issues: Forge owns implementation
- Phase 2 (strategy) issues: Forge coordinates with Quill (copywriter) for copy changes
- Do not attempt to fix issues directly — produce the report and hand off
