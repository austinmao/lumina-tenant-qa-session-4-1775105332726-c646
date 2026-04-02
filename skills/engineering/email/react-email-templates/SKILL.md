---
name: react-email-templates
description: "Build a production HTML email template / create responsive email with dark mode and cross-client compatibility"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /email-template
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins: ["node"]
      os: ["darwin"]
---

# React Email Templates Skill

Generates production-ready HTML email templates using React Email: responsive layouts, dark mode support, cross-client compatibility (Gmail, Outlook, Apple Mail, Yahoo), inline CSS, and deliverability best practices. Ported from Naksha-studio's /email-template command.

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If missing: respond "No active site set. Run `/site <name>` first." and stop.
2. Read the email design system skill (`skills/engineering/email/email-design-system/SKILL.md`) for token references.
3. Read `templates/email/render.ts` to understand the existing render pipeline.
4. Verify `templates/email/package.json` exists (React Email dependencies).

---

## Steps

### 1. Gather template requirements

| Input | Required | Default |
|---|---|---|
| Template name | Yes | N/A |
| Template purpose | Yes | N/A (marketing, transactional, notification) |
| Content sections | Yes | N/A |
| Dynamic variables | No | `firstName` |
| CTA count | No | 1 primary |

### 2. Generate the template structure

Follow the email design system skeleton exactly:

```tsx
import { Body, Button, Container, Head, Heading, Hr, Html, Img, Link, Preview, Section, Text } from "@react-email/components";
import * as React from "react";
import { ORG, CONTACT } from "../org-constants.js";

export interface TemplateNameProps {
  firstName?: string;
  // ... all dynamic variables with defaults
}

export default function TemplateName({ firstName = "Friend" }: TemplateNameProps) {
  return (
    <Html>
      <Head />
      <Preview>{previewText}</Preview>
      <Body style={body}>
        <Container style={container}>
          <Section style={logoSection}>...</Section>
          {/* Content sections */}
          <Section style={footer}>...</Section>
        </Container>
      </Body>
    </Html>
  );
}
```

### 3. Apply cross-client compatibility rules

| Client | Constraints |
|---|---|
| **Outlook (Windows)** | Word rendering engine. No CSS Grid, Flexbox, or border-radius on `<td>`. Use nested tables for layout. Max 23 CSS properties per element. |
| **Gmail** | Strips `<style>` blocks. All CSS must be inline. No CSS variables. Class names stripped. |
| **Apple Mail** | Full CSS support. Dark mode via `@media (prefers-color-scheme: dark)`. |
| **Yahoo** | Limited CSS. No `:hover`. Background images require VML fallback. |
| **Samsung Mail** | Similar to Gmail constraints. Test at 320px width. |

### 4. Implement dark mode

React Email handles dark mode via the `@media (prefers-color-scheme: dark)` query. For each element:

| Element | Light mode | Dark mode |
|---|---|---|
| Body bg | `#f5f0ea` | `#1a1a1a` |
| Container bg | `#ffffff` | `#2a2a2a` |
| Text primary | `#1a1a1a` | `#e5e5e5` |
| Text body | `#333333` | `#cccccc` |
| Text muted | `#777777` | `#999999` |
| Accent | `#8b7355` | `#c9a96e` (lightened for dark bg) |
| Divider | `#e8e0d4` | `#3a3a3a` |

Add `data-ogsb` attributes for Outlook dark mode override prevention where needed.

### 5. Implement responsive behavior

| Breakpoint | Layout changes |
|---|---|
| > 600px | Full 600px container, desktop padding |
| 480-600px | Container fills screen, reduced padding |
| < 480px | Single column, stacked CTAs, smaller headings |

### 6. Validate deliverability

Checklist (auto-checked during generation):
- [ ] Preview text 90-130 chars, meaningful
- [ ] Footer has org name, legal entity, website, contact, context line
- [ ] Marketing templates have unsubscribe link
- [ ] Every `<Img>` has non-empty `alt`
- [ ] No ALL-CAPS words in subject/body
- [ ] From address includes display name
- [ ] All links have descriptive text (no "click here")
- [ ] Plain-text version guidance included

---

## Output

Write template to `templates/email/<domain>/<TemplateName>.tsx` and register in `templates/email/render.ts`.

Summary report to `memory/reports/email-template-<name>.md`:

```markdown
## Email Template — <name>
Site: <site_id> | Date: YYYY-MM-DD

### Structure
[section list with content slot descriptions]

### Cross-Client Notes
[any client-specific workarounds applied]

### Dark Mode
[color mapping applied]

### Deliverability Checklist
[pass/fail for each item]
```

---

## Guidelines

- Use `<Text>`, `<Heading>`, `<Button>`, `<Link>`, `<Hr>`, `<Img>`, `<Section>` from React Email. Never use raw HTML equivalents.
- All styles as `React.CSSProperties` objects at file bottom. No className, no CSS-in-JS.
- Container max-width 600px. Never change this.
- Maximum one primary CTA per section. Two CTAs per section require primary + secondary.
- All organizational constants from `org-constants.ts`, never hardcoded.
- Every emoji in h2 headings per design system rules.

---

## Error Handling

- No site context: prompt `/site <name>`.
- Missing email deps: instruct `cd templates/email && pnpm install`.
- Template name collision: ask user to rename or confirm overwrite.
