---
name: paid-ads
description: "Create and optimize paid ad campaigns on Meta, Google, and YouTube for education-to-experience funnels"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /paid-ads
metadata:
  openclaw:
    emoji: "money"
---

# Paid Ads — Education-to-Experience Funnels

## Overview

Create, structure, and optimize paid advertising campaigns on Meta (Instagram/Facebook), Google Search, and YouTube for the organization's education-to-experience funnel: free offer to webinar to paid program to retreat. All ad copy must pass voice-calibration E1 (reader on journey, not broken), the brand kill list, and platform compliance rules for substance-adjacent content.

## Before Starting

Gather this context (ask if not provided):

1. **Campaign goal** — Awareness, webinar registrations, free offer downloads, retreat inquiries, alumni referral activation?
2. **Funnel stage** — Cold (never heard of the organization), warm (engaged with content/attended webinar), hot (visited pricing/applied), alumni?
3. **Budget** — Monthly spend and whether this is a new or scaling campaign.
4. **Offer** — What is the free offer, webinar topic, or program being promoted?
5. **Landing page** — URL or description of destination page.
6. **Existing data** — Pixel/conversion history, email list size, alumni count for lookalikes.
7. **Creative assets** — Available video (the operator speaking, retreat footage, testimonials), images, alumni quotes.

---

## Platform Selection

### Meta (Instagram / Facebook)

**Best for:** Demand generation, transformation story content, alumni social proof, retargeting.

**Use when:**
- Building awareness among people who do not yet know they are searching
- Running transformation story ads (alumni journeys, retreat footage, the operator speaking)
- Retargeting webinar viewers, page visitors, or email subscribers
- Budget is $1,500+/month (minimum for algorithm learning on Meta)

**Campaign types to use:**
- Conversions: Webinar registration, free offer download
- Lead Gen: In-platform lead forms for connection call booking
- Engagement: Social proof building with alumni content
- Traffic: Blog/content amplification for cold audiences

**the organization-specific note:** Meta's visual-first format is ideal for retreat imagery, ceremony-adjacent nature footage, and short-form alumni testimonial clips. Use carousel ads for transformation arcs.

### Google Search

**Best for:** Capturing existing intent from people actively searching.

**Use when:**
- Targeting high-intent queries: "psychedelic retreat," "psilocybin retreat legal," "plant medicine retreat US," "ayahuasca retreat near me"
- Targeting readiness queries: "midlife crisis retreat," "burnout recovery program," "grief retreat," "personal transformation retreat"
- Targeting research queries: "psilocybin therapy research," "psychedelic healing science," "legal psychedelic experiences"
- Budget is $1,000+/month (minimum for Search with competitive wellness keywords)

**Campaign types to use:**
- Search: Keyword-targeted text ads on intent and readiness queries
- Performance Max: Cross-channel AI-driven (only after 50+ conversions for data)

**the organization-specific note:** Google Search captures people already looking. These are highest-intent leads. Ad copy here can reference "psychedelic" and "psilocybin" in educational framing because the searcher used those terms. Landing pages must match search intent precisely.

### YouTube

**Best for:** Long-form education, webinar clips, the operator speaking content, building trust over time.

**Use when:**
- Promoting webinar replays or educational content
- Running the operator's speaking clips as pre-roll or in-feed ads
- Building retargeting audiences from video viewers
- Budget is $1,000+/month (video views are cost-efficient but need volume)

**Campaign types to use:**
- In-stream skippable: 60-120 sec the operator speaking clips or alumni stories
- In-feed: Educational content that appears in search/browse results
- Shorts: 15-30 sec retreat footage or single-insight clips

**the organization-specific note:** YouTube is the trust-building platform. Viewers who watch 75%+ of a 2-minute the operator clip are among the warmest leads in the funnel. Build retargeting audiences from these viewers.

### Platform Budget Thresholds

| Platform | Minimum Monthly | Recommended | Sweet Spot |
|---|---|---|---|
| Meta | $1,500 | $3,000-5,000 | $5,000-10,000 |
| Google Search | $1,000 | $2,000-4,000 | $3,000-7,000 |
| YouTube | $1,000 | $2,000-3,000 | $3,000-5,000 |

Below minimums, algorithms cannot exit learning phase and data is unreliable.

---

## Campaign Structure and Naming

### Naming Convention

