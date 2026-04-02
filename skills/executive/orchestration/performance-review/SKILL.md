---
name: performance-review
description: "Track startup metrics, unit economics, and performance benchmarks for fundraising"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /performance-review
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: []
      env: []
---

# Performance Review & Startup Metrics

Track, calculate, and optimize key performance metrics for different business models. Covers unit economics, growth efficiency, SaaS metrics, marketplace metrics, and fundraising-ready dashboards. Use when reviewing business performance, preparing investor updates, or optimizing growth efficiency.

## When to Use

- Calculating and tracking startup metrics (CAC, LTV, MRR)
- Preparing investor-ready performance dashboards
- Optimizing unit economics and growth efficiency
- Benchmarking against stage-appropriate targets
- Creating monthly/quarterly business reviews

## Universal Startup Metrics

### Revenue
- MRR = sum of active subscriptions at monthly rate
- ARR = MRR x 12
- MoM Growth = (current - previous) / previous
- Targets: Seed 15-20% MoM, Series A 10-15% MoM (3-5x YoY)

### Unit Economics
- CAC = Total S&M Spend / New Customers
- LTV = ARPU x Gross Margin% x (1 / Churn Rate)
- LTV:CAC > 3.0 = Healthy, 1.0-3.0 = Needs improvement, < 1.0 = Unsustainable
- CAC Payback = CAC / (ARPU x Gross Margin%). Target: < 12 months

### Cash Efficiency
- Burn Multiple = Net Burn / Net New ARR. Target: < 1.5
- Runway (months) = Cash Balance / Monthly Burn. Maintain 12-18 months

## SaaS Metrics

- Net New MRR = New + Expansion - Contraction - Churned
- NDR (Net Dollar Retention): > 120% = Best-in-class, > 100% = Good
- Gross Retention: > 90% = Excellent, > 85% = Good
- Magic Number = Net New ARR (quarter) / S&M Spend (prior quarter). > 0.75 = Ready to scale
- Rule of 40 = Revenue Growth Rate% + Profit Margin%. > 40% = Excellent
- Quick Ratio = (New + Expansion MRR) / (Churned + Contraction MRR). > 4.0 = Healthy

## Metrics by Stage

**Pre-Seed:** Active users, retention (Day 7/30), core engagement, qualitative feedback.
**Seed ($500K-$2M ARR):** MRR growth, baseline CAC/LTV, gross retention, product engagement.
**Series A ($2M-$10M ARR):** ARR growth (3-5x YoY), LTV:CAC > 3, NDR > 100%, burn multiple < 2.0, magic number > 0.5.

## Investor Dashboard Format

```
Current MRR: $250K (up 18% MoM)
ARR: $3.0M (up 280% YoY)
CAC: $1,200 | LTV: $4,800 | LTV:CAC = 4.0x
NDR: 112% | Logo Retention: 92%
Burn: $180K/mo | Runway: 18 months
```

## Common Mistakes

1. Vanity metrics (total users without retention)
2. Too many metrics (track 5-7 core metrics intensely)
3. Ignoring unit economics even at seed stage
4. Not segmenting by customer type, channel, cohort
5. Gaming metrics instead of optimizing for real business outcomes
