---
name: ab-test-setup
description: >
  Plan and analyze A/B tests with proper statistical rigor and ethical
  guardrails. Use when the user wants to design an experiment, set up a split
  test, write a test hypothesis, calculate sample size for a test, analyze
  A/B test results, or decide whether a test result is actionable. Includes
  low-traffic and sequential testing guidance for small audiences.
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /ab-test-setup
metadata:
  openclaw:
    emoji: "test-tube"
    requires:
      env: []
      bins: []
---

# A/B Test Setup

## Overview

Plan, execute, and analyze experiments across the the marketing funnel — from
webinar registration pages to email subject lines to sales pages. This skill
enforces statistical rigor, ethical testing standards, and low-traffic methods
appropriate for education-to-experience businesses with smaller audiences.

## Steps

1. **Define the hypothesis** using the structured framework below.
2. **Calculate required sample size and duration** using the reference tables.
3. **Design variants** following the one-variable rule.
4. **Check the ethics layer** — both variants must pass `voice-calibration` and
   `marketing-psychology` ethics standards.
5. **Run the test** without peeking or modifying variants mid-flight.
6. **Analyze results** — distinguish statistical significance from practical
   significance.
7. **Document learnings** using the test documentation template.

---

## Hypothesis Framework

Every test starts with a written hypothesis. No "let's see what happens."

**Template:**

```
If we change [X],
then [Y] will happen,
measured by [Z],
because [rationale].
```

**Example — weak:**
"Changing the headline might help conversions."

**Example — strong:**
"If we change the webinar registration headline from 'Join Our Free Webinar'
to 'What 200 Past Participants Wish They Knew Before Their First Retreat,'
then registration rate will increase by 20%+, measured by form submissions
divided by unique page views, because social proof and curiosity-driven
headlines outperform generic invitations in our past email open rate data."

A good hypothesis includes:
- **Observation**: What data or insight prompted this idea
- **Change**: The specific modification being tested
- **Expected effect**: Direction and magnitude
- **Metric**: Exactly how success is measured
- **Rationale**: Why you believe this will work

---

## Sample Size Reference

### Inputs

1. **Baseline conversion rate**: Your current rate for the metric
2. **Minimum detectable effect (MDE)**: Smallest lift worth detecting
3. **Significance level**: 95% (p < 0.05) — or see Low-Traffic section
4. **Power**: 80%

### Quick Reference Table (per variant, 95% confidence / 80% power)

| Baseline Rate | 10% Relative Lift | 20% Relative Lift | 50% Relative Lift |
|---------------|--------------------|--------------------|-------------------|
| 1%            | 150,000            | 39,000             | 6,000             |
| 3%            | 47,000             | 12,000             | 2,000             |
| 5%            | 27,000             | 7,000              | 1,200             |
| 10%           | 12,000             | 3,000              | 550               |
| 20%           | 5,000              | 1,300              | 250               |
| 40%           | 2,000              | 550                | 110               |

### Duration Estimate

```
Duration (days) = (Sample per variant x Number of variants)
                  / (Daily traffic to page x Allocation %)
```

Minimum runtime: 7 days (one full business cycle).
Maximum runtime: 4-6 weeks (beyond this, external factors distort results).

---

## Test Types

### A/B Test (Split Test)
- Two versions: Control (A) vs. Variant (B).
- Single change between them. Most common, easiest to analyze.
- Use for: headline tests, CTA tests, form length, social proof placement.

### Multivariate Test (MVT)
- Multiple elements changed in combinations (e.g., headline x image).
- Requires significantly more traffic — rarely appropriate for the organization
  page-level tests.
- Use only when testing element interactions is the explicit goal.

### Sequential Test (for Low Traffic)
- Data analyzed continuously with adjusted stopping rules.
- Allows early stopping when evidence is strong, without inflating false
  positive rate.
- Preferred method given typical traffic volumes.
- See the Low-Traffic Testing section below.

---

## Traffic Allocation

| Strategy | Split | When to Use |
|----------|-------|-------------|
| Standard | 50/50 | Default for most tests |
| Conservative | 80/20 or 90/10 | High-risk changes (pricing, checkout) |
| Ramping | Start 90/10, move to 50/50 | Technical risk mitigation |