```
[Platform]_[FunnelStage]_[Audience]_[Offer]_[Date]

Examples:
META_Cold_Interest-Meditation_FreeGuide_2026Q1
META_Warm_WebinarViewers_RetreatInquiry_2026Mar
GOOG_Search_Intent-PsychedelicRetreat_ConnectionCall_Ongoing
YT_Cold_AustinSpeaking_WebinarReg_2026Q1
META_Hot_Retarget-Applicants_RetreatClose_2026Mar
```

### Account Organization

```
Account
+-- Campaign: META_Cold_Interest-Wellness_FreeGuide_2026Q1
|   +-- Ad Set: Lookalike-Alumni-1pct
|   |   +-- Ad: Transformation-Story-Video-A
|   |   +-- Ad: Alumni-Testimonial-Carousel-B
|   |   +-- Ad: the operator-Quote-Image-C
|   +-- Ad Set: Interest-Meditation-Breathwork
|       +-- Ad: ...
+-- Campaign: META_Warm_WebinarViewers_RetreatInquiry_2026Q1
|   +-- Ad Set: Watched-75pct-Webinar
|   +-- Ad Set: Email-Subscribers-Engaged
+-- Campaign: GOOG_Search_Intent_ConnectionCall_Ongoing
    +-- Ad Group: Psychedelic-Retreat-Keywords
    +-- Ad Group: Plant-Medicine-Keywords
    +-- Ad Group: Readiness-Keywords
```

---

## Audience Targeting

### Life Transition Signals

Target people in specific life transitions — these are the doors people are already standing in. Select the transition that fits the campaign; do not generalize across all of them in one ad set.

- **Burnout recovery** — high-achievers, executives, founders who hit the wall
- **Grief** — loss of parent, partner, identity, purpose
- **Midlife questioning** — "is this all there is?" after decades of achievement
- **Career crisis or pivot** — the identity shift when what you built no longer fits
- **Post-success emptiness** — "I have everything and I feel nothing"
- **New parenthood** — the identity reorganization that no one prepares you for
- **Post-illness re-orientation** — after cancer, serious illness, or health crisis
- **Divorce or relationship ending** — the threshold between who you were and who you are becoming

### Interest Layers

Layer these interests with AND logic for precision targeting on Meta:

- **Primary:** meditation, breathwork, plant medicine, wellness retreats, consciousness, personal development
- **Adjacent:** neuroscience, psychedelic research, mindfulness, yoga retreats, silent retreats, holotropic breathwork
- **Behavioral:** podcast listeners (Tim Ferriss, Huberman Lab, Rich Roll, Aubrey Marcus), book buyers (Michael Pollan, Gabor Mate, Bessel van der Kolk)
- **Professional:** founders, executives, CEOs, entrepreneurs (for Set A avatars)

### Lookalike Audiences

Build from highest-value sources first:

1. **Alumni list** — past retreat participants (highest value; start at 1%, expand to 1-3%)
2. **Connection call bookers** — people who scheduled a call
3. **Webinar completers** — watched 75%+ of any webinar
4. **Email subscribers (engaged)** — opened 3+ emails in last 90 days
5. **Website converters** — free offer downloaders, quiz completers

### Exclusion Lists (Always Set)

- Current retreat participants and recent alumni (unless running referral/community campaign)
- Minors (age 21+ targeting on all campaigns)
- Existing applicants in active pipeline (unless retargeting to close)
- Bounced visitors (under 10 seconds on site)
- Irrelevant page visitors (careers, press, legal pages)

---

## Funnel-Aware Campaign Structure

### Stage 1: Cold Traffic to Free Offer

**Goal:** First touch. Move strangers into the ecosystem.
**Offers:** Quiz ("What's your readiness for transformation?"), guide (integration guide, preparation guide), mini-course, blog content.
**Platforms:** Meta (primary), YouTube (secondary).
**Messaging:** Lead with the reader's interior world. Name the life transition. Do not mention the organization, retreats, or anything for sale.
**CTA:** Soft — "Take the Quiz," "Get the Guide," "Watch the Talk."

### Stage 2: Warm Traffic to Webinar Registration

**Goal:** Deepen engagement. Move engaged leads toward the webinar.
**Audience:** Free offer completers, email subscribers, 75%+ video viewers, blog readers (30+ seconds).
**Platforms:** Meta retargeting (primary), YouTube retargeting, Google Search (readiness keywords).
**Messaging:** Bridge science and spirit (E4). Reference the free content they consumed. Signal depth and credibility. Introduce the operator and the community.
**CTA:** "Reserve Your Seat," "Watch the Free Masterclass," "Join the Live Session."

