---
name: composio-oauth
description: "Implement OAuth flows via Composio for third-party service authentication"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Use Composio as the OAuth provider for connecting third-party services (Google, Zoom, etc.).

## When to Use
- Setting up OAuth for a new integration
- Managing token refresh flows
- Handling multi-tenant OAuth scopes
