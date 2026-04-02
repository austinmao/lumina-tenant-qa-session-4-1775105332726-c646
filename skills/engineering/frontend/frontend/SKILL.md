---
name: frontend
description: "Build a web page / create a landing page / update the website / build a frontend component"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /frontend
  - command: /build-page
  - command: /landing-page
metadata:
  openclaw:
    emoji: "🖥️"
---

# the organization Frontend Build Workflow

When any request involves building, updating, or designing a the organization web page or component,
the agents in this workflow MUST read both reference documents before doing any work:

## Required Reading (both files, every time)

1. `<brand_root>/tokens/design-system.yaml` — brand design system
   - CSS token values (colors, typography, spacing, radii)
   - Core brand system (flag line, promise, mechanism, credibility, proof, CTA)
   - Component brand specs (logo, button, card, badges)
   - Vocabulary rules and messaging guardrails

2. `docs/web/web-ref.yaml` — technical web implementation
   - Stack and deployment (Next.js 15, Vercel team scope `acme-org-team`)
   - Layout rules (max-widths, section padding, overflow-x handling)
   - Typography implementation (clamp values, line-heights)
   - Mobile responsiveness (breakpoints, hero mobile rules)
   - Image handling (sips compression, public/ directory map)
   - E2E testing config (port 3099, Playwright)
   - Contact and config (email, Typeform ID, Zoom URL)
   - Thank-you page rules
   - File write warning (use Bash heredoc, not Write/Edit tools)

## Agent Workflow

This is a two-agent workflow. Do NOT skip the design step.

### Step 1: Canvas (frontend/designer)
- Reads both docs above
- Produces ASCII wireframe + color/typography token table + responsive notes
- Presents to the operator for approval
- Does NOT write any code

### Step 2: Nova (frontend/engineer) — only after the operator approves Canvas spec
- Reads both docs above
- Implements components using Next.js 15 App Router + React 19 Server Components
- Uses only Bash cat heredoc for all file writes in web/ (see web-ref.yaml write_tool_warning)
- Runs E2E tests before declaring complete: `cd web && PORT=3099 npm run dev &` then `npx playwright test`
- Deploys only with explicit the operator confirmation: `npx vercel link --project web --scope acme-org-team --yes && npx vercel --prod --yes`

## Brand Guardrails (non-negotiable)

- All headings: Merriweather (--font-h)
- All body/UI: Open Sans (--font-b)
- Primary actions: btn-primary class (teal gradient pill, white text)
- No colors outside brand token system without the operator approval
- WCAG AA contrast on all text
- Logo always links to https://www.[the organization's domain]
- Contact email: info@[the organization's domain] (never austin@)
- Default top-level CTA language: `Book a Connection Call`
