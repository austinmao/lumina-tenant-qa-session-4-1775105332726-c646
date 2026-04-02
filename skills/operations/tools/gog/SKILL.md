---
name: gog
description: |
  Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
  Covers read operations (search, get, export) and write operations (send, reply,
  sheets update). Use this skill for any Gmail inbox operation, direct 1:1 Gmail
  replies from info@[the organization's domain] or lumina@[the organization's domain], and Google
  Sheets/Docs/Calendar access. For bulk or transactional HTML email (onboarding
  sequences, marketing campaigns), use the Resend skill instead.
compatibility: Requires gog binary (brew install steipete/tap/gogcli), OAuth credentials for each account.
metadata:
  author: your-org
  version: "1.1"
  openclaw:
    emoji: "📬"
    requires:
      env:
        - GOG_ACCOUNT
        - GOG_KEYRING_PASSWORD
      bins:
        - gog
---

# gog

Use `gog` for Gmail/Calendar/Drive/Contacts/Sheets/Docs. Requires OAuth setup.

## Org Constants

All email addresses below are sourced from `config/org.yaml`. Load the `org-config` skill
or read `config/org.yaml` to look up canonical values before using this skill:

| Constant | org.yaml key | Env var |
|---|---|---|
| Primary inbox | `contact.email` | `ORG_INFO_EMAIL` |
| Agent inbox | `contact.agent_email` | `ORG_AGENT_EMAIL` |

Shell commands use `${ORG_INFO_EMAIL:-info@[the organization's domain]}` so the fallback
applies if the env var is not set. Set `ORG_INFO_EMAIL` and `ORG_AGENT_EMAIL` in
`~/.openclaw/.env` to override for a different org.

## Operations Gate

**Safe to run autonomously (read-only):**
- Search and read email threads
- Fetch calendar events
- Read Sheets, Docs, Drive files
- List contacts

**Requires the operator's explicit per-action approval:**
- Send any email (new compose or reply)
- Create calendar events
- Modify or delete any Sheets/Docs content
- Archive, delete, or label messages

---

## Pre-Send Validation (mandatory before every `gog gmail send`)

```bash
BODY_LEN=$(wc -c < /tmp/gmail-body.txt 2>/dev/null || echo 0)
grep -qiE '^(test|hi|hello|draft|placeholder)$' /tmp/gmail-body.txt 2>/dev/null && \
  { echo "ERROR: placeholder body. Abort."; exit 1; }
[ "$BODY_LEN" -lt 50 ] && { echo "ERROR: body too short (${BODY_LEN}c). Abort."; exit 1; }
```

Run this block immediately before every send command. Do not proceed if either check fails.

---

## Setup (once per account)

```bash
gog auth credentials /path/to/client_secret.json
gog auth add "${ORG_INFO_EMAIL:-info@[the organization's domain]}" --services gmail,calendar,drive,contacts,sheets,docs
gog auth add "${ORG_AGENT_EMAIL:-lumina@[the organization's domain]}" --services gmail,calendar,drive,contacts,sheets,docs
gog auth list
```

---

## Common Commands

- Gmail search: `gog gmail search 'newer_than:7d' --max 10`
- Gmail read thread: `gog gmail thread get <threadId> --json`
- Gmail read message: `gog gmail get <messageId> --format full --json`
- Calendar: `gog calendar events <calendarId> --from <iso> --to <iso>`
- Drive search: `gog drive search "query" --max 10`
- Contacts: `gog contacts list --max 20`
- Sheets get: `gog sheets get <sheetId> "Tab!A1:D10" --json`
- Sheets update: `gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED`
- Sheets append: `gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS`
- Sheets clear: `gog sheets clear <sheetId> "Tab!A2:Z"`
- Sheets metadata: `gog sheets metadata <sheetId> --json`
- Docs export: `gog docs export <docId> --format txt --out /tmp/doc.txt`
- Docs cat: `gog docs cat <docId>`

---

## Gmail Reply Format — Direct 1:1 Replies

### When to use gog vs Resend

| Scenario | Tool |
|---|---|
| Replying 1:1 to an inbound email in info@ or lumina@ | **gog** |
| Sending a bulk/transactional sequence (onboarding, marketing, sales) | **Resend** |
| Sending a formatted HTML email to a single person for the first time | **Resend** |
| Quick follow-up after a call, short personal note, status update | **gog** |

