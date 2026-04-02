---
name: whatsapp-group-indexer
description: "Index and log incoming WhatsApp group messages for search"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /search-group
metadata:
  openclaw:
    emoji: "💬"
    requires:
      bins: ["jq"]
---

# WhatsApp Group Indexer

Logs all incoming messages from the Awaken Apr 2026 staff group to a searchable daily log. Runs automatically on every inbound group message.

## Group Registry

| Group Name | JID | Log Path |
|---|---|---|
| Awaken Apr 2026 | `120363423692271199@g.us` | `memory/logs/whatsapp-groups/awaken-apr-2026/` |

## Auto-Index on Inbound Message

When a message arrives from the Awaken Apr 2026 group (`120363423692271199@g.us`), BEFORE doing anything else:

1. Determine today's date: `date +%Y-%m-%d`
2. Append to `memory/logs/whatsapp-groups/awaken-apr-2026/YYYY-MM-DD.md`:

```
## HH:MM — <Sender Name or number>

<message body>

---
```

3. If the message is a media file (image, voice note, document), log: `[media: <type>] <caption if any>`
4. Do NOT respond to the group unless the message explicitly @mentions you or asks a question.

## Search Command: /search-group

When the operator says `/search-group <query>` or "search the Awaken group for <query>":

1. Run: `grep -r -i "<query>" memory/logs/whatsapp-groups/awaken-apr-2026/ --include="*.md" -A2 -B1`
2. Return matching excerpts with date and sender context.
3. If no results: "No messages matching '<query>' found in the Awaken Apr 2026 group logs."

## Silence Rules

- Do NOT reply to every group message — only when @mentioned or responding to a direct question.
- Log EVERY message regardless of whether you respond.
- Never post the log contents back into the group.
