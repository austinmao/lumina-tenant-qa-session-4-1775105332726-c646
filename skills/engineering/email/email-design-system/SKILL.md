---
name: email-design-system
description: >
  Reference for the organization email design tokens, React Email component
  patterns, and template structure rules. Load this skill when creating,
  reviewing, or modifying any HTML email template — including onboarding emails,
  marketing sequences, sales communications, or any transactional email. Use
  this when the operator asks to "create a new email template," "make sure an email
  matches the brand," "add a new template," or "review this email for consistency."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  author: acme-local
  openclaw:
    emoji: "✉️"
---

# Email Design System

## Overview

This is the single source of truth for the organization email design. All email
templates — regardless of which agent domain produces them (onboarding,
marketing, sales) — must conform to these tokens and structural rules. The
canonical reference implementation is:

```
templates/email/onboarding/RetreatGettingStarted.tsx
```

Read that file if you need to see a complete working example of every pattern
documented here.

---

## Template Locations

| Domain | Template directory | Render script |
|---|---|---|
| Onboarding / participant-prep | `templates/email/onboarding/` | `templates/email/render.ts` |
| Marketing | `templates/email/marketing/` | `templates/email/render.ts` |
| Sales | `templates/email/sales/` | `templates/email/render.ts` |

All domains share a single render script: `templates/email/render.ts`.
New templates go in the subdirectory that matches the sending agent's domain.
If a template is shared across domains, place it under `templates/email/shared/`
and import from there.

File naming convention: `PascalCase` matching the email's purpose.
Examples: `RetreatGettingStarted.tsx`, `WelcomeSequence.tsx`, `EnrollmentOffer.tsx`.

---

## Design Tokens

These values are extracted from `RetreatGettingStarted.tsx` and are authoritative.
Do not substitute colors, fonts, or spacing from external sources.

### Colors

| Token name | Hex value | Usage |
|---|---|---|
| `body-bg` | `#f5f0ea` | Page/`<Body>` background (warm off-white) |
| `surface` | `#ffffff` | Email card / `<Container>` background |
| `hero-bg` | `#faf7f2` | Hero or highlight section background |
| `header-footer` | `#1a1a1a` | Dark header bar and dark footer background |
| `text-primary` | `#1a1a1a` | All headings (h1, h2) |
| `text-body` | `#333333` | Paragraph text and list items |
| `text-muted` | `#777777` | Secondary / italic / fine-print within body |
| `text-footer` | `#aaaaaa` | Footer text and footer links |
| `text-footer-muted` | `#666666` | Footer fine print (smallest text in email) |
| `accent` | `#8b7355` | Warm brown — inline links, secondary button, eyebrow labels |
| `divider` | `#e8e0d4` | `<Hr>` section dividers |

### Typography

| Element | Font stack | Size | Weight | Line-height | Notes |
|---|---|---|---|---|---|
| Body default | Georgia, Times New Roman, Times, serif | — | — | — | Applied to `<Body>` |
| h1 | inherit (Georgia) | 28px | 700 | 1.3 | Section headline |
| h2 | inherit (Georgia) | 20px | 700 | default | Section sub-heading |
| Paragraph | inherit (Georgia) | 15px | 400 | 1.7 | Body copy |
| List item | inherit (Georgia) | 15px | 400 | 1.7 | 8px `paddingLeft` |
| Muted text | inherit (Georgia) | 13px | 400 | 1.6 | `fontStyle: italic` |
| Signature | inherit (Georgia) | 15px | 400 | 1.8 | `fontStyle: italic` |
| Eyebrow label | Helvetica Neue, Helvetica, Arial, sans-serif | 12px | 600 | — | `letterSpacing: 2px`, `textTransform: uppercase`, accent color |
| Button text | Helvetica Neue, Helvetica, Arial, sans-serif | 14px | 600 | — | `letterSpacing: 0.5px` |
| Footer text | Helvetica Neue, Helvetica, Arial, sans-serif | 12px | 400 | 1.6 | `text-footer` color |
| Footer muted | Helvetica Neue, Helvetica, Arial, sans-serif | 11px | 400 | 1.5 | `text-footer-muted` color |

The Georgia / serif stack is used for all reading copy. The sans-serif stack is used
only for UI elements: eyebrow labels, buttons, and footer attribution lines.

