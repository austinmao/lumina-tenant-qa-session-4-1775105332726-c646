---
name: org-config
description: "Look up organizational constants — domain, emails, logo, Slack channels, brand colors"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    emoji: "🏢"
---

# Org Config

Org constants are now in `config.yaml` (generated at boot by scripts/provision.py). Read `config.yaml` for the current instance's values.

This skill provides quick-reference lookup for commonly-used organizational constants.

## Identity

| Key | Value |
|---|---|
| Name | [from config/org.yaml: identity.name] |
| Domain | [from config/org.yaml: contact.domain] |
| Homepage | https://www.[from config/org.yaml: contact.domain] |
| Legal | [from config/org.yaml: identity.legal_name] |

## Contact

| Key | Value |
|---|---|
| Contact email | info@[the organization's domain] |
| Agent email | lumina@[the organization's domain] |
| Agent name | Lumina |
| Resend from | info@[the configured sending domain] |
| Resend reply-to | lumina@[the organization's domain] |

## Media

| Key | Value |
|---|---|
| Logo URL | [from config/org.yaml: media.logo_url] |
| CDN base | https://media.[the organization's domain] |

## Slack

| Key | Value |
|---|---|
| Bot channel | #lumina-bot |
| Ops channel | #ops-onboarding (ID: C0AHSENHJHG) |

## Brand Colors

| Token | Hex | Usage |
|---|---|---|
| accent | #8b7355 | Links, secondary buttons, eyebrow labels |
| body-bg | #f5f0ea | Page/Body background |
| text-primary | #1a1a1a | Headings |
| text-body | #333333 | Paragraph text |
| web-accent | #14B8A6 | Web UI accent (buttons, headings) |

## Config File Location

Source of truth for multi-tenancy: `tenants/<tenant-slug>/config/org.yaml` or environment variables set at boot via `scripts/provision.py`.
