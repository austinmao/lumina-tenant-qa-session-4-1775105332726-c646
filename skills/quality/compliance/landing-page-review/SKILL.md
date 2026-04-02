---
name: landing-page-review
description: "Review landing page for frontend quality, accessibility, and cross-device rendering"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /landing-page-review
metadata:
  openclaw:
    emoji: "🖥️"
    requires:
      bins: ["curl"]
      env: []
      os: ["darwin"]
---

## Frontend Code Quality

- Semantic HTML: verify proper heading hierarchy (one `<h1>`, sequential `<h2>`/`<h3>` nesting), landmark regions (`<header>`, `<main>`, `<nav>`, `<footer>`), list elements for any enumerated content
- No inline styles: all styling via CSS classes; flag any `style=""` attributes
- No deprecated HTML attributes: flag `align`, `bgcolor`, `border`, `cellpadding`, `cellspacing`, `valign`, `width`/`height` on non-media elements
- Image optimization: `width` and `height` attributes present, `loading="lazy"` on below-fold images, WebP or AVIF format preferred; flag JPEG/PNG where modern formats apply
- No console errors or warnings: use Playwright `browser_console_messages` to capture and review
- No mixed content: all resource URLs use HTTPS; flag any `http://` src or href on an HTTPS page

## Cross-Device Rendering

Use Playwright to capture screenshots at each combination below. Navigate to the target URL, resize to the specified viewport, then capture:

| Viewport | Width | Mode |
|---|---|---|
| Mobile | 375px | Light |
| Mobile | 375px | Dark |
| Tablet | 768px | Light |
| Tablet | 768px | Dark |
| Desktop | 1024px | Light |
| Desktop | 1024px | Dark |

For each screenshot verify:
- Responsive images scale correctly within container bounds
- No horizontal scrollbar present
- Body text is legible (minimum 16px effective size on mobile)
- Touch targets are at least 44x44px on mobile viewports

## Performance

- No render-blocking resources in `<head>`: scripts should carry `defer` or `async`; non-critical CSS should be loaded asynchronously
- Images have explicit `width` and `height` attributes to prevent Cumulative Layout Shift (CLS)
- Web fonts use `font-display: swap` or `font-display: optional`; avoid `font-display: block` on body fonts
- DOM depth: flag any node chain exceeding 15 ancestor levels
- Image file size: flag any image resource exceeding 500KB; recommend compression or next-gen format

## Accessibility (WCAG AA)

- Color contrast: normal text must meet 4.5:1 ratio; large text (18pt / 14pt bold) must meet 3:1; use contrast checker on primary text, secondary text, and placeholder text
- Keyboard navigation: tab through all interactive elements (links, buttons, inputs, modals); verify each is reachable and shows a visible focus indicator (not `outline: none` without replacement)
- Screen reader semantics: landmark regions present, all images have descriptive `alt` text (decorative images use `alt=""`), icon-only buttons have `aria-label`
- Form inputs: every `<input>`, `<select>`, and `<textarea>` has an associated `<label>` (via `for`/`id` pairing or `aria-labelledby`)
- Skip-to-content: a visually hidden `<a href="#main-content">Skip to content</a>` link must be the first focusable element in the DOM

## Content Quality

- Value proposition: the primary headline and subheadline must be visible above the fold without scrolling on all three viewports
- CTA visibility: at least one call-to-action button must be visible without scrolling on mobile (375px)
- Social proof: testimonials, partner/client logos, or quantified outcomes (e.g., "500+ participants") must appear on the page
- No broken images: all `<img>` elements return HTTP 200; no `alt` fallback text visible due to 404
- No placeholder content: flag any lorem ipsum text, placeholder images (`via.placeholder.com`, `picsum.photos`), or `[TODO]` markers
- Brand voice: defer all copy tone and language kill-list checks to the `brand-content-gate` skill; this skill does not re-implement brand rules

## Scoring

Each section is weighted toward an overall quality score (0–100):

| Section | Weight |
|---|---|
| Frontend Code Quality | 30% |
| Cross-Device Rendering | 25% |
| Performance | 15% |
| Accessibility | 15% |
| Content Quality | 15% |

Within each section, score pass/fail per check item. Section score = (passing checks / total checks) * 100. Multiply by weight and sum for the final score. Report the overall score and per-section scores in the output.

## Issue Routing

After the review, route each finding to the responsible agent:

- **Frontend code quality issues, rendering defects, performance regressions** → escalate to Nova (`agents/frontend/engineer`)
- **Content issues, brand voice, value proposition clarity, CTA copy** → escalate to Quill (`agents/marketing/copywriter`)
- **SEO title, meta description, structured data, canonical tags** → out of scope for this skill; trigger `seo-audit` skill separately

Include the target URL, the failing check, the affected viewport (if applicable), and the routed agent in each issue record.
