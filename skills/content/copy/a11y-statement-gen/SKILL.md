---
name: a11y-statement-gen
description: "Generate a WCAG 2.1 AA accessibility statement page for a website"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /a11y-statement-gen
metadata:
  openclaw:
    emoji: "♿"
---

## Overview

Generates an accessibility statement following the GOV.UK accessibility statement pattern. Covers conformance status, known exceptions, testing methodology, and a contact route for accessibility issues. Output is a Markdown document and a Next.js page component.

## Steps

### 1. Gather Details

Ask the user for:
- Site name and URL
- Conformance status: full / partial / non-conformant with WCAG 2.1 AA (default: partial — safest honest default)
- Known accessibility issues (optional — if unknown, use placeholder text)
- Date of last accessibility review
- Contact method for accessibility issues (email or form URL)
- Testing methodology performed (prompt: manual keyboard testing, screen reader testing, automated Axe scan, third-party audit)

If the user is unsure about known issues, set status to `partial` and use placeholder exceptions.

### 2. Determine Conformance Status Text

| Status | Statement |
|---|---|
| full | "This website is fully compliant with WCAG 2.1 AA." |
| partial | "This website is partially compliant with WCAG 2.1 AA, due to the exceptions listed below." |
| non | "This website is not compliant with WCAG 2.1 AA, due to the exceptions listed below." |

### 3. Generate Accessibility Statement Document

Write `docs/legal/accessibility-statement.md`:

---

# Accessibility Statement for [Site Name]

This accessibility statement applies to [Site URL].

## Our Commitment

We want as many people as possible to be able to use this website. For example, that means you should be able to:

- zoom in up to 300% without the text spilling off the screen
- navigate most of the website using just a keyboard
- navigate most of the website using speech recognition software
- listen to most of the website using a screen reader (including the most recent versions of NVDA, VoiceOver, and JAWS)

## Conformance Status

[Insert conformance status text from Step 2.]

### Known Accessibility Issues

[If partial or non-conformant, list each known issue:]

- **[Issue description]**: [Impact on users, e.g., "Users navigating by keyboard may not be able to complete the contact form without a mouse."] We plan to fix this by [planned date or "a future update"].

*If no known issues, write: "We are not aware of any specific accessibility barriers at this time. If you encounter a barrier, please contact us."*

## Technical Information

This website was built with the following technologies:

- HTML5
- CSS
- JavaScript (React/Next.js)

## Testing Methodology

This website has been tested using:

- [x] Manual keyboard navigation testing
- [x/] Screen reader testing (VoiceOver on macOS, NVDA on Windows) — [mark applicable]
- [x/] Automated scan using Axe DevTools — [mark applicable]
- [x/] Third-party accessibility audit — [mark applicable if done]

## Known Limitations

Pages generated dynamically (e.g., blog posts) may contain embedded content from third-party services (Calendly, YouTube, Stripe) that we do not fully control. We take reasonable steps to ensure these services meet accessibility standards.

## Feedback and Contact

We welcome your feedback on the accessibility of this site. If you experience any accessibility barriers, please contact us:

- Email: [contact email]
- [Or: Use our contact form at [URL]]

We aim to respond within 5 business days.

If you are not satisfied with our response, you can contact the [relevant enforcement body for the user's jurisdiction, e.g., Equality Advisory and Support Service in the UK, or equivalent].

## Assessment Approach

[Company name] assessed the accessibility of this website using:

- Self-evaluation
- [Third-party evaluation — include if applicable]

## Last Reviewed

This statement was last reviewed on [last review date].

---

### 4. Generate Next.js Page

Write `app/accessibility/page.tsx`:

```tsx
import fs from 'fs'
import path from 'path'

export const metadata = {
  title: 'Accessibility Statement | [Site Name]',
  description: 'Our commitment to WCAG 2.1 AA accessibility compliance.',
}

export default function AccessibilityPage() {
  return (
    <main style={{ maxWidth: 800, margin: '0 auto', padding: '2rem 1rem' }}>
      <h1>Accessibility Statement</h1>
      {/* Import and render docs/legal/accessibility-statement.md content here */}
      {/* Recommended: use next-mdx-remote or similar */}
      <p>[Render accessibility-statement.md content here]</p>
    </main>
  )
}
```

Add a comment instructing the user to render the Markdown content using their existing MDX pipeline.

### 5. Add Footer Link

Remind the user to add a link to `/accessibility` in the site footer alongside privacy and terms links.

## Output

- `docs/legal/accessibility-statement.md` — statement document
- `app/accessibility/page.tsx` — Next.js page placeholder

## Error Handling

- User cannot describe known issues → use partial conformance with `[PLACEHOLDER: describe any known barriers here]`
- Contact method not provided → insert `[REQUIRED: provide contact email or form URL for accessibility enquiries]`
- Jurisdiction not provided → omit the enforcement body reference; add placeholder comment