Rules:
- Users must see the same variant on return visits (sticky assignment).
- Run both variants simultaneously — never sequential time periods.
- Ensure balanced exposure across days of week.

---

## Variant Design Principles

1. **Test one variable at a time.** If you change the headline AND the image,
   you cannot attribute the result.
2. **Make meaningful differences.** A one-word change is unlikely to produce
   detectable lift. Test bold alternatives.
3. **Keep implementation identical.** Both variants must load at the same speed,
   render correctly on mobile, and function identically aside from the tested
   element.

---

## Metrics Hierarchy

For every test, define all three levels before launching:

### Primary Metric
- The single metric the test is optimizing.
- Directly tied to the hypothesis.
- This is what you use to call a winner.

### Secondary Metrics
- Related indicators that explain the "why."
- Example: if primary is registration rate, secondary might be time-on-page
  or scroll depth.

### Guardrail Metrics
- Things that must NOT degrade.
- If a guardrail degrades significantly, stop the test regardless of primary
  metric performance.
- Examples: bounce rate, downstream conversion (registered but didn't attend),
  unsubscribe rate, refund/complaint rate.

### Metric Examples for the organization Funnel

**Webinar registration page:**
- Primary: Registration rate (form submissions / unique visitors)
- Secondary: Scroll depth, time to submit
- Guardrail: Show-up rate (registrants who attend)

**Email subject line:**
- Primary: Open rate
- Secondary: Click-through rate
- Guardrail: Unsubscribe rate

**Sales page:**
- Primary: Application/inquiry rate
- Secondary: Time on page, scroll depth, FAQ click rate
- Guardrail: Refund rate, support inquiry rate

---

## Low-Traffic Testing (Critical for This Business)

The organization operates with smaller audiences than SaaS companies. Traditional
frequentist A/B testing often requires traffic volumes that would take months
to accumulate. Use these adapted methods:

### Sequential Testing
- Analyze data as it arrives using sequential analysis methods (e.g., SPRT or
  always-valid p-values).
- Allows stopping early when evidence is strong.
- Set a maximum sample size / duration as a cap.
- Tools: most modern experimentation platforms support sequential designs.

### Bayesian Methods Over Frequentist
- When sample sizes are small, Bayesian analysis provides a probability of
  improvement rather than a binary significant/not-significant answer.
- Report results as: "There is an 85% probability that Variant B improves
  registration rate by at least 5%."
- This is more useful for decision-making than "p = 0.12, not significant."

### Directional Signal Thresholds
When statistical significance is not achievable with available traffic:
- **90%+ probability of improvement**: Strong signal. Implement with confidence.
- **80-90% probability**: Directional signal. Actionable for low-cost changes
  (copy, layout). Confirm with a follow-up test if the change is expensive.
- **60-80% probability**: Weak signal. Do not act. Gather more data or test a
  bolder variant.
- **Below 60%**: No signal. Variants are effectively equivalent.

### Qualitative Alternatives
When quantitative testing is impractical (very low traffic, early-stage pages):
- **5-person usability testing**: Watch 5 people interact with each variant.
  Identifies 85% of usability issues.
- **Session recording review**: Review 20-30 session recordings per variant
  for behavioral patterns.
- **Direct user feedback**: Ask 10-15 past participants which version resonates
  and why.
- **Preference testing**: Show both variants side-by-side to a small panel and
  collect structured feedback.

### Minimum Detectable Effect Guidance
- With small traffic, only test for large differences (>20% relative lift).
- Do not attempt to detect 5-10% lifts — you will never reach significance
  and will waste time.
- Design bolder variants: entirely different headlines, different page
  structures, different value propositions.

---

## Ethical Testing Standards

Both variants must pass the `voice-calibration` skill and the
`marketing-psychology` ethics layer.

**Rules:**
- Never test a manipulative variant against an ethical one to see which
  converts better. The goal is to optimize within ethical bounds.
- Both variants must be truthful, non-coercive, and consistent with
  the active brand voice.
- If a variant uses urgency, scarcity, or social proof, it must be factually
  accurate (real deadlines, real seat counts, real testimonials).
- Testing deceptive framing (fake scarcity, fabricated testimonials, misleading
  claims) is prohibited regardless of conversion impact.

---

## Priority Test Areas (Education-to-Experience Funnel)

Ordered by expected signal speed and volume:

1. **Email subject lines** — Fastest signal. Largest addressable audience.
   Test open rates across your full list.
2. **Webinar registration page** — Highest-volume page in the funnel.
   Test headline, social proof format, form length.
3. **Free offer landing page** — Headline, CTA copy, lead magnet description.
4. **Sales/application page** — Price anchoring sequence, testimonial
   placement, objection ordering, CTA copy. Lower volume but highest
   revenue impact per conversion.

---

## Analysis Methodology

### Statistical vs. Practical Significance

A result can be statistically significant but not worth implementing:
- A 2% relative lift that is statistically significant may not justify the
  engineering effort to maintain the variant.
- Conversely, a 30% lift that falls short of p < 0.05 due to small samples
  may still be a strong directional signal worth acting on (see Low-Traffic
  section).

### Analysis Checklist

1. Did you reach the pre-committed sample size?
   - If no: result is preliminary. Note this in documentation.
2. Is the result statistically significant (p < 0.05) or, for Bayesian
   analysis, is the probability of improvement above the threshold?
3. Is the effect size practically meaningful? Project the business impact.
4. Do secondary metrics support the primary result?
5. Are any guardrail metrics degraded?
6. Check segment differences: mobile vs. desktop, new vs. returning,
   traffic source.

---

## Documentation Template

After every test, record results using this format:

```
# Test: [Descriptive Name]

## Hypothesis
If we change [X], then [Y] will happen, measured by [Z], because [rationale].

## Variants
- Control (A): [Description]
- Variant (B): [Description + what specifically changed]

## Configuration
- Test type: A/B / Sequential / Bayesian
- Traffic allocation: [e.g., 50/50]
- Target sample size: [N per variant]
- Actual sample size: [N achieved per variant]
- Duration: [Start date] to [End date]

## Results
- Primary metric: Control [X%] vs. Variant [Y%] ([+/-Z% relative change])
- Confidence: [p-value or probability of improvement]
- Secondary metrics: [Summary]
- Guardrail metrics: [Any degradation? Y/N]

## Decision
[Implement variant / Keep control / Inconclusive — run follow-up]

## Learnings
[What did we learn? What should we test next?]

## Next Steps
[Specific follow-up actions with owners and dates]
```

---

## Common Mistakes

1. **Peeking problem**: Checking results before reaching sample size and
   stopping when they look good. This inflates false positive rates. Commit
   to a stopping rule before launching, or use sequential testing.
2. **Insufficient sample size**: Running a test for "a few days" without
   calculating required sample. Use the reference table above.
3. **Testing too many things at once**: Changing headline, image, CTA, and
   layout simultaneously. You cannot isolate what caused the result.
4. **Not documenting learnings**: Running tests without recording outcomes
   leads to repeated mistakes and lost institutional knowledge.
5. **Stopping inconclusive tests too early**: "No result" after 3 days is
   not a conclusion. Either run to the planned duration or use sequential
   methods.
6. **Ignoring guardrail metrics**: A variant that lifts registration rate
   but tanks show-up rate is not a winner.

---

## Output Format

When the user asks to plan a test, produce a complete test plan document:

```
# A/B Test Plan: [Name]

## Hypothesis
[Full hypothesis using the framework]

## Test Design
- Type: [A/B / Sequential / Bayesian]
- Duration: [X days/weeks]
- Sample size: [N per variant]
- Traffic allocation: [Split]

## Variants
- Control (A): [Description]
- Variant (B): [Description + rationale]

## Metrics
- Primary: [Metric name and definition]
- Secondary: [List]
- Guardrails: [List]

## Ethics Check
- [ ] Both variants pass voice-calibration
- [ ] Both variants pass marketing-psychology ethics layer
- [ ] No deceptive framing in either variant

## Analysis Plan
- Method: [Frequentist / Bayesian / Sequential]
- Success criteria: [What constitutes a win]
- Minimum runtime: [Days]
```

When the user asks to analyze results, produce a results summary using the
Documentation Template above.

---

## Related Skills

- **voice-calibration**: Verify both variants match the active brand voice.
- **marketing-psychology**: Ethics layer for persuasion techniques.
- **campaign-strategy**: Broader campaign planning context.
- **analytics-tracking**: Setting up measurement for test metrics.
- **copywriting**: Generating variant copy.
