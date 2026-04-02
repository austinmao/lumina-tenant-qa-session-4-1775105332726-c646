---
name: env-management
description: "Manage environment variables, .env files, and secrets across dev/staging/prod"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Manage environment configuration across environments. Handle .env files, Doppler integration, and secret rotation.

## When to Use
- Setting up environment variables for a new project
- Rotating secrets
- Configuring staging/prod differences

## Rules
- Never commit .env files (only .env.example with empty values)
- Use Doppler for production secrets
- Prefix client-side vars with NEXT_PUBLIC_
- Document every env var in .env.example with comments
