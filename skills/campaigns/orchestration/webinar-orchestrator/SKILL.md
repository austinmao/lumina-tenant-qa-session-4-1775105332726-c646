---
name: webinar-orchestrator
description: "Use when creating a webinar presentation through the full multi-agent pipeline from discovery through Vercel preview"
version: "1.0.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /webinar-orchestrator
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["vercel", "open", "bash", "curl", "jq", "node", "npm", "npx"]
      env: ["VERCEL_API_TOKEN", "CAMPAIGN_API_KEY", "CAMPAIGN_API_ENDPOINT"]
---

# Webinar Orchestrator

Coordinates Prism, Quill, Brand, Atlas, Canvas, and Nova across 8 stages to produce
a polished webinar slide deck (`~/webinars/[slug].html`) and publish it for review
via local browser + Vercel preview URL.

**Estimated total time**: 30–60 minutes depending on iteration cycles.

---

## Stage 1 — Discovery (Prism)

Activate Prism (webinar architect) context. Prism must read
`docs/webinar/reference/combined-webinar-ref.yaml` before proceeding.

Interview the operator with the following questions (ask all at once, wait for answers):

```
I'm starting the webinar creation pipeline. To build your presentation, I need:

1. Webinar topic / working title
2. Target audience (who is in the room?)
3. One Big Domino — the single belief that, if accepted, dissolves all other objections
4. Primary offer + price point being pitched
5. Webinar date, time (MT), and duration
6. 5–7 learning outcomes (what attendees leave knowing or able to do)
7. Key credibility anchors or social proof you want to use
8. Co-host or partner org (if any)
```

Save all answers to: `memory/drafts/webinars/YYYY-MM-DD-[slug]-brief.md`

---

## Stage 2 — Outline (Prism → the operator approval gate)

Prism generates a structured outline applying Perfect Webinar (Brunson) +
Masterclass Script DNA (Vishen):

**Outline must include:**
- Big Domino statement (the ONE belief)
- Section-by-section slide breakdown:
  - Slide number, section name, framework element, 1-sentence purpose
  - Secrets #1, #2, #3 with their specific false beliefs being broken
  - Stack slide sequence with value items
- Estimated slide count (target: 20–25)
- Estimated presentation duration

Save outline to: `memory/drafts/webinars/YYYY-MM-DD-[slug]-outline.md`

**Report to the operator:**
```
📋 Webinar outline ready: [Topic]

[Paste outline here]

🎯 Big Domino: [statement]
📊 [N] slides estimated | [~duration]

Reply "approve" to continue, or request specific changes.
```

**STOP.** Do not proceed to Stage 3 until the operator replies with explicit approval.
If the operator requests changes, revise the outline and re-present. Repeat until approved.

---

## Operator's Voice — Verbatim Lines That Work (use these exact phrases)

These are the operator's proven phrases from live delivery. Use verbatim in speaker notes and slide copy — do not paraphrase.

**Core thesis (state within first 5 minutes):**
> "A bad trip doesn't actually come from the medicine. It comes from a nervous system that doesn't feel safe."

> "No one can actually tell you that you're safe. You have to feel it yourself."

**Framework anchor — Plutchik's emotion wheel (required teaching element):**
> "Plutchik said that love is equal to safety plus joy. In order for you to feel love, you need to feel safe and feel happy. Safety is what allows us to breathe and go deeper into our own experience."

**Neuroplasticity metaphor — DMN reset (required for the science section):**
> "If you're going down the mountain and there are tracks laid, it's really hard to deviate from those tracks. But what if you could shake the snow globe and get that fresh powder? You'd be able to carve your new tracks. Psychedelic therapy is proven to reset the default mode network."

**Three-ceremony rationale (required for retreat overview):**
> "The first ceremony is like a handshake with the medicine." (orientation, not yet safe enough to go deep)
> "The second ceremony is where you've built familiarity — that's when people really heal the deep work around their inner traumas." (deepening)
> "The third ceremony: you've shed so many layers that you finally get to experience the fullness of who you truly are, often for the first time ever." (reveal — always add: "I can't promise this for everyone")

