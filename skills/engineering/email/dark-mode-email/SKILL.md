---
name: dark-mode-email
description: "Build email templates that render correctly in dark mode across major email clients"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Handle dark mode rendering in HTML emails. Test across Gmail, Apple Mail, Outlook dark modes.

## When to Use
- Building new email templates
- Fixing dark mode rendering issues

## Key Techniques
- Use color-scheme: light dark meta tag
- Transparent PNGs for logos (avoid white backgrounds)
- MSO conditional comments for Outlook
- prefers-color-scheme media query (Apple Mail, iOS)
- Gmail forces dark: use !important overrides sparingly
