---
name: reasoning-router
description: "Which reasoning level should I use for this task?"
version: "1.0.0"
permissions:
  filesystem: none
  network: false
triggers:
  - command: /reasoning-router
metadata:
  openclaw:
    emoji: "🧠"
---

# Reasoning Effort Router

Use this skill to determine the correct `reasoning_effort` level for any task. The correct level balances response quality against rate-limit quota consumption. Higher reasoning effort uses more quota from the 5-hour message window.

---

## Decision Tree

| Task Type | reasoning_effort | Rationale |
|---|---|---|
| Heartbeat ACK | `low` | Binary response: HEARTBEAT_OK or action needed |
| Status check | `low` | Read-only lookup, no synthesis |
| Simple data lookup | `low` | Single-record retrieval, no reasoning chain |
| Log write | `low` | Structured write, no judgment required |
| Email draft (standard) | `medium` | Single-audience, single-CTA composition |
| CRM record update | `medium` | Structured field mapping |
| Standard workflow execution | `medium` | Following defined playbook |
| Personalized outreach | `medium` | Moderate synthesis from known context |
| Objection handling | `high` | Multi-step reasoning, emotional intelligence |
| Campaign strategy | `high` | Multi-variable planning, audience segmentation |
| Invoice math verification | `high` | Arithmetic chain validation, discrepancy detection |
| Multi-step document analysis | `high` | Cross-reference and pattern recognition |
| Security review | `xhigh` | Adversarial reasoning, edge-case detection |
| Invoice fraud verification | `xhigh` | Financial integrity, potential legal consequences |
| Architecture decisions | `xhigh` | Long-horizon, high-consequence planning |
| Prompt injection detection | `xhigh` | Adversarial pattern recognition |

---

## One Example Per the organization Domain

### Sales (agents/sales/director)

| Task | Level | Example |
|---|---|---|
| Log touchpoint to Attio | `low` | Write Attio note after confirmed send |
| Send post-call follow-up email | `medium` | Personalize using Fireflies summary |
| Handle "I need to think about it" objection | `high` | Apply Feel-Felt-Found with call-specific context |
| Evaluate suspicious lead pattern | `xhigh` | Assess potential fraud or misrepresentation |

### Marketing — Brand (agents/marketing/brand)

| Task | Level | Example |
|---|---|---|
| Log draft approval to memory | `low` | Write approval timestamp to brand-state.json |
| Write a social post caption | `medium` | Single voice archetype, single platform |
| Write a full retreat description (Draft 1) | `high` | Multi-pillar, Chain of Draft, testimonial arc |
| Evaluate brand archetype alignment for a new campaign | `xhigh` | Cross-persona consistency, long-term brand risk |

### Marketing — Email (agents/marketing/email)

| Task | Level | Example |
|---|---|---|
| Log campaign send to memory | `low` | Append to memory/logs/sends/YYYY-MM-DD.md |
| Write a single email draft | `medium` | One offer, one CTA, one segment |
| Design a 7-email welcome sequence | `high` | Multi-email story arc, persona selection, subject line variants |
| Audit a full launch sequence for brand compliance | `xhigh` | Prohibited language scan, segmentation logic review |

### Finance — Payroll (agents/finance/payroll)

| Task | Level | Example |
|---|---|---|
| Log invoice decision to memory | `low` | Append PASS/FLAG/HOLD to invoice-decisions log |
| Verify single invoice math | `medium` | Line items → subtotals → total check |
| Reconcile multiple contractor invoices with overlapping billing periods | `high` | Cross-invoice comparison, pattern detection |
| Evaluate invoice with suspected fraud indicators | `xhigh` | Adversarial math verification, identity cross-check |

### Programs — Onboarding (agents/programs/onboarding/*)

| Task | Level | Example |
|---|---|---|
| Write HEARTBEAT_OK response | `low` | No pending actions detected |
| Send application confirmation email | `medium` | Template-based, standard context |
| Evaluate medical intake for contraindications | `high` | Tier 1 / Tier 2 classification, RAG lookup |
| Review intake with suspected injection attempt | `xhigh` | Security alert, quarantine decision |

---

## Rate Limit Guardrails

These are enforced alongside reasoning effort selection:

- Minimum **5 seconds** between any two API calls
- Minimum **10 seconds** between web searches
- Maximum **5 searches per batch** — then take a **2-minute break** before resuming
- On **429 error**: STOP immediately, wait 5 minutes, retry once. If the 429 persists after retry, notify the operator via Slack and halt the workflow.

---

## Quick Reference

```
low    → heartbeat, status, lookup, log
medium → draft, CRM update, standard workflow
high   → objection, strategy, multi-step analysis
xhigh  → security, fraud, architecture, adversarial
```