The dividing line: if the email is a reply to something the recipient already sent
to the organization, use gog. If the organization is initiating a send to someone who has not
just written in, use Resend.

### Format rule: plain text for direct replies

Direct 1:1 Gmail replies from info@ or lumina@ use **plain text only** (`--body`).
Do not use `--body-html` for conversational replies. Reasons:

- Plain text matches the register of a personal reply. A React-Email-style HTML
  template in a reply to someone's handwritten question reads as cold and robotic.
- Gmail renders plain text replies cleanly in all clients, including mobile.
- Full HTML in a reply (even minimal `<div>` + inline styles) can trigger Gmail's
  "clipping" warning on long messages and increases spam score.
- the active brand voice is warm and direct — plain prose carries that better than
  a designed template.

**Exception:** If the reply contains a structured comparison (pricing tiers,
retreat schedule options, a checklist) that genuinely requires a table or bold
headings to be readable, use `--body-html` with minimal inline-styled HTML only.
No external CSS, no `<style>` blocks, no background images. See "Minimal HTML"
section below.

### Plain text reply — canonical form (safe multiline)

```bash
cat >/tmp/gmail-body.txt <<'EOF'
Hi Sarah,

Thank you for reaching out. [Reply body in the active brand voice — warm, grounded, specific.]

Warmly,
The the organization Team
EOF

BODY_LEN=$(wc -c < /tmp/gmail-body.txt 2>/dev/null || echo 0)
grep -qiE '^(test|hi|hello|draft|placeholder)$' /tmp/gmail-body.txt 2>/dev/null && { echo "ERROR: placeholder body. Abort."; exit 1; }
[ "$BODY_LEN" -lt 50 ] && { echo "ERROR: body too short (${BODY_LEN}c). Abort."; exit 1; }

GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" \
gog gmail send \
  --account "$GOG_ACCOUNT" \
  --from "${ORG_INFO_EMAIL:-info@[the organization's domain]}" \
  --to "recipient@example.com" \
  --subject "Re: Their subject line" \
  --reply-to-message-id "<their-message-id>" \
  --body-file /tmp/gmail-body.txt \
  --no-input
```

Key points:
- `--reply-to-message-id` takes the raw RFC 2822 Message-ID from the inbound
  message (with angle brackets, e.g. `<abc123@mail.gmail.com>`). gog sets both
  `In-Reply-To` and `References` headers and places the reply in the correct
  Gmail thread automatically.
- `--subject` should be `Re: <original subject>`. If the original subject already
  starts with `Re:`, keep it as-is — do not double-prefix.
- `--from` must be a verified send-as alias on the account. info@ and lumina@ are
  both configured as send-as aliases on the operator's Google Workspace account.
- `--no-input` prevents interactive prompts — required when running from an
  agent context.
- Never include `--quote` unless the operator explicitly requests the quoted thread.
  Quoted text adds noise to 1:1 replies and is not the organization's style.
- Do not use shell-escaped newline strings like `\n` in a `--body "..."` value.
  Use `--body-file` (preferred) so line breaks are always rendered correctly.
- Default to plain text without markdown. Do not include markdown syntax (`**`,
  `#`, backticks, list markers) unless the operator explicitly asks for markdown.

### How to extract the Message-ID from an inbound message

When email-triage reads a thread with `gog gmail thread get <threadId> --json`,
the JSON includes a `messages[]` array. Each message has a `payload.headers[]`
array. The Message-ID is in the header named `Message-ID`:

```python
import json, subprocess, os

result = subprocess.run(
    ['gog', 'gmail', 'thread', 'get', thread_id, '--json', '--results-only',
     '--account', os.environ['GOG_ACCOUNT']],
    capture_output=True, text=True,
    env={**os.environ, 'GOG_KEYRING_PASSWORD': os.environ['GOG_KEYRING_PASSWORD']}
)
thread = json.loads(result.stdout)

# Get the Message-ID from the latest message in the thread
latest_message = thread['messages'][-1]
headers = latest_message['payload']['headers']
message_id = next(h['value'] for h in headers if h['name'] == 'Message-ID')
# message_id is now e.g. "<CABcD12EFgHiJ@mail.gmail.com>" — pass directly to --reply-to-message-id
```

Alternatively, use `gog gmail get <messageId> --format metadata --headers Message-ID --json`.

### Sending from lumina@ vs info@