### Stage 3: Hot Traffic to Paid Offer

**Goal:** Convert. Move webinar attendees and high-intent visitors toward connection call or retreat inquiry.
**Audience:** Webinar attendees (especially 75%+), pricing page visitors, application starters who did not complete, connection call no-shows.
**Platforms:** Meta retargeting (primary), Google Search (branded + high-intent).
**Messaging:** Social proof (alumni numbers, testimonials). Address specific objections (safety, legality, what to expect). Create genuine time relevance only when retreat dates are real — always fetch from the `airtable-retreats` skill, never hardcode.
**CTA:** "Book a Connection Call," "Complete Your Application," "See Upcoming Retreats."

### Stage 4: Alumni to Referral Activation

**Goal:** Turn alumni into referral sources and community advocates.
**Audience:** Past retreat participants, active community members.
**Platforms:** Meta (primary — alumni see content in feed and share organically).
**Messaging:** Community belonging, "you are part of something." Invite them to bring someone. Feature their stories (with permission).
**CTA:** "Share With Someone Who's Ready," "Invite a Friend to the Masterclass."

---

## Ad Copy Formulas

All ad copy must pass: voice-calibration E1 (reader on journey, not broken), the brand kill list, and the compliance section below.

### PAS (Problem-Agitate-Solve)

"Problem" must pass E1: the reader is already on their journey, not broken. Frame the problem as a signal of readiness, not a deficit.

```
[Name the interior experience — not a category]
[Deepen: what it feels like from the inside, the specific texture of it]
[Introduce the possibility — not the product]
[CTA]
```

Example (cold — burnout recovery):
> You have been performing a version of yourself for so long that you have forgotten what the original feels like.
> The exhaustion is not from doing too much. It is from doing too much of the wrong thing, for reasons that stopped being yours somewhere along the way.
> There is a place where people go to remember. Not to be fixed — to be met.
> Get the Guide

### BAB (Before-After-Bridge)

Frame "Before" as where the reader is (with dignity, not deficit). Frame "After" as transformation, not rescue.

```
[Before: the reader's current interior world — specific, not clinical]
[After: the felt experience on the other side — sensory, believable]
[Bridge: the path between them — the organization as accelerant, not savior]
```

Example (warm — webinar registration):
> Before: The quiet suspicion that you have been optimizing your life for someone else's definition of it.
> After: The morning you wake up and realize the weight behind your sternum is gone — not because something was removed, but because something was finally allowed.
> The bridge is not another book or podcast. It is an experience, held by a community of 400+ people who stood exactly where you are standing now.
> Reserve Your Seat

### Social Proof Lead

Open with a real alumni testimonial or community metric. Always use real quotes with permission — never fabricate.

```
[Alumni quote or community stat]
[What this points to — the experience behind the number]
[CTA]
```

Example (hot — connection call):
> "I came expecting answers. I left with something better — I stopped needing them." — Alumni, 2025 Spring Retreat
> 400+ people have made this crossing. The people who went before you are rooting for you.
> Book a Connection Call

### Headline Formulas

**For Google Search ads:**
- [Readiness signal] + [What we offer]: "Ready for Change | Legal Retreat Experiences"
- [Question the searcher is already asking]: "What Happens at a Plant Medicine Retreat?"
- [Credibility] + [Outcome]: "60+ Retreats | 400+ Alumni | Feel Fully Alive"

**For Meta/YouTube ads:**
- Hook with interior world: "You have been meaning to slow down for three years."
- Hook with polarity: "The success is real. So is the emptiness."
- Hook with recognition: "Something in you already knows."
- Hook with community proof: "400+ people have made this crossing."

### CTA Variations by Funnel Stage

| Stage | Soft CTAs | Direct CTAs |
|---|---|---|
| Cold | Take the Quiz, Get the Guide, Watch the Talk | -- |
| Warm | Reserve Your Seat, Watch the Masterclass, Join the Live Session | -- |
| Hot | Book a Connection Call, See Upcoming Retreats, Complete Your Application | Apply Now |
| Alumni | Share With Someone Ready, Invite a Friend | -- |

