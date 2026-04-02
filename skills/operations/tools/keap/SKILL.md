---
name: keap-crm
description: "Search contacts, manage tags, trigger campaign sequences, and send emails via Keap CRM"
version: "1.0.0"
permissions:
  filesystem: none
  network: true
triggers:
  - command: /keap
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["node", "python3"]
      env: ["KEAP_ACCESS_TOKEN"]
      os: ["darwin", "linux"]
---

# Keap CRM Integration

Invoke Keap CRM operations through the MCP server wrapper. All 112 tools are available;
the quick reference below covers the most common intents.

## Quick Reference

| Intent | Tool | Approval |
|---|---|---|
| Find a contact by email or name | `keap_search_contacts` | safe |
| List all tags | `keap_list_tags` | safe |
| Get a specific contact | `keap_get_contact` | safe |
| List campaigns | `keap_list_campaigns` | safe |
| Get campaign details | `keap_get_campaign` | safe |
| Apply a tag to a contact | `keap_apply_tags` | requires approval |
| Remove a tag from a contact | `keap_remove_tags` | requires approval |
| Trigger a campaign sequence | `keap_trigger_campaign_sequence` | requires approval |
| Send an email to a contact | `keap_send_email` | requires approval |
| Opt-in a contact | `keap_opt_in_contact` | safe |
| Opt-out a contact | `keap_opt_out_contact` | safe |

## Invocation Pattern

```bash
# Call a specific tool with JSON arguments
python3 scripts/keap/invoke.py keap_search_contacts '{"email": "user@example.com"}'

# Trigger a campaign sequence for a contact
python3 scripts/keap/invoke.py keap_trigger_campaign_sequence '{"campaign_id": 123, "sequence_id": 1, "contact_id": 456}'

# List all available tools
python3 scripts/keap/invoke.py list_tools
```

Output is always valid JSON on stdout:
- Success: `{"result": {"content": [{"type": "text", "text": "..."}]}}`
- Tool list: `{"tools": [{"name": "...", "description": "..."}, ...]}`
- Error: `{"error": {"code": "<code>", "message": "..."}}`

## Tool Discovery

Run `python3 scripts/keap/invoke.py list_tools` to get the full list of 112 available tools
with their names, descriptions, and input schemas.

## Approval Gates

Operations are classified into two tiers:

### Safe (no approval required)
- All `keap_list_*` tools (list_tags, list_campaigns, list_contacts, etc.)
- All `keap_get_*` tools (get_contact, get_campaign, get_tag, etc.)
- All `keap_search_*` tools (search_contacts, etc.)
- `keap_opt_in_contact`, `keap_opt_out_contact`

### Requires Operator Approval
- All `keap_create_*` tools (create_contact, create_tag, etc.)
- All `keap_update_*` tools (update_contact, etc.)
- All `keap_delete_*` tools (delete_contact, delete_tag, etc.)
- `keap_apply_tags`, `keap_remove_tags`
- `keap_send_email`, `keap_send_marketing_email`
- `keap_trigger_campaign_sequence`
- Any bulk operation

Before executing a write operation, present the operation summary to the operator and
wait for explicit approval. Never batch multiple write operations without per-operation
confirmation.

## PII Rules

Contact records from Keap contain personally identifiable information (PII).

- **Never** log full contact records, email addresses, phone numbers, or names to `MEMORY.md`
- **Only** log contact IDs and operation results (e.g., "Applied tag 42 to contact 789")
- Raw payloads may only be written to `memory/drafts/` or `memory/logs/` directories
- When summarizing contacts for the operator, display only the minimum fields needed
- Never store Keap API responses containing PII in skill files or SOUL.md

## Logging

All write operations MUST be logged to `memory/logs/crm-writes/YYYY-MM-DD.md` with:

- Timestamp (ISO 8601)
- Tool name
- Contact ID (never full name or email)
- Operation result (success/failure)
- Error details if failed

Example log entry:
```markdown
## 2026-03-26T14:30:00Z — keap_apply_tags
- Contact: 789
- Tags applied: [42, 55]
- Result: success
```

Read operations are not logged unless they fail.

## Error Handling

| Error code | Meaning | Action |
|---|---|---|
| `auth_failed` | Keap token expired or invalid | Notify operator; do not retry |
| `timeout` | MCP server did not respond in time | Retry once; escalate if repeated |
| `process_error` | Node.js subprocess crashed | Check `node` installation; notify operator |
| `api_error` | Keap API returned an error | Log details; notify operator |
| `validation` | Bad arguments or protocol error | Fix arguments and retry |
