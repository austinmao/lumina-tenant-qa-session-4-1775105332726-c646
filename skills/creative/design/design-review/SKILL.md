---
name: design-review
description: "Run a 5-point design quality audit / review a page or component for accessibility, usability, consistency, content, and motion"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /design-review
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      os: ["darwin"]
---

# Design Review Skill

Conducts a structured 5-point design quality audit on a page, component, or screen. Evaluates accessibility, usability, visual consistency, content quality, and motion/interaction design. Produces a scored report with actionable fixes ranked by severity. Ported from Naksha-studio's /design-review and design-critique reference.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `brand_root` and `site_dir` from site context.
3. Read `<brand_root>/tokens/design-system.yaml` for design token references.
4. If a brand guide exists at `<brand_root>/brand-guide.md`, read it for brand-specific rules.

---

## Steps

### 1. Identify the review target

Accept from the user:
- **Target type**: page, component, section, or screen
- **Target identifier**: URL, file path, or component name
- **Context**: What stage is this (wireframe, mockup, implementation, production)?

### 2. Run the 5-point audit

Score each dimension 1-5 (1=critical failures, 5=exemplary). Each dimension has specific checkpoints.

#### Dimension 1: Accessibility (Weight: 25%)

| Checkpoint | Pass criteria | Severity if failed |
|---|---|---|
| Color contrast | All text meets WCAG AA (4.5:1 normal, 3:1 large) | Critical |
| Keyboard navigation | All interactive elements focusable in logical order | Critical |
| Screen reader semantics | Headings hierarchical (h1-h6), landmarks present, ARIA labels on icons | High |
| Touch targets | Minimum 44x44px on mobile, 8px minimum gap between targets | High |
| Alt text | All images have descriptive alt text; decorative images have `alt=""` | Medium |
| Reduced motion | Animations respect `prefers-reduced-motion` | Medium |
| Focus indicators | Visible focus ring on all interactive elements (not just outline: none) | High |
| Form labels | Every input has an associated `<label>` or `aria-label` | Critical |

#### Dimension 2: Usability (Weight: 25%)

| Checkpoint | Pass criteria | Severity if failed |
|---|---|---|
| Visual hierarchy | Primary CTA is most prominent element; scanning path follows F/Z pattern | High |
| Information density | No more than 7 items in a single group; white space > 30% of viewport | Medium |
| Error states | All form fields show validation errors inline with specific guidance | High |
| Loading states | Skeleton screens or spinners for async content; no layout shifts | Medium |
| Empty states | Empty lists/sections show helpful message + action | Low |
| Responsive behavior | Layout adapts cleanly at 320px, 768px, 1024px, 1440px breakpoints | High |
| Navigation clarity | User can reach any page in 3 clicks or fewer | Medium |
| CTA clarity | Each page has exactly one primary action; CTAs use action verbs | High |

#### Dimension 3: Visual Consistency (Weight: 20%)

| Checkpoint | Pass criteria | Severity if failed |
|---|---|---|
| Color usage | All colors from design tokens; no rogue hex values | High |
| Typography | All text uses defined font sizes, weights, line-heights from token scale | High |
| Spacing | All gaps/padding from the spacing scale (4px base) | Medium |
| Component reuse | Same data patterns use same component (no visual synonyms) | Medium |
| Border radius | Consistent radius from token scale across all components | Low |
| Icon style | All icons same style family (outline/filled), consistent size | Low |
| Shadow usage | Shadows from token scale; consistent elevation model | Low |
| Dark mode | If dark mode exists: all elements adapt correctly; no hardcoded colors | High |

#### Dimension 4: Content Quality (Weight: 15%)

| Checkpoint | Pass criteria | Severity if failed |
|---|---|---|
| Heading structure | Logical h1-h6 hierarchy; no skipped levels | High |
| Copy length | Headlines under 8 words; body paragraphs under 3 sentences | Medium |
| Microcopy | Buttons use verbs ("Get started" not "Submit"); error messages are helpful | Medium |
| Placeholder text | No lorem ipsum in production; all content is real or clearly marked as draft | High |
| Tone consistency | Copy matches brand voice (formal, casual, technical as defined in brand guide) | Medium |
| Link text | No "click here" or "learn more" as standalone link text | Medium |

#### Dimension 5: Motion & Interaction (Weight: 15%)

| Checkpoint | Pass criteria | Severity if failed |
|---|---|---|
| Entrance animations | Elements enter from consistent direction; duration 200-500ms | Low |
| Hover states | All interactive elements have visible hover feedback | Medium |
| Transition smoothness | No janky animations; GPU-accelerated properties only (transform, opacity) | Medium |
| Loading transitions | Content transitions smoothly from skeleton to loaded state | Low |
| Scroll behavior | Scroll animations trigger once; parallax is subtle (< 20% speed differential) | Low |
| Reduced motion | All animations disabled with `prefers-reduced-motion: reduce` | High |
| Micro-interactions | Meaningful feedback on user actions (button press, toggle, form submit) | Low |

### 3. Calculate scores

```
Weighted Score = (D1 * 0.25) + (D2 * 0.25) + (D3 * 0.20) + (D4 * 0.15) + (D5 * 0.15)
```

**Rating**:
- 4.5-5.0: Exemplary (ship with confidence)
- 3.5-4.4: Good (minor issues, shippable)
- 2.5-3.4: Needs work (address before shipping)
- 1.5-2.4: Significant issues (redesign required)
- 1.0-1.4: Critical failures (do not ship)

### 4. Generate fix recommendations

For each failed checkpoint, produce:
- **Severity**: Critical / High / Medium / Low
- **Current state**: What is wrong
- **Expected state**: What it should be
- **Fix guidance**: Specific code/design change needed
- **Estimated effort**: Quick fix (< 15 min) / Moderate (1-4h) / Significant (> 4h)

Sort all fixes by severity descending, then by effort ascending (quick wins first within each severity).

---

## Output

Write report to `memory/reports/design-review-<target>.md`:

```markdown
## Design Review — <target_name>
Site: <site_id> | Date: YYYY-MM-DD | Stage: <wireframe|mockup|implementation|production>

### Score Summary
| Dimension | Score | Weight | Weighted |
|---|---|---|---|
| Accessibility | X/5 | 25% | X.XX |
| Usability | X/5 | 25% | X.XX |
| Visual Consistency | X/5 | 20% | X.XX |
| Content Quality | X/5 | 15% | X.XX |
| Motion & Interaction | X/5 | 15% | X.XX |
| **Overall** | | | **X.XX/5** |

### Rating: <rating>

### Critical Issues (must fix)
[numbered list]

### High Issues (should fix)
[numbered list]

### Medium Issues (nice to fix)
[numbered list]

### Low Issues (polish)
[numbered list]

### Strengths
[what the design does well]
```

---

## Guidelines

- Be specific and actionable. "Color contrast is poor" is not helpful. "The #777777 body text on #f5f0ea background has 3.8:1 contrast ratio, below the 4.5:1 WCAG AA requirement" is.
- Do not invent issues to fill the report. If a dimension scores 5/5, say so.
- The review is objective. Reference specific design tokens, WCAG criteria, or established usability heuristics (Nielsen's 10).
- Never score below 1 on any dimension.
- If the target is a wireframe, skip Dimension 5 (Motion) and re-weight remaining dimensions proportionally.

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If the target cannot be found: ask user to provide the correct path or URL.
- If no design tokens exist: note in the report that consistency checks are against general best practices, not project-specific tokens.