### Layout

| Element | Spec |
|---|---|
| Container max-width | 600px, centered (`margin: 0 auto`) |
| Container background | `#ffffff`, `padding: 0 0 40px` |
| Hero section | `padding: 40px 40px 8px`, `backgroundColor: #faf7f2` |
| Body section | `padding: 28px 40px 8px` |
| Logo header | `backgroundColor: #1a1a1a`, `padding: 28px 40px`, `textAlign: center` |
| Footer | `backgroundColor: #1a1a1a`, `padding: 32px 40px`, `marginTop: 20px`, `textAlign: center` |
| Divider (`<Hr>`) | `borderColor: #e8e0d4`, `margin: 0 40px` (inset, does not span full width) |

### Buttons

| Variant | Background | Text color | Border-radius | Padding | Margin | When to use |
|---|---|---|---|---|---|---|
| Primary | `#1a1a1a` | `#ffffff` | 4px | `12px 24px` | `4px 0 24px` | Main CTA — the highest-priority action in a section |
| Secondary | `#8b7355` | `#ffffff` | 4px | `12px 24px` | `4px 0 24px` | Supporting CTA — when two actions compete, or for form completions |

Use at most one primary button per section. If a section has two CTAs, make
one primary and one secondary. Do not use more than two buttons in a single
section.

### Logo

```
URL:  https://images.squarespace-cdn.com/content/v1/628ba13f70f05c064dcc79cc/05099b52-3538-47da-9a9d-2a4f356c1ce6/brand+Final+Logo+color.png?format=600w
Header size:  width="220" height="59"
Footer size:  width="120" height="32"
Alt text:     "[Organization name]"  (always — never blank)
```

The logo always appears in the dark header. It also appears centered in the
dark footer at the smaller size. Do not place the logo anywhere else in the
template body.

### Logo Linking Behavior

| Campaign state | Logo `href` | Rationale |
|---|---|---|
| Active event campaign | Event registration URL | Every element drives toward the single campaign destination |
| No active campaign | `https://[the organization's domain]` | Default brand destination |
| Between campaigns | Unlinked or homepage | Prevents stale campaign links |

During active campaigns, the header logo is a CTA surface — do not waste it on
a homepage link. Pass the event URL as a template prop (`eventUrl`); never
hardcode a campaign URL. Default `logoHref` to `"https://[the organization's domain]"`.

### Links

All inline links use `color: #8b7355` (accent) and `textDecoration: underline`.
Never use `#1a1a1a` or `#333333` for inline links — those are text colors.
Footer links use `color: #aaaaaa` (not accent).

---

## React Email: Structural Rules

These rules apply to every template in this project without exception.

### Required imports

```tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Img,
  Link,
  Preview,
  Section,
  Text,
} from "@react-email/components";
import * as React from "react";
```

Import only the components you use. Do not import unused components.

### Document skeleton

Every template must follow this exact outer structure:

```tsx
<Html>
  <Head />
  <Preview>{previewText}</Preview>
  <Body style={body}>
    <Container style={container}>
      {/* Logo header — always first */}
      <Section style={logoSection}>
        <Img src={LOGO_URL} width="220" height="59" alt="[Organization name]" style={logo} />
      </Section>

      {/* Content sections */}
      {/* ... */}

      {/* Footer — always last inside Container */}
      <Section style={footer}>
        {/* footer content */}
      </Section>
    </Container>
  </Body>
</Html>
```

### Component rules

- Use `<Text>` for all body copy. Never use raw `<p>` tags.
- Use `<Heading>` for h1 and h2 elements. Never use raw `<h1>` / `<h2>` tags.
- Every h2 section heading must include a relevant emoji prefix: `📅 Prep Calls`, `📋 Health Intake Form`, `📖 Recommended Reading`, `💬 Join Us on WhatsApp`, `✈️ Getting Here`, `💌 Questions? We're Here.`, etc. The emoji is part of the heading string, not a separate element.
- Use `<Button href={url}>` for all calls to action. Never use `<a>` tags for CTAs.
- Use `<Link href={url}>` for inline hyperlinks in body copy. Never use `<a>` tags.
- Use `<Hr>` for section dividers. Never use raw `<hr>` tags.
- Use `<Img>` for all images. Never use raw `<img>` tags.
- Use `<Section>` for all layout rows. Never use raw `<div>` or `<table>` tags.
- Use `<Container>` exactly once per template as the 600px wrapper.
- Use `<Preview>` exactly once — it controls the preview/snippet text visible in email clients before open.

