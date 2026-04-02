---
name: ux-writing
description: "Write microcopy, form labels, error messages, tooltips, and onboarding text"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /ux-writing
metadata:
  openclaw:
    emoji: "✏️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# UX Writing

Write microcopy for user interfaces -- form labels, error messages, tooltips, empty states, confirmation dialogs, onboarding text, and navigation labels. This skill produces the words that guide users through the product experience, reducing friction and building trust at every interaction point.

## When to Use

- Writing form labels, placeholder text, and help text for a new form
- Creating error messages for validation failures, API errors, and edge cases
- Writing empty state messages (no results, first-time user, cleared data)
- Creating onboarding text (welcome screens, feature introductions, setup wizards)
- Writing confirmation dialogs (delete confirmation, submit confirmation, cancel warning)
- Labeling navigation items, buttons, and interactive elements
- Writing tooltips and contextual help text
- Reviewing existing microcopy for clarity, consistency, and accessibility

## Context Loading

Before writing any microcopy:
1. Read `<brand_root>/brand-guide.md` for voice and tone guidelines
2. Read the page specification or wireframe for the UI context
3. Read existing microcopy in the component library (`web/src/components/`) for consistency
4. Read `<brand_root>/content-system.md` for terminology decisions (if it exists)

## UX Writing Principles

### 1. Clarity First
Every piece of microcopy has one job: help the user understand what to do next. If the user has to think about what the text means, it has failed.

- Use plain language (grade 6-8 reading level)
- Front-load the most important information
- One idea per sentence
- Avoid jargon, abbreviations, and internal terminology

### 2. Brevity Without Sacrifice
Short is good. Unclear is never good. If cutting words makes the meaning ambiguous, keep the words.

- Button labels: 1-3 words ("Save", "Continue", "Add contact")
- Form labels: 1-4 words ("Email address", "Phone number")
- Error messages: 1 sentence, maximum 2
- Tooltips: 1-2 sentences maximum
- Empty states: 1-3 sentences

### 3. Actionable Language
Tell users what they can do, not what they cannot.

- Instead of: "You cannot submit without an email"
- Write: "Enter your email address to continue"
- Instead of: "Error: invalid input"
- Write: "Enter a valid email address (e.g., name@example.com)"

### 4. Consistent Terminology
Use the same word for the same concept everywhere. Never use "account", "profile", and "settings" interchangeably if they refer to different things.

Document terminology decisions:
| Concept | Use | Do not use |
|---|---|---|
| The event | retreat | program, workshop, event |
| The person | you | user, customer, client |
| Creating an account | sign up | register, create account, join |
| Accessing an account | log in | sign in, login (as a verb) |
| Removing access | log out | sign out, logout (as a verb) |

## Component-Level Guidelines

### Form Labels

```
Label: Email address
Placeholder: name@example.com
Help text: We'll send your confirmation here
```

Rules:
- Labels are always visible (never rely on placeholder text alone -- it disappears on focus)
- Labels use sentence case ("Email address" not "Email Address")
- Placeholder text shows the expected format, not a repeat of the label
- Help text explains why the information is needed or how it will be used
- Required fields: indicate with "(required)" text, not just an asterisk

### Error Messages

Structure: **What happened** + **How to fix it**

```
Good:  "Enter a valid email address (e.g., name@example.com)"
Bad:   "Invalid email"
Bad:   "Error 422: Validation failed for field 'email'"

Good:  "Password must be at least 8 characters"
Bad:   "Password too short"
Bad:   "Error: does not meet minimum length requirement"

Good:  "This email is already registered. Log in instead?"
Bad:   "Duplicate entry"
```

Rules:
- Never blame the user ("You entered an invalid email" implies fault)
- Never show system error codes or technical details
- Always include the fix (what the user should do next)
- Use the same tone as the rest of the UI (not suddenly formal or stern)
- For unexpected errors: "Something went wrong. Please try again. If this keeps happening, contact support."

### Empty States

Empty states are opportunities, not dead ends.

```
First-time empty state:
  Headline: "No contacts yet"
  Body: "Add your first contact to get started."
  CTA: [Add contact]

Search empty state:
  Headline: "No results for 'xyz'"
  Body: "Try a different search term or check for typos."

Cleared data:
  Headline: "All caught up"
  Body: "No new notifications. Check back later."
```

