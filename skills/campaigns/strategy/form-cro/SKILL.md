---
name: form-cro
description: "Optimize registration forms, quiz flows, and application forms for higher completion rates"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /form-cro
metadata:
  openclaw:
    emoji: "clipboard"
    requires:
      env: []
      bins: []
---

# Form CRO

## Overview

Optimize the organization's forms — webinar registration, retreat applications, quizzes,
guide downloads, connection call booking, and email signups — for maximum
completion while respecting emotional safety. Every recommendation must account
for the fact that people may be sharing sensitive information about their mental
health journey.

## Core Principle: Every Field Has a Cost

Each additional field reduces completion rate:
- 1-3 fields: baseline completion
- 4-6 fields: 10-25% reduction
- 7+ fields: 25-50%+ reduction

For each field, ask:
1. Is this necessary before we can serve this person?
2. Can we learn this later (progressive profiling)?
3. Can we infer it from context?

---

## the organization Form Types

### 1. Webinar Registration (with Embedded Poll)

**Goal**: Maximize registrations while capturing audience research data.

**Required fields** (3 max):
- First name
- Email
- One research question (multi-select, see Poll-in-Registration below)

**Field order**: Name -> Email -> Research poll (optional, last)

**Button copy**: "Save My Seat" or "Reserve My Spot"

**Trust copy**: "Free. No replay paywall. Live Q&A included."

### 2. Retreat Application / Inquiry

**Goal**: Gather enough context to assess fit while honoring the sensitivity of what people share.

Longer forms are justified here — applicants expect depth. Use multi-step format.

**Step 1 — Basics** (low friction):
- Full name, email, phone (optional)

**Step 2 — Interest & context**:
- Which retreat are you interested in?
- What draws you to this experience? (open text)

**Step 3 — Background** (sensitive — see Emotional Safety):
- Relevant experience or preparation (open text, optional)
- Anything we should know to support your safety? (open text, optional)

**Step 4 — Logistics**:
- How did you hear about us?
- Preferred dates (if multiple offerings)

**Button copy**: "Submit My Application" or "Start the Conversation"

### 3. Quiz Flows (Multi-Step with Branching)

**Goal**: Engage, educate, and segment — then deliver a personalized result.

**Structure**:
- One question per screen
- Progress indicator ("Question 3 of 7")
- Back button always available
- Result anticipation copy on later screens ("Almost there — your results are being prepared")
- Branching logic: skip irrelevant questions based on prior answers
- Final screen collects name + email to deliver results
- Never require email before showing at least a partial result

**Question design**:
- Use image cards or large buttons, not small radio buttons
- 3-5 answer options per question (reduce decision fatigue)
- Warm framing: "There are no wrong answers — this helps us understand what matters to you"

### 4. Guide / Resource Download

**Goal**: Minimum friction. The guide is the value exchange.

**Fields**: Email only (single field + submit button)
- Optionally add first name if personalization is planned
- Never add phone, organization, or role fields

**Button copy**: "Send Me the Guide" or "Get Instant Access"

### 5. Connection Call Booking

**Goal**: Get someone on the calendar with minimal pre-questions.

**Fields**:
- Name, email (pre-filled if possible)
- Calendar widget (embedded scheduling tool)
- One optional question: "What would you most like to explore on our call?" (open text)

**Never require**: Phone number, detailed medical history, or multi-paragraph intake at this stage. Save depth for the call itself.

### 6. Email List Signup

**Goal**: Absolute minimum friction.

**Fields**: Email only (single field inline with submit button)
- No name field, no dropdowns, no checkboxes
- Button copy: "Join Us" or "Stay Connected"
- Trust copy below: "Weekly reflections on healing, connection, and ceremony. Unsubscribe anytime."

---

## Poll-in-Registration Pattern

Embed research questions (multi-select) into registration forms without hurting completion.