Never use: "Buy Now," "Don't Miss Out," "Last Chance," "Act Now," or any pressure language.

---

## Compliance (CRITICAL)

Every ad must pass all six compliance checks before submission. Violations cause ad rejection, account restrictions, or legal exposure.

### 1. No Health Outcome Claims (FTC)

Do not claim that retreats, programs, or experiences treat, cure, or improve any medical or mental health condition. No before/after health claims. No clinical outcome promises.

- PROHIBITED: "Our retreats reduce depression by 80%"
- PROHIBITED: "Heal your PTSD with plant medicine"
- PROHIBITED: "Clinically proven to reduce anxiety"
- APPROVED: "An experience of deep inner work, held by trained facilitators"
- APPROVED: "Education rooted in the latest neuroscience research"
- APPROVED: "A community dedicated to personal growth and connection"

### 2. No Substance Names in Ad Copy (Platform Rejection)

Meta and Google reject ads that reference specific controlled or psychedelic substances. Do not use these terms in any ad copy, headline, description, or image text:

- PROHIBITED in ads: psilocybin, mushrooms, ayahuasca, LSD, MDMA, ketamine, DMT, psychedelics (as a product/service descriptor)
- EXCEPTION — Google Search only: "psychedelic" and "psilocybin" may appear in educational framing when the searcher used those terms. Test carefully; monitor for rejections.
- APPROVED framing: "plant medicine" (use carefully — some platforms flag this too), "expanded states," "healing experiences," "retreat experiences," "inner work," "facilitated journeys"

Landing pages linked from ads should also avoid substance names above the fold. Platform review bots scan landing pages.

### 3. No Fear-Based Hooks or Shame Triggers

Per voice-calibration E1: the reader is on their journey, not broken. Never use deficit framing, fear of missing out, shame, or urgency tactics that imply the reader is damaged.

- PROHIBITED: "If you're struggling and desperate for change..."
- PROHIBITED: "Don't let another year pass feeling broken"
- PROHIBITED: "Are you tired of failing at..."
- APPROVED: "You have been sensing that something deeper is possible."
- APPROVED: "Something in you already knows."

### 4. No Clinical Claims or Medical Advice

Do not position the organization as a medical provider, therapy practice, or clinical treatment center.

- PROHIBITED: therapy, therapeutic, clinical treatment, medical intervention
- APPROVED: healing experience, inner work, facilitated journey, personal growth, retreat experience

### 5. No Before/After Health Claims

Do not use before/after framing that implies medical or mental health outcomes.

- PROHIBITED: "Before: depressed and anxious. After: healed and whole."
- APPROVED: "Before: performing a version of myself. After: living as myself." (identity/experience framing, not health)

### 6. Brand Kill List Enforcement

Every ad must pass the brand kill list. Never use:

| Prohibited | Use Instead |
|---|---|
| Sacred | Meaningful, Intentional, Ritual |
| Miracle | Lasting Change, Real Shift, Genuine Transformation |
| Therapy / Therapeutic | Healing Experience, Inner Work, Facilitated Journey |
| Spirit Guide | Facilitator, Guide, Practitioner |
| Breakthrough | Realization, Opening, Integration, Recognition |

---

## Budget Allocation

### Split Rule

- **70% to proven campaigns** — campaigns with established positive ROAS or cost-per-lead below target
- **30% to test campaigns** — new audiences, new creative angles, new platforms, new offers

### Scaling Rules

- Increase budgets 20-30% at a time, never more
- Wait 3-5 days between increases for algorithm re-learning
- Do not pause and restart campaigns — this resets the learning phase
- Consolidate winning ad sets rather than fragmenting budget across many

---

## Creative Testing Hierarchy

Test in this order (highest impact first):

1. **Headline / hook** — the first line determines if they read or scroll; test 3-5 variations per concept
2. **Image or video** — test transformation story video vs. retreat footage vs. the operator speaking vs. alumni testimonial vs. nature/stillness imagery
3. **Body copy** — test PAS vs. BAB vs. Social Proof Lead
4. **CTA** — test soft vs. direct within the appropriate funnel stage

**Testing rules:**
- Test one variable at a time for clean data
- Need 100+ conversions per variant for statistical significance (or 1,000+ impressions for awareness campaigns)
- Kill underperformers after 3-5 days with sufficient spend
- Iterate on winners — do not replace them, create variations of what works

---

## Bid Strategies and Progression