Rules:
- Always include a next step (CTA button, suggestion, or alternative)
- Use illustrations sparingly -- they should complement, not replace, the text
- First-time empty states should be encouraging, not apologetic
- Search empty states should be helpful (suggest alternatives)

### Buttons and CTAs

```
Primary actions:  "Save", "Continue", "Submit application", "Reserve your spot"
Secondary actions: "Cancel", "Go back", "Skip for now"
Destructive actions: "Delete contact", "Remove", "Unsubscribe"
```

Rules:
- Use verbs that describe the action ("Save changes" not "OK")
- Be specific ("Delete contact" not just "Delete")
- Primary buttons use confident language ("Continue" not "Try to continue")
- Destructive buttons use explicit language ("Delete this contact permanently")
- Never use "Click here" -- the button label IS the action

### Confirmation Dialogs

```
Destructive confirmation:
  Title: "Delete this contact?"
  Body: "This will permanently remove [Name] and all their data. This action cannot be undone."
  Primary: "Delete contact"
  Secondary: "Cancel"

Save/discard:
  Title: "Unsaved changes"
  Body: "You have unsaved changes. Do you want to save before leaving?"
  Primary: "Save changes"
  Secondary: "Discard"
  Tertiary: "Cancel"
```

Rules:
- Title states the action as a question
- Body explains the consequences
- Button labels match the action (never "Yes" / "No" -- too ambiguous)
- Destructive actions require the user to confirm the specific thing being deleted

### Tooltips

```
Good: "Last updated 3 hours ago. Updates sync every 6 hours."
Bad:  "This shows when the data was last updated."
```

Rules:
- Provide information the user cannot get from the UI alone
- Keep to 1-2 sentences maximum
- Do not repeat the label -- add new information
- Trigger on hover (desktop) and long-press (mobile)
- Never put essential information only in tooltips -- they are supplementary

### Onboarding Text

```
Welcome screen:
  Headline: "Welcome to the organization"
  Body: "Set up your profile in 3 steps. Takes about 2 minutes."
  CTA: "Get started"

Feature introduction:
  Headline: "New: Campaign analytics"
  Body: "See how your campaigns perform with real-time metrics."
  CTA: "See analytics" / "Maybe later"
```

Rules:
- Set expectations (time, number of steps)
- Focus on value, not features ("See how your campaigns perform" not "We added analytics")
- Always allow skipping or dismissing
- Do not overwhelm -- introduce one concept at a time

### Loading and Progress States

```
Loading: "Loading contacts..."
Saving: "Saving changes..."
Processing: "Setting up your account... This may take a moment."
Success: "Changes saved"
```

Rules:
- Use the present participle for ongoing actions ("Loading..." not "Load")
- Be specific about what is loading ("Loading contacts" not just "Loading")
- For long operations, set expectations ("This may take a moment")
- Success confirmations can be brief (toast or inline message)

## Accessibility in Microcopy

- Screen reader text for icons: provide `aria-label` text that describes the action, not the icon ("Close dialog" not "X")
- Link text: descriptive and unique ("View booking details" not "Click here" or "Learn more")
- Status messages: use `aria-live` regions to announce dynamic content changes
- Form errors: associate error text with the input via `aria-describedby`

## Output Format

Deliver microcopy as a structured list:
```
Component: [component name]
Context: [where it appears in the UI]
Copy:
  Label: "..."
  Placeholder: "..."
  Help text: "..."
  Error (empty): "..."
  Error (invalid): "..."
  Success: "..."
```

## Boundaries

- Never write marketing copy, landing page text, or email content. This skill is for interface text only.
- Never finalize microcopy without seeing the UI context (wireframe, screenshot, or component spec).
- Never use humor in error messages -- it undermines trust when something goes wrong.
- Never create new terminology without checking the existing terminology list.

## Dependencies

- `copywriting` -- brand voice standards that microcopy must follow
- `form-building` -- forms that consume the labels, help text, and error messages
- `ui-ux-design` -- wireframes and component specs that define the UI context
- `brand-voice-calibration` -- voice calibration for the specific tenant

## State Tracking

- `terminology` -- keyed by concept: approved term, rejected alternatives, context
- `components` -- keyed by component name: copy inventory (labels, errors, help text, empty states)
