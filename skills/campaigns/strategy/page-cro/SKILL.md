---
name: page-cro
description: "Optimize landing pages, sales pages, and registration pages for higher conversion"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /page-cro
metadata:
  openclaw:
    emoji: "chart-up"
---

# Page Conversion Rate Optimization (CRO)

## Overview

Analyze any the organization marketing page and produce actionable recommendations to
improve conversion rate. Applies a 7-layer CRO framework tuned for healing,
transformation, and experience-based offers where trust and safety are the
primary conversion drivers (not convenience or price).

## Initial Assessment

Before analyzing, identify:

1. **Page type** (see Page-Type Guidance below)
2. **Primary conversion goal** — the single action the page exists to produce
3. **Traffic source** — where visitors arrive from (organic, paid, email, referral, social, direct)
4. **Target avatar** — which brand avatar (A1-A3, B1-B3, C1-C3 from `voice-calibration`) the page addresses

If any of these are unknown, ask before proceeding.

---

## 7-Layer CRO Analysis Framework

Analyze in this order. Every layer applies to every page type.

### Layer 1 — Value Proposition Clarity

Can a visitor articulate what this page offers within 5 seconds?

**Check for:**
- Is the primary benefit clear, specific, and differentiated?
- Is it written in the reader's language, not the organization's internal language?
- Does it name a real felt experience or interior longing — not a category like "wellness" or "healing"?

**Common issues on healing/transformation pages:**
- Too mystical — visitor cannot tell what they are being offered
- Too clinical — reads like a treatment protocol, not an invitation
- Trying to say everything (retreat + community + science + lineage) instead of the one thing that matters to this visitor right now

### Layer 2 — Headline Effectiveness

Does the headline open in the reader's interior world (`voice-calibration` V1)?

**The rule:** The first line names the reader's felt experience — not the product,
not the organization, not the retreat, not the modality. The hero section speaks to what
the reader is already feeling before they arrived at this page.

**Test:** Read the headline. Who does it name? If it names the organization, a retreat,
a date, a price, or a modality, it fails Layer 2.

**Strong patterns for the organization pages:**
- Name the interior wound: "You have everything you were told to want. And you are still waiting to feel it."
- Name the unnamed knowing: "Something in you already knows."
- Name the threshold: "You have been meaning to do this for a long time."