### Inline styles only

React Email renders to static HTML. All styles must be declared as inline
`React.CSSProperties` objects passed via the `style` prop. Never use:
- CSS class names (`className`)
- CSS-in-JS libraries
- `<style>` blocks
- Tailwind classes in production templates (Tailwind is available as a dev dep but email clients strip embedded CSS)

Declare each style object as a typed constant at the bottom of the file:

```tsx
const paragraph: React.CSSProperties = {
  color: "#333333",
  fontSize: "15px",
  lineHeight: "1.7",
  margin: "0 0 16px",
};
```

### Props interface

Every template must export a typed props interface:

```tsx
export interface MyTemplateProps {
  firstName?: string;   // always optional with a sensible default
  // ...other variables
}
```

Provide defaults for all props so the component renders in a preview state
without any arguments.

### Preview text

`<Preview>` component renders 90-130 characters in the inbox preview pane. The
copywriting standard for preview text prose is 85-100 characters of meaningful
content (see `skills/marketing/copywriting` Preview Text Engineering section).
The `<Preview>` component may pad beyond the prose length to fill inbox space.
The prose must communicate the email's core value proposition. It is the first
thing subscribers read after the subject line.

### Template variables

Pass all dynamic values as props. Never hardcode participant names, dates, URLs,
or retreat-specific strings directly in JSX. The one exception is the logo URL
and permanent site URLs (`home.[the organization's domain]`, `[the organization's domain]`,
`info@[the organization's domain]`) which are organizational constants — import them
from `templates/email/org-constants.ts` (the `ORG` and `CONTACT` exports) rather
than hardcoding string literals in each template:

```tsx
import { ORG, CONTACT } from "../org-constants.js";
// Usage: ORG.homepage, ORG.eventsUrl, CONTACT.info, CONTACT.fromLabel
```

All canonical values (domain, URLs, email addresses) live in `config/org.yaml`
and are mirrored into `org-constants.ts` for TypeScript templates.

---

## Template Sections Reference

The following section types exist in the canonical template. Reuse them in
this order when applicable. Sections you do not need may be omitted.

| Section | Style object | Purpose |
|---|---|---|
| Logo header | `logoSection` | Dark header with centered logo. Always first. |
| Hero | `hero` (`hero-bg` background) | Opening message: eyebrow + h1 + greeting paragraph. Always immediately after the logo header. |
| Content sections | `section` | One section per distinct topic. Separated by `<Hr>`. |
| Footer | `footer` | Dark footer with small logo, org attribution, unsubscribe / legal text. Always last. |

### Eyebrow labels

Use an eyebrow label at the top of the hero section only (not in every content
section). The eyebrow conveys the context or emotional framing of the email:

```tsx
<Text style={heroEyebrow}>Welcome to the Journey</Text>
```

Style: 12px, 600 weight, 2px letter-spacing, uppercase, sans-serif, accent color.

### Signature block

End the final content section (before the footer) with a signature:

```tsx
<Text style={signature}>
  With Love and Respect,
  <br />
  Lumina
</Text>
```

---

## Deliverability Requirements

Every template must satisfy all of the following before it is considered
production-ready.

### Footer must-haves

The dark footer section must always contain:
1. Organization logo (120x32, centered)
2. Organization name and legal entity line:
   `[Organization name] · [Legal entity description from config/org.yaml]`
3. Website and contact email links
4. A context line explaining why the recipient is receiving this email
   (e.g., "You're receiving this because you're registered for {retreatName}."
   or "You're receiving this because you subscribed at [the organization's domain].")
5. For marketing / newsletter emails: a plain-text unsubscribe link or
   one-click list-unsubscribe mechanism. Omit for purely transactional
   emails (booking confirmation, health intake reminder) where the recipient
   has no option to opt out of required communications.

### 600px max-width rationale

600px is the industry-standard maximum for email templates. Wider layouts
break in Outlook, Gmail, and Apple Mail on mobile. The `<Container>`
`maxWidth: "600px"` must not be changed.