1. **Awareness campaigns:** Start with Reach or Impressions objective. Use CPM bidding. Goal: build retargeting audiences cheaply.
2. **Consideration campaigns:** Switch to Traffic or Video Views objective after building initial audiences. Use cost-per-click or cost-per-view bidding.
3. **Conversion campaigns:** Switch to Conversions objective only after accumulating 50+ conversions. Use Target CPA or Maximize Conversions bidding based on historical cost-per-lead data.

**Progression timeline:**
- Weeks 1-2: Awareness + audience building
- Weeks 3-4: Layer in consideration retargeting
- Weeks 5+: Activate conversion campaigns with sufficient data
- Exception: Google Search can start at conversion objective immediately if keywords have clear commercial intent

---

## Retargeting Windows

| Audience | Window | Frequency Cap | Message |
|---|---|---|---|
| Webinar attendees (75%+) | 1-7 days | Higher frequency OK | Direct: connection call, retreat dates |
| Free offer completers | 7-14 days | 4-5x/week | Webinar invitation, deeper content |
| Pricing/application page visitors | 1-14 days | 5-7x/week | Objection handling, alumni proof, retreat dates |
| Blog/content viewers (30+ sec) | 14-30 days | 3x/week | Free offer, webinar registration |
| General site visitors | 30-60 days | 2x/week | Awareness content, the operator speaking clips |
| Video viewers (75%+) | 14-30 days | 3x/week | Webinar registration, free offer |
| Lapsed email subscribers | 30-90 days | 1-2x/week | Re-engagement content, new free offer |

Exclude recent converters for 7-14 days after conversion to avoid wasted spend.

---

## Reporting Cadence

### Weekly Performance Review

- Spend vs. budget pacing
- CPA / cost-per-lead vs. targets
- Top and bottom performing ads (pause bottom 20%)
- Audience performance breakdown
- Frequency check (pause ad sets above 3.0 frequency for cold audiences)
- Landing page conversion rate
- Disapproved ads or policy issues — resolve same day
- Creative fatigue signals (CTR declining week-over-week)

### Monthly Strategy Review

- Overall channel performance vs. funnel goals
- Creative performance trends and fatigue lifecycle
- Audience insights: which life transitions and interest layers convert best
- Budget reallocation: shift from 70/30 proven/test based on learnings
- Test results summary and next month's test plan
- Lookalike audience refresh (update source lists with new alumni/converters)
- Compliance audit: review any rejected ads and update copy templates

---

## Steps

1. Confirm campaign goal, funnel stage, budget, offer, and available creative assets.
2. Select platform(s) using the platform selection guide above.
3. Define audience targeting: life transition, interest layers, lookalikes, and exclusions.
4. Structure campaigns using the naming convention and account organization above.
5. Write ad copy using the appropriate formula (PAS, BAB, or Social Proof Lead).
6. Run every ad through the compliance checklist (all six checks).
7. Run every ad through the brand kill list.
8. Run every ad through voice-calibration E1: does the copy treat the reader as on their journey, not broken?
9. Define bid strategy based on funnel stage and available conversion data.
10. Set retargeting windows and frequency caps.
11. Present the complete campaign plan: campaigns, ad sets, ad copy, targeting, budget allocation, and testing plan.

## Output

Deliver a structured campaign plan containing:

- **Platform(s) selected** with rationale
- **Campaign structure** with naming, ad sets, and targeting for each
- **3-5 ad copy variations** per campaign, labeled by formula used (PAS/BAB/Social Proof)
- **Compliance certification**: confirm all six checks passed for each ad
- **Budget allocation** across campaigns with 70/30 split noted
- **Testing plan**: what to test first, expected timeline, kill criteria
- **Retargeting setup**: windows, frequency caps, audience definitions
- **Reporting schedule**: weekly and monthly review items

## Error Handling

- If campaign goal is unclear: ask before proceeding — do not guess the funnel stage
- If budget is below platform minimums: recommend the single best platform and explain why others are not viable at that budget
- If no creative assets exist: recommend starting with image-based Meta ads using alumni quotes and retreat photography, not video
- If compliance check fails on any ad: flag the specific violation, cite the rule, provide a compliant rewrite
- If the brand kill list catches a term: replace with the approved alternative and note the substitution
- If retreat dates are needed for urgency framing: fetch live from the `airtable-retreats` skill — never hardcode dates
