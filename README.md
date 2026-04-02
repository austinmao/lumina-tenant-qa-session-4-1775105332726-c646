# Lumina Tenant Repo

This repository contains tenant-specific configuration for a Lumina customer instance.

## Structure

- `tenant.yaml` — Tenant configuration (gateway compatibility, cognition registry)
- `site-config.yaml` — Site-specific configuration (Sanity, domain)
- `agents/` — Tenant-specific agent overrides (SOUL.md, AGENTS.md)
- `brands/` — Brand assets (logos, tokens, brand guide)
- `config/` — Runtime config (ClawWrap targets, outbound policy)
- `skills/` — Tenant-specific skill overrides

## Template

This repo was created from [lumina-tenant-template](https://github.com/<github-org>/lumina-tenant-template).
Check template_version in tenant.yaml to see which version this was created from.

## Updating from template

Template updates are delivered as PRs via the template-sync GitHub Action in the platform repo.