### Image alt text

Every `<Img>` must have a non-empty `alt` attribute describing the image.
Email clients commonly block images by default; the alt text is the only
content the recipient sees until they enable images.

### Plain-text fallback

React Email generates HTML only. When sending via Resend, include a `text`
field alongside `html` containing a plain-text version of the email. This
improves deliverability (spam filters check for a text part) and accessibility.

The plain-text version must include:
- Subject / headline
- All body copy, logically ordered
- All URLs written out in full (not anchor text)
- Footer attribution and unsubscribe URL

### Spam filter hygiene

- Avoid ALL-CAPS words in subject lines or body copy.
- Avoid excessive exclamation marks.
- Avoid spam trigger phrases ("FREE", "Act now", "Limited time").
- The from address display name must always include the organization name
  (`the organization <info@[the organization's domain]>`, not bare addresses).
- The reply-to address must always be a real monitored inbox
  (`lumina@[the organization's domain]`).

### Accessibility

- All links must have descriptive text. Never use "click here" or "learn more"
  as the only link text.
- Color contrast: body text `#333333` on white `#ffffff` passes WCAG AA.
  Do not introduce text colors that reduce this contrast.
- Muted text `#777777` on white is borderline for WCAG AA at small sizes.
  Use only for supplemental, non-essential information.

---

## Adding a New Template

Follow these steps exactly when adding a new template to any domain.

### Step 1 — Create the file

Create `<domain-templates-dir>/<TemplateName>.tsx`.
Copy the import block and document skeleton from `RetreatGettingStarted.tsx`.
Delete all content sections; keep logo header, hero skeleton, and footer.

### Step 2 — Define the props interface

Export a typed interface. Every variable injected at send time must appear here.
Provide safe defaults for all props.

### Step 3 — Write content sections

Add `<Section>` blocks for each distinct content area. Separate with `<Hr style={divider} />`.
Reuse the existing style constants from `RetreatGettingStarted.tsx`; copy them into
the new file verbatim rather than creating new style names for the same visual elements.

### Step 4 — Write the style block

Add a `// ── Styles ──` comment at the bottom of the file. Declare all style
objects as `React.CSSProperties` constants. Cross-reference the token table above
to confirm every color and size matches.

### Step 5 — Register in render.ts

Add the template to `templates/email/render.ts` so it can be invoked at send
time. Two additions are required in that file:

1. Add an import at the top of the template registry section:
   ```ts
   import MyNewTemplate from "./subdomain/MyNewTemplate.js";
   ```
2. Add an entry to the `TEMPLATES` object, choosing a kebab-case
   `templateName` string:
   ```ts
   "my-new-template": {
     subject: (props) => `Subject line here: ${props.someVar ?? "default"}`,
     component: MyNewTemplate as React.ComponentType<Record<string, unknown>>,
   },
   ```

The `templateName` value is what callers pass in the stdin JSON field
`templateName` to invoke this template at send time.

### Step 6 — Dry-run test

Set `"dryRun": true` in the render input JSON and run the script to verify:
- No TypeScript compilation errors
- Props substitute correctly (no `undefined` rendering as literal "undefined")
- Preview text is present and under 150 characters
- Footer contains org attribution and context line

### Step 7 — Review against the New Template Checklist

Run through every item in the checklist section below before declaring the
template ready for production send.

---

## New Template Checklist

Run through all items before any first live send from a new template.

### Design tokens
- [ ] All colors match the token table exactly (no approximations or close-but-different hexes)
- [ ] Georgia serif stack used for all body copy, headings, paragraphs
- [ ] Helvetica Neue sans-serif stack used for eyebrow label, buttons, footer text
- [ ] h1 is 28px / 700 weight; h2 is 20px / 700 weight
- [ ] Paragraph text is 15px / 1.7 line-height
- [ ] Button padding is 12px 24px; border-radius is 4px
- [ ] Logo uses the correct Squarespace CDN URL (not a local copy)
- [ ] Header logo is 220x59; footer logo is 120x32

