---
name: hyperspell
description: "Search knowledge base / look up customer documents / find context from connected sources"
version: "1.0.0"
permissions:
  filesystem: none
  network: true
triggers:
  - command: /hyperspell
metadata:
  openclaw:
    emoji: "🔮"
    requires:
      env: ["HYPERSPELL_API_KEY"]
---

## Overview

Search the customer's knowledge base via Hyperspell. This includes documents from connected sources (Google Drive, Notion, Slack, Gmail) and curated domain content uploaded to the customer's vault.

Hyperspell auto-injects relevant context before each AI turn when `autoContext: true` is enabled in the plugin config. Use this skill for explicit manual searches when the auto-context is insufficient.

## Steps

1. The gateway's Hyperspell plugin provides two tools:
   - `hyperspell_search` — search connected sources for relevant documents
   - `hyperspell_remember` — save information to the customer's memory vault

2. For knowledge lookups, use `hyperspell_search` with the user's query.

3. For saving important context, use `hyperspell_remember` with the text to save.

## Slash Commands

- `/getcontext <query>` — search for relevant context from connected sources
- `/remember <text>` — save text to the customer's Hyperspell vault
- `/sync` — manually sync workspace memory files to Hyperspell

## Output

Return the search results with source attribution (which document, which source).

## Error Handling

- If HYPERSPELL_API_KEY is not set: inform the user that knowledge base search is not configured
- If Hyperspell is unreachable: report "Knowledge base temporarily unavailable" and continue without context
