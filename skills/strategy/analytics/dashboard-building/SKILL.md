---
name: dashboard-building
description: "Design KPI dashboards with metrics selection and visualization best practices"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /dashboard-building
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: []
      env: []
---

# KPI Dashboard Design

Design effective KPI dashboards with metrics selection, visualization best practices, layout patterns, and real-time monitoring. Use when building executive dashboards, selecting meaningful KPIs, or designing department-specific metrics views.

## When to Use

- Designing executive summary dashboards
- Selecting meaningful KPIs for a business unit
- Building real-time operations monitoring displays
- Creating SaaS metrics dashboards
- Establishing metric governance and reporting cadence

## KPI Framework

| Level | Focus | Update Frequency | Audience |
|---|---|---|---|
| Strategic | Long-term goals | Monthly/Quarterly | Executives |
| Tactical | Department goals | Weekly/Monthly | Managers |
| Operational | Day-to-day ops | Real-time/Daily | Teams |

## Common KPIs by Department

**Sales:** MRR, ARR, ARPU, Pipeline Value, Win Rate, Average Deal Size, Sales Cycle Length.
**Marketing:** CPA, CAC, Lead Volume, MQLs, Conversion Rate, Email Open/Click Rate, Marketing ROI.
**Product:** DAU/MAU, Session Duration, Feature Adoption Rate, NPS, CSAT, Churn Rate, Activation Rate.
**Finance:** Gross Margin, Net Profit Margin, EBITDA, Current Ratio, Cash Flow, Revenue per Employee.

## Dashboard Layout Patterns

### Executive Summary
4-6 headline KPI cards with trend indicators (up/down arrows + percentage change). Revenue trend line chart. Revenue by product/segment pie chart. Alert section for threshold breaches.

### SaaS Metrics Dashboard
MRR/ARR cards with growth rates. MRR growth trend line. Unit economics block (CAC, LTV, LTV:CAC ratio, payback period). Cohort retention heatmap. Churn analysis (gross, net, logo, expansion).

### Real-time Operations
System health gauges (CPU, MEM, DISK). Service status indicators (healthy/degraded/down). Request throughput sparkline. Error rate with threshold line. Recent alerts feed.

## Implementation Patterns

**SQL for KPI Calculations:**
- MRR: SUM of active subscriptions normalized to monthly
- Cohort retention: LEFT JOIN users to activity by cohort month
- CAC: Total S&M spend / new customers acquired

**Dashboard Tools:** Streamlit (Python prototyping), Grafana (ops monitoring), Looker/Tableau (BI).

## Best Practices

**Do:** Limit to 5-7 KPIs, show context (comparisons, trends, targets), consistent color coding (red=bad, green=good), enable drilldown, match update frequency to metric cadence.

**Do Not:** Show vanity metrics, overcrowd the display, use 3D charts, hide calculation methodology, ignore mobile responsiveness.