Both addresses are send-as aliases configured on the operator's Google Workspace account.
Set `GOG_ACCOUNT` to the account that owns the OAuth token (the operator's primary account),
then pass `--from` to specify which alias to use:

- Participant-facing replies: `--from "info@[the organization's domain]"`
- Sales-context replies (Lumina persona): `--from "${ORG_AGENT_EMAIL:-lumina@[the organization's domain]}"`

### Reply-all (when the original was sent to multiple people)

If the inbound message had multiple recipients and the reply should go to all of
them, use `--reply-all` instead of `--to`:

```bash
GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" \
gog gmail send \
  --account "$GOG_ACCOUNT" \
  --from "${ORG_INFO_EMAIL:-info@[the organization's domain]}" \
  --subject "Re: Their subject line" \
  --reply-to-message-id "<their-message-id>" \
  --reply-all \
  --body "Body text here." \
  --no-input
```

`--reply-all` auto-populates `--to` and `--cc` from the original message.
Use it only when the inbound email was a group message and a group reply is
appropriate. For most participant 1:1 replies, use explicit `--to`.

### Minimal HTML — when it is appropriate

Only use `--body-html` for a direct reply when the content has genuine structure
that plain text cannot represent clearly (a pricing table, a multi-column
schedule, a numbered checklist with bold headings). When using HTML:

1. No `<style>` blocks — Gmail strips them in reply context.
2. No external CSS. All styles must be inline on each element.
3. No background images or web fonts.
4. No React Email. Write raw HTML with inline styles only.
5. Always include a `--body` plain text fallback alongside `--body-html`.
   Some clients (and accessibility tools) display the plain text part.

Minimal HTML pattern for a simple structured reply:

```bash
GOG_KEYRING_PASSWORD="$GOG_KEYRING_PASSWORD" \
gog gmail send \
  --account "$GOG_ACCOUNT" \
  --from "${ORG_INFO_EMAIL:-info@[the organization's domain]}" \
  --to "recipient@example.com" \
  --subject "Re: Their subject line" \
  --reply-to-message-id "<their-message-id>" \
  --body "Hi Sarah,

Here is the retreat schedule overview:

April 7 (Day 1): Arrival and orientation, 3–7pm
April 8 (Day 2): Full day — 9am to 9pm
April 9 (Day 3): Integration and departure, 9am to 1pm

[Rest of plain text reply]

Warmly,
The the organization Team" \
  --body-html '<div style="font-family:Georgia,serif;font-size:15px;line-height:1.6;color:#333;max-width:600px;">
<p>Hi Sarah,</p>
<p>Here is the retreat schedule overview:</p>
<table style="border-collapse:collapse;width:100%;">
  <tr><td style="padding:6px 12px;border:1px solid #ddd;font-weight:bold;">April 7 (Day 1)</td><td style="padding:6px 12px;border:1px solid #ddd;">Arrival and orientation, 3–7pm</td></tr>
  <tr><td style="padding:6px 12px;border:1px solid #ddd;font-weight:bold;">April 8 (Day 2)</td><td style="padding:6px 12px;border:1px solid #ddd;">Full day — 9am to 9pm</td></tr>
  <tr><td style="padding:6px 12px;border:1px solid #ddd;font-weight:bold;">April 9 (Day 3)</td><td style="padding:6px 12px;border:1px solid #ddd;">Integration and departure, 9am to 1pm</td></tr>
</table>
<p>[Rest of reply]</p>
<p>Warmly,<br>The the organization Team</p>
</div>' \
  --no-input
```

Font used: `Georgia, serif` — matches the active brand voice (warm, human).
Max width: 600px on the outer div. Body background: none (reply context, not compose).
The `<table>` inline style uses `border-collapse:collapse` — the only reliably
rendered table style across Gmail clients.

---

## Notes

- Set `GOG_ACCOUNT=you@gmail.com` to avoid repeating `--account`.
- For scripting, prefer `--json` plus `--no-input`.
- Sheets values can be passed via `--values-json` (recommended) or as inline rows.
- Docs supports export/cat/copy. In-place edits require a Docs API client (not in gog).
- Never send email without the operator's explicit per-message approval. Draft first,
  present the draft and the exact command, wait for "send" confirmation.
- After sending, log the send to `memory/logs/sends/YYYY-MM-DD.md`:
  `- {ISO timestamp} | type: gmail-reply | account: {from} | to: {recipient} | subject: {subject} | thread: {threadId}`