**Weak patterns (reject these):**
- Feature-first: "3-Day Psilocybin-Assisted Retreat in Jamaica"
- Brand-first: "[Brand name]: [Tagline]" (describes the brand, not the reader's experience)
- Generic wellness: "Transform Your Life Today"

### Layer 3 — CTA Strength and Placement

CTAs are invitations, not commands. They must pass `voice-calibration` register.

**Approved CTA language:**
- "Begin Here"
- "Book a Connection Call"
- "Take the Assessment"
- "Join Us"
- "Reserve Your Place"
- "Start Here"
- "Explore the Experience"
- "See If This Is Right for You"

**Rejected CTA language (never use):**
- "Buy Now"
- "Sign Up"
- "Submit"
- "Register Now"
- "Get Started" (too SaaS)
- "Claim Your Spot" (scarcity pressure)
- "Download Now"

**Placement rules:**
- Primary CTA visible above the fold
- Repeat CTA after each trust signal cluster (testimonial, objection answer, safety signal)
- Secondary CTA ("Have questions? Book a Connection Call") after objection-handling section
- Final CTA at page bottom, paired with an invitation question: "What would it mean to give yourself this?"

### Layer 4 — Visual Hierarchy

Does the eye flow naturally toward the action?

**Check:**
- Can someone scanning get the core message without reading body text?
- Is there clear H1 > H2 > body hierarchy?
- Do images support the emotional arc or distract from it?
- Is there enough white space — especially around CTAs and testimonials?
- Are the most important trust signals visually prominent, not buried?

**Common issues on healing/transformation pages:**
- Wall of spiritual text with no visual breaks
- Stock nature photos that add atmosphere but no meaning
- Competing elements: video, testimonial carousel, countdown timer, chat widget all fighting for attention
- Critical safety information (legality, medical screening) buried below fold

### Layer 5 — Trust Signals

Trust is the primary conversion driver for healing and transformation businesses.
Visitors are evaluating: "Is this safe? Is this legitimate? Will I be okay?"

**Required trust signal categories (check for presence and placement):**

1. **Testimonials with transformation arcs** — not "it was great" quotes.
   Each testimonial should contain: before state, the experience (oblique — gesture, don't narrate), after state, and what it meant. Name, photo, and context (profession, life stage) increase credibility.

2. **Credibility markers:**
   - Legal status (501(c)(3) nonprofit, legal jurisdiction)
   - Research citations or clinical trial references
   - Alumni count ("400+ alumni"), retreat count ("60+ retreats"), years operating
   - Facilitator credentials (training, experience, certifications)

3. **Safety signals:**
   - Medical screening process mentioned explicitly
   - Facilitator credentials and experience
   - Legal jurisdiction and compliance
   - Emergency protocols referenced (not detailed — just acknowledged)
   - "What to expect" transparency

4. **Media and press mentions** — logos or quotes from recognized outlets

5. **Community proof:**
   - Community size and engagement
   - Alumni quotes about post-retreat support
   - Integration program existence

**Placement:** Trust signals go near CTAs (to reduce friction at the decision point)
and after benefit claims (to validate them). The strongest testimonial goes above
the fold or immediately below the hero.

### Layer 6 — Objection Handling

The top objections for the target audience, in order of frequency:

1. **"Is this legal?"** — Address directly and early. Legal jurisdiction, nonprofit status, compliance framework. Do not bury this. A single clear sentence near the top removes the objection for the entire page visit.

2. **Safety fears** — Bad trip, losing control, health risks, "What if something goes wrong?" Address with: medical screening process, facilitator experience, safety protocols, and normalizing language ("A mix of readiness and nervousness is exactly the right way to arrive").

3. **"Is this for me?"** — Readiness uncertainty, worthiness doubt, "I'm not spiritual enough," "I haven't done enough therapy first." Address with: avatar-specific language, "You don't need to be ready — you just need to come," and testimonials from people who arrived uncertain.

4. **Price justification** — For experience-based offers, the value is invisible until after the experience. Address with: what is included (meals, facilitation, integration support, community access), comparison framing (cost of not changing vs. cost of the retreat), and alumni testimony about lasting impact.

5. **Partner/family concerns** — "How do I explain this to my spouse/family/employer?" Address with: normalizing language, partner retreat options, resources for conversations with loved ones.

6. **Medical contraindications** — "I'm on SSRIs," "I have a heart condition." Address with: clear mention of medical screening, invitation to a screening call, reassurance that the process exists to protect them.

**Check:** Are the top 3 objections addressed before the primary CTA? If not, the page has a conversion leak at the decision point.

### Layer 7 — Friction Points

Anything that slows, confuses, or creates doubt.

**Check for:**
- Forms with unnecessary fields (every field is a dropout point)
- Unclear next steps after CTA click — what happens when they submit?
- Broken or slow-loading elements
- Mobile experience issues (especially for pages shared via text/social)
- Jargon or insider language that a first-time visitor would not understand
- Ambiguous pricing (hidden costs, unclear what is included)
- No clear path back if the visitor is not ready ("not ready yet?" secondary path)
- Missing "What happens next" section after the CTA

---

## Page-Type Guidance

### Webinar Registration Page

- **Primary goal:** Register for the webinar
- **Hero:** Open in the reader's interior world (V1), not with the webinar title or date
- **Above the fold:** Headline (V1), one-sentence value statement, date/time, CTA ("Reserve Your Place")
- **Below the fold:** What they will learn (3 specific outcomes), presenter credibility, testimonial from past attendee, objection handling (legality, "is this for me?")
- **CTA language:** "Reserve Your Place" or "Join Us"
- **Friction watch:** Do not require more than name + email. Phone number is a dropout trigger on webinar pages.
- **Experiment ideas:** Test headline (interior world vs. outcome-focused), test with/without presenter photo, test countdown timer vs. no timer, test social proof ("237 people registered" vs. none)

### Free Offer Landing Page (quiz, guide, mini-course)

- **Primary goal:** Opt in for the free resource
- **Hero:** Name the question the reader is already asking themselves. The free offer answers that question.
- **Above the fold:** Headline, one-line description of what they get, CTA ("Begin Here" or "Take the Assessment")
- **Below the fold:** What the resource covers, who it is for, sample insight or preview, the organization credibility
- **CTA language:** "Begin Here," "Take the Assessment," "Start Here"
- **Friction watch:** Minimal fields (name + email only). Do not gate with phone number.
- **Experiment ideas:** Test quiz vs. guide format, test immediate access vs. email delivery, test with/without testimonial, test headline variations

### Paid Program Sales Page

- **Primary goal:** Apply, enroll, or book a call
- **Hero:** Open in the reader's wound (V1, E2 — specific felt experience, not category)
- **Structure:** Hero > Problem articulation (name the interior world) > Bridge (what if there were another way?) > The offer (what this program is) > What is included > Testimonials with transformation arcs > Objection handling (all 6 objections) > Pricing with value framing > Final CTA with invitation question
- **CTA language:** "Book a Connection Call," "Begin Your Application," "See If This Is Right for You"
- **Trust signals:** Heavy. Multiple testimonials, credibility markers, safety signals, facilitator bios.
- **Friction watch:** If the page ends at a form, keep fields minimal. If it routes to a call booking, make the calendar embed seamless.
- **Experiment ideas:** Test long-form vs. condensed version, test video testimonial vs. text, test pricing position (early vs. late), test with/without FAQ section, test "Who this is for / Who this is not for" section

### Retreat Information Page

- **Primary goal:** Apply or book a screening call
- **Hero:** Open in the reader's world, not with dates/location/price
- **Structure:** Hero > The experience (oblique, E3 — gesture, don't narrate) > What is included (logistics: location, meals, facilitation, integration) > Safety and screening > Testimonials > Facilitator bios > Dates and pricing > Application CTA
- **CTA language:** "Begin Your Application," "Book a Connection Call," "Reserve Your Place"
- **Trust signals:** Safety-heavy. Medical screening, facilitator credentials, legal status, emergency protocols, alumni count.
- **Friction watch:** Do not put dates/pricing above fold — the reader needs to want the experience before they evaluate logistics. Do not over-describe what happens in ceremony (E3).
- **Experiment ideas:** Test hero image (nature vs. community vs. ceremony-adjacent), test "What to expect" section position, test video walkthrough vs. photo gallery, test FAQ vs. inline objection handling

### Application / Inquiry Page

- **Primary goal:** Complete and submit the application
- **Hero:** Brief — one line of reassurance. "This is the first step. There is no wrong way to begin."
- **Structure:** Reassurance > What to expect from the process > Application form > "What happens next" section
- **CTA language:** "Begin Here," "Take the First Step"
- **Trust signals:** Light. Process transparency ("We review applications within 48 hours. A team member will reach out to schedule a call."), confidentiality statement.
- **Friction watch:** Every unnecessary form field is a dropout. Ask only what is needed for screening. Multi-step forms with progress indicators outperform single long forms. Save progress if possible.
- **Experiment ideas:** Test single-step vs. multi-step form, test with/without progress bar, test form field count (minimal vs. detailed), test reassurance copy variations

### Replay / Recording Page

- **Primary goal:** Watch the recording, then convert to next step (apply, book call, register for next event)
- **Hero:** Minimal — the visitor is here for the video. Do not obstruct.
- **Structure:** Video player (prominent, auto-play optional) > Key takeaways (for skimmers) > CTA for next step > Testimonials from live attendees > Related resources
- **CTA language:** "Book a Connection Call," "Join the Next Session," "Begin Here"
- **Friction watch:** Do not gate the recording behind a form if they already registered. Do not auto-play with sound. Ensure mobile video playback works.
- **Experiment ideas:** Test CTA position (below video vs. sticky sidebar), test with/without chapter markers, test post-video CTA overlay vs. below-video CTA

### Alumni / Community Page

- **Primary goal:** Deepen engagement, referral, or re-enrollment
- **Hero:** Speak to shared experience. "You know what this is. You have been here."
- **Structure:** Community welcome > Upcoming events/offerings > Alumni testimonials > Ways to stay connected > Referral invitation
- **CTA language:** "Join Us," "Invite Someone," "Explore What's Next"
- **Trust signals:** Community size, alumni stories, event photos (real, not stock)
- **Experiment ideas:** Test referral incentive vs. no incentive, test upcoming events prominence, test alumni spotlight format

### Founder Story / About Page

- **Primary goal:** Build trust and credibility, then route to a conversion page
- **Hero:** Open with the universal human experience the operator's story represents, not with the operator's bio
- **Structure:** The human story (V2 transformation arc: before > threshold > journey > after > meaning) > the organization's origin and mission > Credibility markers > Team/facilitator bios > CTA to explore offerings
- **CTA language:** "Explore the Experience," "Book a Connection Call"
- **Trust signals:** the operator's personal arc, nonprofit status, research partnerships, media mentions, facilitator credentials
- **Experiment ideas:** Test video story vs. written story, test story length (condensed vs. full arc), test CTA placement (mid-story vs. end only)

---

## Above-the-Fold Rule

The hero section names the reader's felt experience — not the product, not the
brand, not the logistics. This is non-negotiable across all page types.

**Test:** Cover everything below the fold. Can a visitor feel seen and curious
from what remains? If the above-fold content could belong to any wellness
company, it fails.

**Cross-reference:** `voice-calibration` V1 (Open in the Reader's World) and E2
(Name the Interior World with Precision).

---

## Psychology Anchoring Principles

Apply these when constructing page flow. Cross-reference `marketing-psychology`
skill for deeper treatment.

1. **Loss aversion** — Frame the cost of inaction ("What does another year of this feel like?") rather than the gain of action. Use sparingly and with care — never as manipulation, always as honest reflection.

2. **Social proof cascade** — Place proof near each decision point, not clustered in one section. The visitor re-evaluates trust at every scroll pause.

3. **Commitment and consistency** — Small yeses lead to large yeses. A quiz, a guide download, or a webinar registration before a retreat application reduces friction at the big ask.

4. **Authority transfer** — Research citations, facilitator credentials, and media mentions transfer authority to the offer. Place before the CTA, not after.

5. **Scarcity (honest only)** — If retreat seats are genuinely limited, state the number. Never manufacture false scarcity. "12 seats. 4 remaining." is honest. "Limited spots — act now!" is pressure.

6. **Reciprocity** — Give before asking. Free content (webinar, guide, quiz) creates reciprocity that lowers resistance at the paid offer.

7. **Processing fluency** — Simpler pages convert better. Reduce cognitive load: fewer fonts, fewer colors, fewer competing elements, shorter paragraphs, more white space.

---

## Steps

1. Identify the page type, primary conversion goal, traffic source, and target avatar
2. If any are unknown, ask before proceeding
3. Run the 7-layer analysis in order (Layers 1-7)
4. For each layer, note: current state, specific issue, recommended fix
5. Cross-reference CTA language against approved list (Layer 3)
6. Cross-reference headline against `voice-calibration` V1 rule (Layer 2)
7. Check all 6 objection categories against the page content (Layer 6)
8. Check trust signal categories against the page content (Layer 5)
9. Compile recommendations into the output format below

## Output

Structure recommendations as:

### Page Assessment
- Page type, conversion goal, traffic source, target avatar
- Current estimated conversion strength (weak / moderate / strong) with one-sentence rationale

### Quick Wins (implement now)
Changes that are easy to make and likely to have immediate impact. Each item: what to change, why, and the specific replacement copy or layout change.

### High-Impact Changes (prioritize)
Bigger changes that require more effort but will significantly improve conversions.

### Copy Alternatives
For headline, subheadline, and CTA: provide 2-3 alternatives with rationale. All must pass `voice-calibration`.

### Test Ideas
Hypotheses worth A/B testing rather than assuming. Organized by page section (hero, trust, objections, CTA).

### Layer Scorecard
Rate each of the 7 layers: pass / needs work / fail. One-sentence note per layer.

## Error Handling

- If page type is not in the list above: apply the 7-layer framework generically and note which page-type guidance was closest
- If target avatar is unknown: analyze for the broadest the organization audience (C1 — Quiet Crossroads Professional) and flag that avatar-specific optimization is available
- If the page contains substance-specific language in general-audience content: flag immediately as a compliance concern before continuing analysis

## Related Skills

- `voice-calibration` — CTA language validation, headline V1 check, register calibration
- `marketing-psychology` — deeper treatment of persuasion principles
- `transformation-story` — testimonial and story arc structure (V2)
- `brand-standards` — visual and verbal brand compliance
- `copywriting` — full copy rewrites (use page-cro for optimization of existing pages; use copywriting for net-new copy)
