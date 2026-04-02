---
name: website-discovery
description: "Gather website-specific decisions before sitemap ideation — reads brand guide automatically, then asks only the questions the brand guide can't answer"
version: "1.1.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /website-discovery
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      os: ["darwin"]
---

# Website Discovery Skill

Reads `<brand_root>/brand-guide.md` to extract brand context automatically,
then asks only the website-specific questions the brand guide cannot answer.

Produces `docs/website/discovery-brief.md` for Blueprint to use as sitemap input.

---

## Step 1 — Read brand guide (no questions yet)

Read `<brand_root>/brand-guide.md` and extract:

| Field | Source in BRAND-GUIDE.md |
|---|---|
| Primary audience | ## Audience → Primary Audience + Emotional Reality |
| What they want | ## Audience → What They Want |
| What they fear | ## Audience → What They Fear |
| Primary CTA | ## CTA System → Primary CTA |
| Emotional sequence | ## Brand Foundation → Emotional Sequence |
| Target feeling | ## Brand Foundation → Emotional Sequence (last step: Alive) |
| Positioning | ## Positioning → Core Differentiator + Secondary Differentiators |
| What the organization is not | ## Positioning → What the organization Is Not |
| Voice guardrails | ## Voice And Tone → Guardrails |
| Words to avoid | ## Verbal Identity → Words To Avoid |

Do not ask the operator any of these — they are already answered.

---

## Step 2 — Ask only the website-specific questions

Ask these four questions in sequence. One at a time. No batching.

### Question 1 — Starting point

> "The brand guide gives me everything I need on audience, CTA, and positioning — I'll use that directly.
>
> One structural question before I propose anything: should the new site be built **starting from your existing page structure**, or should I **propose a fresh information architecture** using the old site only as a content inventory?
>
> Starting fresh often produces cleaner IA. Starting from the existing structure is faster and preserves institutional knowledge."

Record: `starting_point: existing | fresh`

---

### Question 2 — Must-have pages

> "Are there pages or sections you know must exist in the new site — things you'd feel the launch was incomplete without, regardless of what the audit found?"

Follow-up if short answer:
> "Any content from the old site you want to make sure doesn't get lost even if the page is restructured?"

Record: `must_have_pages[]`, `preserve_content[]`

---

### Question 3 — Gap confirmation

> "The audit identified 12 content gaps — pages that should exist but don't. I'll read through them now. Tell me which ones feel wrong or unnecessary, and whether there are any gaps the audit missed.
>
> [List the gaps from the audit: /about/team, /about/how-it-works, /about/mission, /plant-medicine (hub), /science, /safety, /integration, /legal, /retreats/colorado, /community/overview, /alumni, /press]"

Record: `confirmed_gaps[]`, `rejected_gaps[]`, `additional_gaps[]`

---

### Question 4 — Constraints

> "Any hard constraints? For example:
> - URLs that must stay exactly as they are (active campaigns, printed materials, external links)
> - Content that can't change (legal language, active contracts)
> - Offerings that are being retired or launched soon
> - Anything else that would affect how I structure the sitemap"

Record: `url_constraints[]`, `content_constraints[]`, `upcoming_changes[]`

---

## Step 3 — Write discovery brief

Write to `docs/website/discovery-brief.md`:

```markdown
# Website Discovery Brief — YYYY-MM-DD

*Produced by Blueprint via website-discovery skill.*
*Brand context auto-populated from <brand_root>/brand-guide.md.*
*Website-specific decisions confirmed by the operator.*

## Starting Point
[existing structure | fresh ideation]

## Brand Context (from BRAND-GUIDE.md — no interview needed)

**Primary audience:** High-functioning people who look capable on the outside and feel
disconnected, stuck, or over-controlled on the inside.

**What they want:** To feel fully alive, more connected, more authentic and free, to
trust the container, to experience real change that lasts.

**What they fear:** Losing control, unsafe facilitators, empty spiritual language,
overpromising, intense experiences without durable change.

**Primary CTA:** Book a Connection Call

**Emotional sequence:** Seen → Safe → Open → Connected → Alive

**Core differentiator:** Togetherness as the mechanism of transformation — not merely
a feature of the experience.

**Voice:** Uplifting, inspiring, expert, powerfully transformational — never hypey,
salesy, manipulative, or guru-ish.

## Website-Specific Decisions (the operator-confirmed)

**Must-have pages:**
[List from Question 2]

**Preserved content:**
[List from Question 2 follow-up]

**Confirmed gaps (from audit):**
[Subset the operator confirmed]

**Rejected gaps:**
[Gaps the operator said are not needed — with reason]

**Additional gaps (not in audit):**
[Any the operator added]

**Constraints:**
- URL constraints: [...]
- Content constraints: [...]
- Upcoming changes: [...]

## Approval
- [ ] the operator confirmed this brief is accurate before sitemap ideation began
```

Present the brief and ask:
> "Does this accurately capture everything? Any corrections before I propose the sitemap?"

Mark the approval checkbox only after the operator confirms.

---

## Handoff

After the operator confirms:
> "Discovery complete. Brief saved to docs/website/discovery-brief.md. Proceeding to sitemap ideation — building the IA around the brand guide's audience and conversion goals, using the audit as a content inventory."
