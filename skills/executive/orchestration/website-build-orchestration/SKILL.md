---
name: website-build-orchestration
description: "Orchestrate website builds from blueprint through design, TDD, and deployment"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /website-build-orchestration
metadata:
  openclaw:
    emoji: "🏗️"
    requires:
      bins: []
      env: []
      os: ["darwin"]
---

# Website Build Orchestration

Coordinate the full website build pipeline from blueprint through design, implementation, TDD, and deployment. This skill manages the end-to-end process of constructing pages, running quality gates, and deploying to staging and production.

## When to Use

- Starting a new website build from an approved blueprint
- Coordinating foundation infrastructure (global nav, footer, shared layout, design tokens)
- Managing the build pipeline for individual pages
- Running cross-page consistency checks before deployment
- Managing domain cutover from staging to production

## Pipeline Phases

### Phase 0: Resume Check
On every invocation, check for pipeline state. If a prior pipeline exists, resume from the indicated stage with provided prior work. If complete, report completion. If an external-write stage needs fresh approval, stop and ask.

### Phase 1: Blueprint Reading
Read `memory/site-context.yaml` to determine the active site, then read the blueprint at the path specified in `site-context.website.blueprint`. If site context does not exist, prompt: "No active site set. Run `/site <name>` first."

Build exactly what the blueprint specifies. Do not interpret, infer, or improvise. If a spec is ambiguous, ask for clarification before proceeding.

### Phase 2: Foundation Build
Build shared infrastructure before individual pages:
- Global navigation
- Footer
- Shared layout components
- Design tokens
- Common components

Pages built on an inconsistent foundation create rework.

### Phase 3: Page Build
For each page with status `spec-complete` or above in the blueprint:
1. Delegate design to Creative Director (design spec)
2. Delegate implementation to Frontend Engineer (code)
3. Use handoff contracts for every delegation
4. Verify contract assertions after each sub-agent completes
5. Contract verification failures halt the pipeline

### Phase 4: TDD
Every page goes through TDD before deploying to staging. No exceptions. TDD failures block deployment.

### Phase 5: Consistency Check
Before marking any page as built, run cross-page consistency checks:
- Nav links match routes
- Shared components are consistent across pages
- CTA language is aligned
- No orphan pages

### Phase 6: Staging Deploy
Deploy to staging subdomain. Individual page staging deploys are autonomous after TDD passes.

### Phase 7: Approval and Production
For domain cutover: full status report before requesting approval. Include routes, redirects, TDD results, and post-deploy verification.

## Approval Gates

- **Foundation**: User approves design before build begins
- **Domain cutover**: User provides explicit approval
- **Production deploy**: Never deploy to production domain without explicit approval
- **Staging deploys**: Autonomous after TDD passes (individual pages)

## Build Log

Every build event is recorded in `docs/website/build-log.md`. Append only -- never edit or delete existing entries.

## Governance Events

After each pipeline stage completes, emit a governance event:
```bash
python3 scripts/paperclip-event.py stage website-YYYY-MM-DD <from_stage> <to_stage> --agent "Website Orchestrator"
```

These calls are non-fatal -- if the governance system is offline, the pipeline continues.

## Communication Format

- **Build status**: one message at start, one at staging deploy, one per page built
- **TDD results**: always include pass/fail count
- **Consistency check results**: brief table format: nav OK | CTA OK | shared components OK | orphan pages: 0
- **Blockers**: state what is blocked and what information is needed
- **Domain cutover**: full status report with routes, redirects, TDD results, post-deploy verification

## Boundaries

- Never modify the blueprint. It is read-only.
- Never deploy to production without explicit approval.
- Never skip TDD. Fix failures and re-run before deploying.
- Never build pages with status below `spec-complete` in the blueprint.
- Never write or modify page specs or the redirect map -- those are owned by the blueprint author.

## Dependencies

- `frontend` -- web page implementation workflow
- `campaign-tdd` -- mandatory TDD after code generation
- `deployment` -- Vercel deploy to staging and production
- `brand-standards` -- brand voice and compliance
- `schema-markup` -- structured data for built pages
