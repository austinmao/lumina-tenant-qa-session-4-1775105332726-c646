---
name: tech-stack-review
description: "Evaluate and recommend technology decisions for web projects"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Evaluate technology choices for web projects. Compare frameworks, databases, hosting options, and integrations against project requirements.

## When to Use
- New project setup requiring stack decisions
- Evaluating whether to add a new dependency
- Comparing hosting/deployment options

## Steps
1. Understand project requirements (type, scale, team, timeline)
2. Evaluate options against: performance, DX, ecosystem, cost, maintenance
3. Recommend stack with rationale
4. Document decision in architecture decision record
