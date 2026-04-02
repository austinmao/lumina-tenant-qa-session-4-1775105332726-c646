---
name: engineering-orchestration
description: "Coordinate engineering tasks across Frontend, Backend, Email, and DevOps teams"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Coordinate multi-team engineering work. Decompose technical requirements into tasks, assign to the right engineer, track dependencies, and verify integration.

## When to Use
- CMO or CCO delegates technical work requiring multiple engineers
- A project spans frontend + backend + infrastructure

## Steps
1. Receive technical brief from CMO/CCO or operator
2. Decompose into engineer-specific tasks with dependencies
3. Assign via sessions_spawn to the correct engineer agents
4. Track completion and resolve blockers
5. Verify integration across components
6. Report completion to the requesting C-suite agent
