---
name: ux-writing
description: "Write microcopy, form labels, error messages, tooltips, and onboarding text"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Write UI microcopy that guides users. Every word in the interface matters.

## Principles
- Be concise (labels: 1-3 words, errors: 1 sentence, tooltips: 1-2 sentences)
- Be specific (not "Error occurred" but "Email address is already registered")
- Be helpful (suggest next action in every error message)
- Match brand voice (warm for the organization, not robotic)

## Common Patterns
- Form labels: noun ("Email address" not "Enter your email")
- Buttons: verb + object ("Create account" not "Submit")
- Empty states: explain + suggest action
- Loading states: set expectation ("Loading your dashboard...")
- Success messages: confirm + next step