**CTA positioning — "moving toward" (required reframe before the close):**
> "Very often we run away from something — run away from fear, from anger, from abandonment. But what if we move towards something? What if we move towards the experience of self-love? What if we move towards the experience of wholeness? What if we move towards actually being able to breathe and enjoy this moment? That's a very different energy."

**Connection call framing (required on CTA slide speaker notes):**
> "The reason we begin with a connection call is simple: one honest conversation can create a lot of clarity about fit, timing, and what comes next."

**Close (final line before Q&A):**
> "The only thing that changes today is whether you take the first step."

---

## Offer Facts (use in all webinar copy — populate from org config)

**Awaken Together Retreat:**
- Price: **$5,995 (psilocybin) / $6,995 (ayahuasca) — all-inclusive** (lodging, all meals, ceremonies, preparation, integration)
- Non-profit: if the organization is a 508(c)(1)(a) private church, retreat investment is ~50% tax-deductible
- Sales call URL: `[configured connection call URL]` (surface copy should call this a Connection Call)
- CTA framing: "Book a Connection Call" (not "Apply" — it's a conversation first)
- Do not add artificial urgency incentives or countdown framing. If there is a real deadline or capacity note, state it plainly and without pressure.
- Payment plans available (discuss on the call)
- SSRIs: not typically contraindicated, but can blunt the experience ("more medicine may be necessary to have the same experience") — never imply "fine" or "no problem"; direct to screening call
- No known lethal dose, no physiological addiction

**Credibility stats (use these exact figures):**
- 650+ people facilitated (96% report it as the most transformative experience of their lives)
- 400+ alumni still actively engaged in community
- 60+ retreats facilitated
- 300+ five-star reviews
- 200+ video testimonials
- January 2026 retreat: 100% of participants reported most transformative experience of their lives
- the operator has spoken at TedX Boulder, Mindvalley
- Do NOT reference MAPS or Rick Doblin as credibility anchors. Use instead: FDA Breakthrough Therapy designation, Johns Hopkins / NYU / UCSF research programs
- the operator was an advisor to the Colorado legislature in support of the Natural Medicine Health Act (licensing/training measures)

**Pre-retreat required reading (always include in retreat overview slide):**
1. *Letting Go* by David Hawkins (emotional release framework)
2. *No Bad Parts* by Dr. Richard Schwartz (Internal Family Systems — IFS)
3. *The Mind Illuminated* by John Culadasa (meditation guide)
Framing: "These books are theory. The retreat is where the theory becomes embodied experience."

**Legal/structure explanation (required for Q&A prep and legitimacy slides):**
If the organization operates as a 508(c)(1)(a) private church — serving psilocybin as a sacrament under religious protections — use this analogy: "Just like the Catholic Church can serve wine to kids, we're legally allowed to serve psilocybin under a religious model." Core belief: every participant's subjective experience is equally valid; no doctrine imposed — the goal is to support each person in discovering their own deepest experience. Additionally, if the organization has licensed natural medicine facilitators under state law, include this as a legitimacy anchor.

**Retreat Dates (always fetch live from Airtable before building copy):**

Fetch upcoming retreat dates from Airtable before writing the webinar copy. Use the `airtable-retreats` skill or this query:
- Base: Journey Information (`app9JBuCaLgG6Yyps`)
- Table: All (`tblZ3frILITQbTSLT`)
- Filter: Start date > today, sorted ascending
- Fields: Journey Code, Start, End, Status
- If no future dates exist in this table, check the most recently viewed Journey bases or ask the operator for current dates

Include a **Retreat Dates slide** (after the Investment slide, before the CTA):
- Show 2–3 upcoming dates with availability status
- Mark any retreat with ≤ 2 spots as "⚠️ Almost full"
- Always note: "Groups capped by design — small cohorts only"
- CTA: "Drop your availability in the chat"

---

## Stage 3 — Copy (Quill)

Activate Quill (brand copywriter) context.

Quill writes all slide copy from the approved outline:

- Apply Chain of Draft per slide: Draft 1 (content) → Review (clarity + voice) → Final
- Voice archetype: Science Translator (clear, curious, evidence-grounded) unless outline specifies otherwise
- Use `[PLACEHOLDER]` for any statistic, testimonial, or result that needs real data
- Format: one section per slide with slide number, headline, body copy, speaker note

**Required structural elements for the webinar (use as defaults):**

| Element | Placement | What it is |
|---|---|---|
| Geography warm-up | Opening (before slide 1) | the operator asks "pop into the chat — where are you calling in from?" Builds community before content. |
| Plutchik emotion wheel anchor | Before the Three Secrets | "Love = safety + joy" — the single framework that maps all three secrets onto one emotional truth |
| Embodied moment (breath) | After origin story, before Three Secrets | "Close your eyes, take a slow breath in. Notice what this topic brings up for you in your body." 2–4 min. |
| Live curiosity demo | Between Secret 2 and Secret 3 | Volunteer exercise: the operator asks "What's that like being you right now?" then double-clicks twice. Replaces pattern-break. |
| 4 provider vetting questions | Secret 3 / Container slide | Required checklist: (1) How do you assess my medical situation? (2) How do you build my inner capacity before ceremony? (3) How do you build connection among participants? (4) How do you support integration? |
| "Moving toward" reframe | Just before offer reveal | Reframe from "running away from fear" to "moving toward self-love, wholeness, possibility" |
| Single CTA | CTA slide | `Book a Connection Call` — one clear next step, no competing asks |
| Connection call positioning | CTA speaker notes | "One honest conversation can create clarity about fit, timing, and what comes next" |
| Integration positioning | Integration/Secret 3 slide | Frame integration as where the real work happens — "grounding lessons from the experience back into daily life" |

**Slide Text Budget (enforced per slide type):**

| Slide type | Max body words | Notes |
|---|---|---|
| Hook / title | ≤40 | One arresting line, maybe two |
| Authority / credibility | ≤100 | Story beats, not bio bullets |
| State audience feelings | ≤60 | Short, resonant list |
| Origin story | ≤130 | Narrative flow; no explanations |
| Case study (testimonial) | ≤120 | P.A.R. arc only |
| Teaching / Secret | ≤120 | ONE concept per slide; split if needed |
| Connect the dots | ≤60 | Short — reader already has the parts |
| Offer / stack | ≤100 | Clarity over completeness |
| CTA / close | ≤50 | Command + consequence |

**Rule**: If a teaching slide exceeds 120 words, split it into two slides.
One concept per slide. Audiences listen to the operator — they must not be reading.

**Italic emphasis**: Use `<em>` on exactly 1–3 key phrases per slide.
The phrase that, if forgotten, makes the whole point collapse.

Save to: `memory/drafts/webinars/YYYY-MM-DD-[slug]-copy.md`

---

## Stage 4 — Copy Review (Brand agent)

Activate Brand agent context.

Brand agent reviews `memory/drafts/webinars/YYYY-MM-DD-[slug]-copy.md` against:

- Active brand voice: uplifting, inspiring, expert, powerfully transformational
- No fabricated statistics or unverifiable claims
- Consistent transformation arc: overwhelmed high-achiever → surrender → healing → restored purpose/joy
- Brand v2.0 language: `Transcend Together`, `Feel Fully Alive`, `Connection changes what becomes possible`, legal/nonprofit/science-informed credibility

**If issues found:**
- List specific slides and the issue (e.g., "Slide 12: claim needs [PLACEHOLDER]")
- Route back to Quill for revision
- Re-review until approved

**Brand approval message:**
```
✅ Brand review complete — copy approved.
```

---

## Stage 5 — Marketing Review (Atlas)

Activate Atlas (funnel architect) context.

Atlas reviews the brand-approved copy for conversion structure:

- **One Big Domino**: Is it clearly identified and sustained throughout every section?
- **Single offer**: No forking — exactly one CTA, one price point
- **Offer clarity**: Can a first-time visitor understand what they're buying in 10 seconds?
- **CTA strength**: Is the call to action specific, urgent, and low-friction?
- **Funnel persona match**: Does the copy match the identified target audience?
- **Epiphany bridges**: Are all three Secrets delivered as story + transformation, not information?

**If issues found:**
- List specific issues with slide references
- Route back to Quill for revision, Brand re-approves, Atlas re-reviews
- Repeat until Atlas approves

**Atlas approval message:**
```
✅ Marketing review complete — conversion structure approved.
```

---

## Stage 6 — Design (Canvas)

Activate Canvas (frontend designer) context.

Canvas produces a design spec for the HTML presentation based on the approved copy:

**Canvas must deliver:**

1. Section-by-section visual layout
   - Slide type: dark | light | teal-accent | full-bleed-image
   - Layout pattern: centered-hero | two-column | card-grid | quote-callout | stack-reveal
   - Background: specific CSS value (color, gradient, or class name)

2. Color token assignments per slide type (v2.0 — canonical: `<brand_root>/brand-guide.md`):
   - `h1`: `#121212` (--ink) on light slides, `#FFFFFF` on dark slides; use teal only for emphasis moments
   - Buttons/CTAs: bg `#14B8A6`, text `#FFFFFF` (--on-accent)
   - Body text: `#121212` (--ink, light bg) | `#e8e3dc` (dark bg)
   - Background dark: `#1a1a2e` | light: `#F7F7F7` (--surface-2) | ember accent: `#FF5E3A` for warmth/emphasis only (≤5%)
   - Gradient stops: `#0D9488` (--accent-mid)

3. Typography scale:
   - Hero h1: 3.5–4rem, weight 700
   - Section h2: 2.2–2.8rem, weight 600
   - Body: 1.1–1.2rem, line-height 1.7
   - Quote callout: 1.4rem italic centered

4. Mobile responsive breakpoints (375px, 768px, 1200px)

5. Interaction notes:
   - Progress bar fixed top
   - Navigation dots right side
   - Speaker notes toggle (N key)
   - Smooth scroll between sections

Save spec to: `memory/drafts/webinars/YYYY-MM-DD-[slug]-design-spec.md`

---

## Stage 6b — Design Review (Brand agent)

Brand agent reviews `memory/drafts/webinars/YYYY-MM-DD-[slug]-design-spec.md`:

- Brand color compliance (Tierra Teal usage consistent with brand guide)
- Typography hierarchy matches active brand standards
- No visual elements that conflict with the transformation brand identity
- Brand logo placement: header, light background variant

**If issues found:** Route back to Canvas for revision. Re-review until approved.

**Brand design approval message:**
```
✅ Brand design review complete — visual spec approved.
```

---

## Safety & Legitimacy Data (use verbatim — do not approximate)

This section contains verified statistics for the psilocybin credibility sequence. Use these exact figures.

**Global Drug Survey — Safety Profile:**
- 0.2% of psilocybin users required emergency medical treatment — the lowest rate of any substance surveyed
- Framing: "Among all substances tracked by the Global Drug Survey, psilocybin had the lowest rate of emergency treatment — 0.2%."

**RAND 2025 National Survey (most current as of 2026-03-05):**
- 11 million Americans used psilocybin in the past year
- 17.5% lifetime prevalence among U.S. adults
- Approximately 10 million Americans microdose psychedelics
- Psilocybin is the #1 most-used psychedelic in the U.S.
- Source: RAND Corporation, 2025 national survey

**Legal Jurisdiction Proof (do NOT pitch as alternatives — frame as legitimacy evidence only):**
- **Oregon**: Measure 109 passed 2020; regulatory framework launched 2023; approximately 10,000 clients served; 377 licensed facilitators as of 2026; first state in U.S. to legalize psilocybin therapy
- **Colorado**: Prop 122 passed Nov 2022 (58% vote); licensing began December 2024; 124+ licensed natural medicine facilitators statewide; the organization has licensed natural medicine facilitators and was among the earliest operating in the state
- Framing: "This isn't fringe. Oregon has served 10,000 people. Colorado just began licensing — the organization is among the first."

**Credibility Slide Architecture (required before Investment slide):**
Include a social proof credibility wall slide before the offer/investment slide with these anchors:
- 400+ alumni
- 60+ retreats facilitated
- 1 lifelong community
- 200+ video testimonials
- Legal + non-profit + licensed natural medicine facilitators in Colorado

---

## Stage 7 — Build (Nova)

Activate Nova (frontend engineer) context.

Nova implements the Canvas-designed, Brand-approved spec as a standalone HTML file.

**Output path:** `~/webinars/YYYY-MM-DD-[slug].html`

**Build requirements:**
- Single self-contained file (no external CDN dependencies — inline all CSS/JS)
- All Quill copy from `memory/drafts/webinars/YYYY-MM-DD-[slug]-copy.md` applied verbatim
- Full-bleed sections matching Canvas's design spec exactly
- Progress bar fixed at top (updates on scroll)
- Navigation dots on right (clickable, highlights active section)
- Speaker notes panel (toggle with N key, hidden by default)
- Smooth scroll with section anchors
- Mobile responsive at all Canvas-specified breakpoints
- WCAG AA compliant (contrast ratios ≥ 4.5:1, all interactive elements keyboard-accessible)
- 20–25 slides per approved outline structure

**Directory setup:**
```bash
mkdir -p ~/webinars
```

**Asset path rules (CRITICAL for web deployment):**

When the webinar is served via Next.js or any web server (not `file://`), relative filesystem paths break.

| Context | Correct path format |
|---|---|
| Brand logos | `/brand/logos/[brand]-[variant].svg` |
| Press/partner logos | `/press/[partner-name].png` |
| People/portrait photos | `/people/[filename].jpg` |
| Public images in `web/public/` | `/[filename]` (root-relative) |

**NEVER use**: `../../../assets/brand/logos/`, `../../assets/`, or any relative traversal path.
**Always use**: absolute root-relative paths starting with `/`.

**Required slide sequence for webinars (before offer):**

After the Three Secrets section and before the CTA:
1. **Credibility wall** (S22b pattern): 5-stat grid — 400+ alumni / 60+ retreats / 300+ ceremony hours / 250+ integration hours / Non-profit (508(c)(1)(a))
2. **Investment slide** (S23 pattern): value stack comparison table + non-profit badge
3. **Retreat dates slide** (S23b pattern): Singular hero offer (next upcoming retreat, ember/orange accent, "⚠ Only X Spots") + secondary list of other dates below or to the right. Never equal-grid all dates — singular hero drives higher conversion.
4. **Community + next steps slide** (S23c pattern): show how connection continues after the retreat; no artificial countdowns or fast-action stacks
5. **CTA slide** (S24): QR code + connection call URL

**Investment slide requirements:**
- Include a **value stack comparison table** showing what equivalent services cost separately vs. the all-inclusive price
- Include a **non-profit badge**: "508(c)(1)(a) Non-Profit — 50% Tax Deductible" — place in bottom-right or as a badge on the price block
- Current prices: $5,995 (psilocybin retreat, all-inclusive) / $6,995 (ayahuasca retreat, all-inclusive)
- Payment plans available — always note "discuss on the connection call"

**QR code requirements:**
- Format: inline SVG (path-based, `M1 1.5h7m...` stroke syntax via `qrcode` npm package or Python `qrcode` library)
- Do NOT use base64 PNG (`qrcode.toDataURL()`) — it can be truncated during file edits
- Encode: `[configured connection call URL]` (current route; surface copy should say Connection Call)
- CTA URL: `[configured connection call URL]` — NOT just `/start`
- Three sizes by placement:
  - CTA slide (hero moment): `width="150" height="150"`
  - Q&A slide (sidebar): `width="110" height="110"`
  - Closing/final slide: `width="80" height="80"`
- Wrap QR in white-background div for dark slides: `<div style="background:#fff;border-radius:8px;padding:8px;display:inline-block"><!-- SVG --></div>`
- Generation command (preferred):
  ```bash
  node -e "
  const qrcode = require('qrcode');
  qrcode.toString('[configured connection call URL]', {type:'svg',margin:1,width:150}, (err,svg) => {
    const start = svg.indexOf('<svg'); const end = svg.lastIndexOf('</svg>')+6;
    process.stdout.write(svg.substring(start,end));
  });"
  ```

---

## Stage 7b — TDD (MANDATORY — runs after every campaign build)

**This step is non-negotiable.** Every campaign that produces code artifacts (API routes, pages, email templates) MUST have tests written and passing before the pipeline is considered complete.

Invoke the `openclaw-tdd-engineer` Claude Code sub-agent (`.claude/agents/openclaw-tdd-engineer.md`) with:

```
Run TDD for the [slug] campaign. Write tests for every new code artifact produced in this pipeline:

For each new file in web/src/app/api/**:
  - Auth/validation cases (401, 400, 500)
  - Happy path (200 + side-effects verified)

For each new file in web/src/app/**/page.tsx:
  - All render states (driven by config/props)
  - Fail-safe (malformed input → graceful fallback, no crash)

For each new file in web/src/emails/*.tsx:
  - Renders without throwing
  - Required props present and rendered

TDD protocol: write tests first → confirm red → verify green → report count.
Working directory: /Users/luminamao/Documents/Github/openclaw/web
```

**Do not proceed to Stage 8 until all tests pass (npx vitest run — 0 failures).**

If any test reveals an implementation bug: fix the implementation, re-run, confirm green.

**Checkpoint (required before Stage 8):** After all tests pass, write the following file:

```
File: memory/drafts/webinars/YYYY-MM-DD-[slug]-tdd-complete.md
Content:
# TDD Complete: [slug]
Date: [today]
Tests before: [N]
Tests after: [N+M]
Failures: 0
vitest output: [paste last 5 lines of npx vitest run output]
```

Stage 8 MUST NOT begin until this file exists. If the file is absent, TDD has not been verified.

---

## Stage 8 — Publish for Review

**Pre-condition (HARD GATE):** Verify `memory/drafts/webinars/YYYY-MM-DD-[slug]-tdd-complete.md` exists. If absent, return to Stage 7b. Do not proceed.

After Nova confirms the file is written and the TDD checkpoint file exists:

**Step 1 — Local:**
```bash
open ~/webinars/YYYY-MM-DD-[slug].html
```
Opens in default browser for immediate local review.

**Step 2 — Vercel preview:**
```bash
vercel ~/webinars/ --prod=false --name=webinar-[slug]
```
Capture the preview URL from Vercel CLI output (format: `https://webinar-[slug]-[hash].vercel.app`).

If Vercel deploy fails, report the error and provide only the local file path.

**Report to the operator:**
```
✅ Webinar complete: [slug]

📊 [N] slides | ~[duration] presentation
🎯 Big Domino: [statement]
📚 Frameworks: Brunson Secrets #1-3 + Stack + Vishen Masterclass DNA

🌐 Local: ~/webinars/YYYY-MM-DD-[slug].html
🔗 Preview: [vercel_preview_url]

Agents involved:
- Prism: discovery + outline
- Quill: all slide copy
- Brand: copy review ✅ + design review ✅
- Atlas: conversion review ✅
- Canvas: design spec
- Nova: HTML build
```

---

## Stage 9 — Register Campaign in Admin Database

**Agent**: Atlas (campaign-api skill)
**Trigger**: Automatically after Stage 8 publish is confirmed
**Purpose**: Ensure every webinar is traceable in the admin panel at `/admin/campaigns`
**Approval gate**: None required — creating a `draft` status DB record is reversible and low-risk

### Steps

1. Extract `title` from the webinar brief at `memory/drafts/webinars/YYYY-MM-DD-[slug]-brief.md`
2. Set `topic` = webinar date/time string (e.g., `"Webinar — March 5, 2026"`)
   - Parse from the brief's event logistics section (date + format)
3. Set `campaign_type` = `"webinar"`

4. **Dedup check** — call GET first:
   ```bash
   curl -s -X GET "$CAMPAIGN_API_ENDPOINT/api/campaigns" \
     -H "Authorization: Bearer $CAMPAIGN_API_KEY" \
     -H "Content-Type: application/json" | jq --arg title "[TITLE]" --arg type "webinar" \
     '.campaigns[] | select((.title | ascii_downcase) == ($title | ascii_downcase) and .campaign_type == $type) | .id'
   ```
   - If an ID is returned → campaign already exists; skip creation; log "already existed (ID: [id])"
   - If no ID → proceed to step 5

5. **Create campaign** (only if dedup check returned empty):
   ```bash
   RESPONSE=$(curl -s -X POST "$CAMPAIGN_API_ENDPOINT/api/campaigns" \
     -H "Authorization: Bearer $CAMPAIGN_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{\"title\":\"[TITLE]\",\"topic\":\"[TOPIC]\",\"campaign_type\":\"webinar\"}")
   campaign_id=$(echo "$RESPONSE" | jq '.campaign.id')
   ```

6. **Log result** to `memory/logs/api-submits/YYYY-MM-DD.md`:
   ```
   [TIMESTAMP] Stage 9: Campaign "[TITLE]" registered. ID: [campaign_id]. Status: draft.
   ```
   On duplicate: `[TIMESTAMP] Stage 9: Campaign "[TITLE]" already existed (ID: [campaign_id]). Skipped creation.`

7. **On DB failure** (non-2xx response or curl error):
   - Log error to `memory/logs/api-submits/YYYY-MM-DD.md`: `[TIMESTAMP] Stage 9 ERROR: [error message]`
   - Send iMessage to the operator: `"Stage 9 failed for '[TITLE]'. Campaign not registered. Check memory/logs/api-submits/. Error: [error]"`
   - Do NOT mark Stage 9 as complete — leave for retry

8. **Notify the operator** on success via iMessage:
   ```
   Campaign "[TITLE]" registered in admin panel.
   ID: [campaign_id]
   Status: draft
   Admin: [configured admin base URL]/admin/campaigns/[campaign_id]
   ```

### Environment Requirements

- `CAMPAIGN_API_KEY` — Bearer token (stored in `~/.openclaw/.env`)
- `CAMPAIGN_API_ENDPOINT` — base URL (e.g., `[configured admin base URL]`)

### Notes

- Stage 9 runs automatically after Stage 8 — no user input required
- Assets (landing page, email, SMS) are NOT created here — that is the campaign-workflow's job
- Campaign starts in `draft` status and must be promoted manually or via campaign-workflow
- `CAMPAIGN_API_ENDPOINT` should be set to `[configured admin base URL]` for production

---

## Error Handling

| Condition | Action |
|-----------|--------|
| `VERCEL_API_TOKEN` missing | Skip Vercel deploy; deliver local file only; notify the operator |
| `vercel` CLI not installed | Skip deploy; suggest `npm i -g vercel`; deliver local file |
| the operator doesn't approve outline after 3 iterations | Stop pipeline; save current outline as draft; notify the operator |
| Any agent review fails repeatedly | Flag to the operator with specific issues; pause for human guidance |
| `~/webinars/` write fails | Try `/tmp/webinars/`; report fallback path |

---

## File Manifest

| Stage | Output file |
|-------|-------------|
| Stage 1 | `memory/drafts/webinars/YYYY-MM-DD-[slug]-brief.md` |
| Stage 2 | `memory/drafts/webinars/YYYY-MM-DD-[slug]-outline.md` |
| Stage 3 | `memory/drafts/webinars/YYYY-MM-DD-[slug]-copy.md` |
| Stage 6 | `memory/drafts/webinars/YYYY-MM-DD-[slug]-design-spec.md` |
| Stage 7 | `~/webinars/YYYY-MM-DD-[slug].html` |
| Stage 9 | `memory/logs/api-submits/YYYY-MM-DD.md` |