### Structure
- [ ] `<Html>` → `<Head />` → `<Preview>` → `<Body>` → `<Container>` hierarchy is correct
- [ ] Logo header section is first inside `<Container>`
- [ ] Footer section is last inside `<Container>`
- [ ] All body copy uses `<Text>`, not `<p>`
- [ ] All CTAs use `<Button>`, not `<a>`
- [ ] All inline links use `<Link>`, not `<a>`
- [ ] All headings use `<Heading>`, not `<h1>`/`<h2>`
- [ ] No CSS class names anywhere; all styles are inline `React.CSSProperties`
- [ ] No `<div>` or `<table>` tags
- [ ] `<Container>` max-width is 600px

### Props and variables
- [ ] All dynamic values are props with sensible defaults
- [ ] No participant names, emails, or URLs hardcoded in JSX
- [ ] Org constants (`LOGO_URL`, footer `info@[the organization's domain]`) declared as module constants

### Deliverability
- [ ] Footer contains: org name + legal entity, website, contact email, context line
- [ ] Marketing templates include unsubscribe mechanism in footer
- [ ] Every `<Img>` has a non-empty `alt` attribute
- [ ] `<Preview>` text is present, 90–130 characters, meaningful
- [ ] Subject line has no ALL-CAPS words or spam trigger phrases
- [ ] From address includes display name (`the organization <...>`)
- [ ] Plain-text `text` field will be included in the Resend send payload

### Pre-send verification
- [ ] Dry-run completed with `"dryRun": true` — no TypeScript errors, no undefined values
- [ ] Rendered HTML reviewed visually (open in browser or email preview tool)
- [ ] the operator has approved the content before any live send

---

## Render Script Pattern

All templates in this project are rendered with `tsx` via a shared `render.ts`
dispatcher that accepts JSON on stdin. The canonical implementation is at
`templates/email/render.ts`.

The dispatcher reads a required `templateName` field from stdin JSON and routes
to the correct template component. The current `templateName` registry is:

| `templateName` value | Template file |
|---|---|
| `"retreat-getting-started"` | `templates/email/onboarding/RetreatGettingStarted.tsx` |

When a new template is created, add it to the `TEMPLATES` registry in
`templates/email/render.ts` alongside its import. See that file's inline
comments for the exact pattern.

Key behaviors to replicate:
- Read full stdin before parsing (handle streaming input)
- Support a `"dryRun": true` flag that logs recipients and shows an HTML preview
  without calling the Resend API
- Use `render()` from `@react-email/render` to produce the HTML string
- Send via `resend.batch.send()` in chunks of 100 (Resend batch limit)
- Include an `idempotencyKey` per chunk to prevent duplicate sends on retry
- On any batch error: log the error, push failed results, and continue to the
  next chunk — do not abort the entire send
- Output a final JSON summary: `{ sent: N, failed: N, results: [...] }`

Environment variables the render script reads (never hardcode these):
- `RESEND_API_KEY`
- `RESEND_TRANSACTIONAL_FROM` — full display-name format: `"the organization <info@[the organization's domain]>"`
- `RESEND_TRANSACTIONAL_REPLY_TO` — plain address: `"lumina@[the organization's domain]"`

---

## Node / Package Dependencies

The React Email templates depend on packages installed under `templates/email/`.
There is one shared `package.json` for all templates — no per-domain installs.

Before running the render script for the first time (or after a fresh clone):

```bash
cd templates/email && pnpm install
```

Required packages (already in `templates/email/package.json`):
- `react-email@4.0.10`
- `@react-email/components`
- `@react-email/render`
- `resend`
- `react`
- `react-dom`
- `tsx` (dev — for running `.ts` scripts directly)

Run the shared dispatcher from the repo root:

```bash
npx tsx templates/email/render.ts < /tmp/input.json
```

Or with environment variables set inline (as used in the participant-prep skill):

```bash
RESEND_API_KEY="$RESEND_API_KEY" \
RESEND_TRANSACTIONAL_FROM="$RESEND_TRANSACTIONAL_FROM" \
RESEND_TRANSACTIONAL_REPLY_TO="$RESEND_TRANSACTIONAL_REPLY_TO" \
  npx tsx templates/email/render.ts < /tmp/input.json
```

---

## Installation

This skill is workspace-scoped and shared across all agents in this repo.

Place at: `skills/email-design-system/SKILL.md`

No environment variables or binaries are required. This is a read-only
reference skill. It loads contextually when any agent creates or reviews
email templates.
