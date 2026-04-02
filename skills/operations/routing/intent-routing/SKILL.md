---
name: intent-routing
description: "Route a task to the correct skill using intent keyword matching across image generation, specialist, integration, and general-purpose skill maps."
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /intent-routing
metadata:
  openclaw:
    emoji: "🗺️"
---

# Intent Routing Maps

Use these maps with the Skill Routing tiers defined in AGENTS.md. Evaluate Tier 3 (intent keyword match) by scanning the task against these tables. Select the most specific matching skill.

## Routing Table

Load routing table from `config/routing-table.yaml`.

The config defines keyword-to-skill mappings organized into four sections:
- **image_generation** — highest priority; evaluated before all other tiers
- **tenant_specialist** — purpose-built skills that take priority over bundled skills when the domain matches
- **tenant_integration** — additional installed and active integration skills
- **general_purpose** — bundled skills for common cross-domain tasks

The config also includes:
- **delegated_agents** — requests that should route to a specialist agent via `delegation` rather than a skill
- **disambiguation** — strict rules for skills that overlap in domain (e.g., `attio` vs `api-gateway`, `gog` vs `email-triage`)
- **routing_notes** — skills that are NOT valid routing targets (e.g., `resend`, `discord`)

Evaluate tiers in order: image_generation → tenant_specialist → tenant_integration → general_purpose. Select the most specific matching skill.

## Delegated Agents — Website Build

When the user requests any of the following, delegate to `agents/website/orchestrator` (Construct) via the `delegation` skill:

**Keywords**: build website, create website, build page, build homepage, website for, landing page for, redesign site, rebuild site, new website, single page website

**Action**: Construct invokes ClawPipe with `pipelines/website/website-single-page-native.yaml`. Do NOT attempt to build a website by invoking frontend skills directly — always route to Construct for orchestrated builds.