**Rules**:
1. Place research questions AFTER all required fields (name, email)
2. Mark research questions as optional — never block submission
3. Frame with purpose: "Help us tailor this session for you"
4. Use multi-select checkboxes, not open text (lower effort)
5. Limit to 4-6 options + "Other" with optional text field
6. One research question maximum per registration form

**Example research question**:
> What topics are you most curious about? (select all that apply)
> - Integration practices
> - Legal landscape
> - Scientific research
> - Personal healing journeys
> - Facilitator training
> - Other: ___

**Why this works**: Required fields come first (name, email = committed). The
optional poll feels like personalization, not data extraction. Completion rate
impact is minimal because the form already submitted the moment they filled
required fields.

---

## Multi-Step Quiz UX

1. **Progress indicator**: Show "Step X of Y" or a progress bar. Never hide how
   many steps remain.
2. **One question per screen**: Reduces cognitive load and creates a sense of
   momentum.
3. **Result anticipation**: On later screens, add copy like "Almost there —
   preparing your personalized results" to sustain motivation.
4. **Branching logic**: If an answer makes subsequent questions irrelevant, skip
   them. Shorter paths = higher completion.
5. **Back button always available**: People abandon when they feel trapped.
6. **Save progress**: If technically feasible, preserve answers on refresh or
   accidental navigation. At minimum, warn before leaving.
7. **Deliver value before gating**: Show at least a partial result or insight
   before asking for email. Full results can be gated.

---

## Emotional Safety in Forms

the organization's forms touch healing, transformation, and sometimes trauma. These
rules are non-negotiable.

### Language
- Use warm, human language — never clinical or institutional
- "Share what feels right" not "Please complete all required fields"
- "Your experience" not "Patient history"
- "What draws you to this work?" not "Reason for inquiry"

### Sensitive Information Handling
- **Never require** sensitive fields (medical history, substance experience,
  mental health context) at top-of-funnel forms (webinar reg, guide download,
  email signup)
- **Progressive disclosure**: Collect sensitive information only after trust is
  established — later in the funnel (application step 3, post-booking intake),
  not at first touch
- Mark all sensitive fields as optional with reassurance copy:
  "This information helps us create a safe experience for you. Share only what
  feels comfortable."
- Never use red error styling on sensitive fields — use gentle prompts instead

### Framing
- "There are no wrong answers"
- "This helps us support you" (explain why you are asking)
- "You can share as much or as little as you like"
- Never imply judgment about answers

---

## Field Ordering Principles

1. **Easy first**: Name, email — low cognitive cost, builds commitment
2. **Contextual middle**: Interest, preferences, logistics
3. **Sensitive last**: Health background, personal history, financial info
4. **Logical grouping**: Keep related fields together (all contact info, then
   all interest info, then all background info)
5. **Optional fields after required fields**: Never block progress with optional
   questions

---

## Progressive Profiling

Do not ask everything at once. Collect information across multiple interactions:

- **First touch** (signup/registration): Name + email only
- **Post-registration** (confirmation page or email): "What topics interest you
  most?" (multi-select)
- **Application stage**: Deeper background, experience, intentions
- **Post-booking intake**: Medical history, dietary needs, emergency contact

**Rule**: Each interaction should ask only what is needed for the current step
plus one optional enrichment question maximum.

---

## Error Message Patterns

Errors must be supportive, not punitive. People in a vulnerable mindset may
interpret harsh error messages as rejection.

**Email field**:
- Good: "Please enter your email so we can send your results"
- Bad: "Invalid email address"

**Required field left blank**:
- Good: "We need your name to save your spot"
- Bad: "This field is required"

**Phone format**:
- Good: "Could you double-check your phone number? We want to make sure we can reach you"
- Bad: "Invalid phone number format"

**General rules**:
- Position error messages directly below the field
- Never clear entered data on error
- Use warm amber/gold tones, not aggressive red, for error states on sensitive
  forms
- Focus the cursor on the first field that needs attention

---

## Mobile-First Defaults

All the organization forms must work on mobile as the primary experience:

- **Single-column layout** always (no side-by-side fields except first/last name)
- **Tap targets**: 44px minimum height for all interactive elements
- **Thumb-friendly positioning**: Primary actions in the bottom half of the screen
- **No horizontal scrolling**: Every element fits within viewport width
- **Appropriate keyboards**: `type="email"` for email, `type="tel"` for phone
- **Sticky submit button** on longer forms (visible without scrolling to bottom)
- **Autofill support**: Use standard `name`, `autocomplete` attributes so
  browsers can pre-fill

---

## Completion Rate Diagnostics

When analyzing a form with low completion:

1. **Where do people drop off?** Check field-level analytics if available.
   Common drop-off points:
   - Phone number fields (make optional or remove)
   - Open-text fields requiring long answers (shorten prompt or make optional)
   - Sensitive questions too early in the form
   - Confusing multi-select with too many options

2. **Mobile vs. desktop split?** If mobile completion is significantly lower,
   check tap targets, keyboard types, and layout.

3. **Error rate by field?** High error rates indicate confusing labels,
   over-strict validation, or wrong input types.

4. **Time to complete?** If high, the form has too many fields or unclear
   instructions.

5. **Start rate vs. completion rate?** Low start rate = value proposition
   problem. Low completion rate = form friction problem.

---

## Layout Best Practices

- **Labels**: Always visible above the field (never placeholder-only — they
  disappear on focus)
- **Placeholders**: Use for examples only ("e.g., maria@email.com"), not as labels
- **Help text**: Below the field, only when genuinely needed
- **White space**: Generous spacing between fields (16-24px minimum)
- **Visual hierarchy**: Form title and value proposition above; trust elements
  and privacy copy below the submit button
- **CTA button**: Full width on mobile, left-aligned with fields on desktop;
  high contrast with the background
- **Button copy**: Always action + outcome ("Save My Seat", "Get My Results",
  "Submit My Application") — never generic "Submit"
- **Post-submit**: Clear success confirmation with next steps ("Check your email
  for your guide" or "We'll be in touch within 48 hours")

---

## Steps

When asked to optimize a form:

1. **Identify the form type** from the six the organization types above.
2. **Assess current state**: How many fields? Which are required? What is the
   current completion rate? Where do people drop off?
3. **Apply the field cost principle**: For each field, justify its presence or
   recommend removing/deferring it.
4. **Check emotional safety**: Are sensitive questions placed appropriately? Is
   language warm and non-clinical? Are sensitive fields optional?
5. **Check field order**: Easy first, sensitive last, logical grouping.
6. **Check mobile experience**: Single column, tap targets, keyboard types,
   sticky submit.
7. **Review error messages**: Supportive, specific, positioned near the field.
8. **Review button copy and trust elements**: Action + outcome on button;
   privacy/trust copy near submit.
9. **Recommend progressive profiling**: What can be asked later instead of now?
10. **If multi-step**: Verify progress indicator, back button, branching logic,
    and result anticipation.

## Output

Deliver recommendations in this format:

### Form Audit
For each issue found:
- **Issue**: What is wrong
- **Impact**: Estimated effect on completion (High / Medium / Low)
- **Fix**: Specific recommendation
- **Priority**: P1 (do immediately) / P2 (next sprint) / P3 (test when ready)

### Recommended Form Design
- **Required fields**: Justified list
- **Optional fields**: With rationale for inclusion
- **Field order**: Recommended sequence
- **Copy**: Labels, placeholders, button text, trust copy
- **Error messages**: For each field
- **Layout notes**: Single-step vs. multi-step, mobile considerations

### Test Ideas
2-3 A/B test hypotheses with expected outcomes, specific to this organization's context.

---

## Questions to Ask

If the user has not provided enough context, ask:
1. Which form type is this? (registration, application, quiz, download, booking, signup)
2. What is the current completion rate (if known)?
3. Do you have field-level drop-off data?
4. What is the mobile vs. desktop traffic split?
5. What happens after someone submits this form?
