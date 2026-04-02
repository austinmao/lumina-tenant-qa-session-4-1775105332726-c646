---
name: email-design-system
description: "Use when referencing the legacy marketing email design-system entrypoint."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /email-design-system
---

# Email Design System Compatibility

This legacy path points to the canonical email design system under `skills/engineering/email/email-design-system/`.

When working on shared templates, keep `templates/email/org-constants.ts` as the source for organization email, URL, and domain constants. The canonical component token reference remains the engineering email design-system skill.
