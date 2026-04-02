---
name: resend-log-to-attio
description: >
  Log a Resend email send as an Attio note and local send-log entry. Use this
  skill immediately after every successful Resend send from lumina@[the organization's domain] —
  provides the contact lookup, note creation, and local log write steps in order.
version: "1.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /log-email-send
metadata:
  openclaw:
    emoji: "📋"
    requires:
      env:
        - ATTIO_API_KEY
        - RESEND_API_KEY
      bins:
        - curl
        - jq
        - python3
---

# Resend → Attio Send Logger

## Purpose

After every email sent from lumina@[the organization's domain] via Resend, write:

1. **An Attio note** on the recipient's People record (or deal record if one
   exists and the context is deal-related)
2. **A local send-log entry** in `memory/logs/sends/YYYY-MM-DD.md`

This is a mandatory post-send step for all outbound sends — not optional.
It gives the organization a complete CRM audit trail synchronized with Resend delivery IDs.

---

## Operations Gate

**Safe to execute autonomously (no the operator approval required):**
- `POST /v2/objects/people/records/query` — look up contact by email
- `GET /v2/notes` — read existing notes on a record

**Requires the operator's explicit approval in the current session:**
- `POST /v2/notes` — creates a new note on a CRM record
  Exception: Lumina's SOUL.md grants standing approval for post-send logging.
  Log all note creations to `memory/logs/crm-writes/YYYY-MM-DD.md` as required
  by the attio skill rules.

---

## When to Execute This Skill

Execute immediately after every successful Resend API call that returns a
non-error response containing a `data.id` (Resend email ID). Do not execute
on failed sends. Do execute on partial successes — log what was sent.

Triggers:
- After any send in `sales-sequences` (Triggers 1–4)
- After any onboarding email (programs/onboarding domain)
- After any test send that uses lumina@[the configured sending domain] as sender
- After any Gmail/GOG send from lumina@[the organization's domain] (log to Attio with
  `channel: email(gog)` instead of `channel: resend`)

---

## Step-by-Step Procedure

### Step 1 — Collect required values before calling this skill

Have these values ready before starting:

| Value | Source |
|---|---|
| `recipient_email` | The `to` address of the sent email |
| `subject` | Subject line of the sent email |
| `resend_id` | The `data.id` field from the Resend API response |
| `template_name` | Template or sequence name (e.g., "sales-welcome", "welcome-onboarding") |
| `send_context` | Which sequence/trigger this is (e.g., "Trigger 1 — Lead Capture") |
| `rep_email` | Assigned rep who was CC'd (or "none" for no-rep sends) |
| `sent_at` | ISO 8601 UTC timestamp (e.g., "2026-03-01T14:30:00Z") |
| `body` | Full plaintext email body — appended to the note under a `Body:` header |

### Step 2 — Look up the Attio People record by email

```bash
python3 <<'PYEOF'
import urllib.request, urllib.parse, os, json, sys

BASE = 'https://api.attio.com/v2'
TOKEN = os.environ['ATTIO_API_KEY']
recipient_email = os.environ.get('LOG_RECIPIENT_EMAIL', '')

if not recipient_email:
    print('ERROR: LOG_RECIPIENT_EMAIL not set', file=sys.stderr)
    sys.exit(1)

payload = {
    'filter': {
        'email_addresses': {
            '$eq': recipient_email
        }
    },
    'limit': 1
}
data = json.dumps(payload).encode()
req = urllib.request.Request(f'{BASE}/objects/people/records/query', data=data)
req.add_header('Authorization', f'Bearer {TOKEN}')
req.add_header('Content-Type', 'application/json')

try:
    result = json.load(urllib.request.urlopen(req))
    records = result.get('data', [])
    if records:
        print(records[0]['id']['record_id'])
    else:
        print('NOT_FOUND')
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
PYEOF
```

**If result is `NOT_FOUND`:** The recipient has no Attio People record yet.
Do one of the following, in order:
1. If this is a Trigger 1 send (new lead), the contact should have been created
   before the send. Go back and create the contact via the deal-management skill,
   then retry the lookup.
2. If this is an onboarding send (not a sales lead), skip the Attio note
   but still write the local send-log entry. Log `attio_note: skipped (no record)`.
3. Never create a new Attio People record solely to log an email — that is
   the pipeline-triggers / deal-management skill's job.

**If result is a UUID:** That is the `record_id` for Step 3.

### Step 3 — Write the Attio note

Note format matches the touchpoint format defined in `deal-management`:

```
[YYYY-MM-DD HH:MM UTC] Email touchpoint
From: lumina@[the configured sending domain]
To: <recipient_email>
Subject: <subject>
Channel: Resend
Resend ID: <resend_id>
Template: <template_name>
Context: <send_context>
Rep CC: <rep_email>

Body:
<full plaintext email body>
```

```bash
python3 <<'PYEOF'
import urllib.request, os, json, sys

BASE = 'https://api.attio.com/v2'
TOKEN = os.environ['ATTIO_API_KEY']

record_id     = os.environ.get('LOG_RECORD_ID', '')
recipient     = os.environ.get('LOG_RECIPIENT_EMAIL', '')
subject_line  = os.environ.get('LOG_SUBJECT', '')
resend_id     = os.environ.get('LOG_RESEND_ID', '')
template      = os.environ.get('LOG_TEMPLATE', 'unknown')
context       = os.environ.get('LOG_CONTEXT', 'unspecified')
rep           = os.environ.get('LOG_REP_EMAIL', 'none')
sent_at       = os.environ.get('LOG_SENT_AT', '')
body          = os.environ.get('LOG_BODY', '')

required = {'LOG_RECORD_ID': record_id, 'LOG_RECIPIENT_EMAIL': recipient,
            'LOG_SUBJECT': subject_line, 'LOG_RESEND_ID': resend_id,
            'LOG_SENT_AT': sent_at}
missing = [k for k, v in required.items() if not v]
if missing:
    print(f'ERROR: missing env vars: {missing}', file=sys.stderr)
    sys.exit(1)

# Timestamp formatted to minute precision for note body
ts = sent_at[:16].replace('T', ' ')

note_content = (
    f'[{ts} UTC] Email touchpoint\n'
    f'From: lumina@[the configured sending domain]\n'
    f'To: {recipient}\n'
    f'Subject: {subject_line}\n'
    f'Channel: Resend\n'
    f'Resend ID: {resend_id}\n'
    f'Template: {template}\n'
    f'Context: {context}\n'
    f'Rep CC: {rep}'
)
if body:
    note_content += f'\n\nBody:\n{body}'

payload = {
    'data': {
        'format': 'plaintext',
        'title': f'Email sent — {subject_line[:60]}',
        'content': note_content,
        'parent_object': 'people',
        'parent_record_id': record_id
    }
}

data = json.dumps(payload).encode()
req = urllib.request.Request(f'{BASE}/notes', data=data)
req.add_header('Authorization', f'Bearer {TOKEN}')
req.add_header('Content-Type', 'application/json')

try:
    result = json.load(urllib.request.urlopen(req))
    note_id = result.get('data', {}).get('id', {}).get('note_id', 'unknown')
    print(f'OK: note_id={note_id}')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'ERROR: HTTP {e.code} — {body}', file=sys.stderr)
    sys.exit(1)
PYEOF
```

### Step 4 — Write the local send-log entry

Append to `memory/logs/sends/YYYY-MM-DD.md` (create the file if it does not
exist for today). Use this exact one-line format to match existing log entries:

```
- <sent_at> | type: <template_name> | to: <recipient_email> | resend_id: <resend_id> | context: <send_context> | attio_record: <record_id> | attio_note: <note_id>
```

If no Attio record was found (Step 2 returned NOT_FOUND), use:
```
- <sent_at> | type: <template_name> | to: <recipient_email> | resend_id: <resend_id> | context: <send_context> | attio_record: none | attio_note: skipped (no record)
```

### Step 5 — Write the CRM-writes audit entry

Append to `memory/logs/crm-writes/YYYY-MM-DD.md`:

```
- <sent_at> | method: POST | endpoint: /v2/notes | record: people/<record_id> | desc: Email send note — <template_name> — resend_id: <resend_id>
```

---

## Deal-Level Logging (when a deal record exists)

When the send context is deal-related (Trigger 3 follow-up, Trigger 4
stage-action emails, proposal follow-up, etc.) and a deal record ID is known,
write a second note on the **deal record** in addition to the People note:

- Use `parent_object: deals` and `parent_record_id: <deal_record_id>`
- Note content is identical to the People note
- Log both note IDs in the CRM-writes audit entry:
  `desc: Email send note — <template_name> — people/<people_note_id> + deals/<deal_note_id>`

If a deal record ID is not known (Trigger 1 welcome, onboarding sends), skip
the deal-level note. Do not create a placeholder deal.

---

## Error Handling

| Scenario | Action |
|---|---|
| Attio lookup returns NOT_FOUND | Skip Attio note; write local log with `attio_note: skipped (no record)`; continue |
| Attio note POST returns 401 | Stop; notify the operator: "ATTIO_API_KEY invalid or revoked"; do not retry |
| Attio note POST returns 403 | Stop; notify the operator: "token missing note:write scope"; do not retry |
| Attio note POST returns 429 | Wait 2 seconds; retry once; if still 429, skip note and log the failure |
| Attio note POST returns 5xx | Skip note; write local log with `attio_note: failed (5xx)`; notify the operator |
| `ATTIO_API_KEY` env var missing | Stop; notify the operator: "ATTIO_API_KEY not set in .env" |

Never let a logging failure block the confirmation to the operator that the email was sent.
The send already happened — log failure is a non-blocking side effect.

---

## Environment Variables Required

| Variable | Purpose |
|---|---|
| `ATTIO_API_KEY` | Personal access token with `record:read`, `note:read`, `note:write` scopes |
| `RESEND_API_KEY` | Already required for the send itself; referenced here for completeness |

Both variables are already defined in `.env` and `.env.example`.
No new environment variables are introduced by this skill.

---

## Checklist — Before Logging Any Note

- [ ] Resend API returned a successful response with a non-empty `data.id`
- [ ] Recipient email address is a real address (not a Resend test address like `delivered@resend.dev`)
- [ ] `ATTIO_API_KEY` is set and has `note:write` scope
- [ ] Attio People lookup completed before attempting note write
- [ ] Note content contains no medical intake data (HIPAA)
- [ ] Note content contains no API keys or env var values
- [ ] Local send-log and CRM-writes log entries written after Attio note confirms

---

## Skill Dependency Map

```
resend (parent)           →  sends email, returns resend_id
resend/log-to-attio       →  called after every send; writes Attio note + local logs
deal-management           →  consumes: touchpoint format defined here
pipeline-triggers         →  triggers that invoke resend; all four trigger resend → log-to-attio
sales-sequences           →  sequences that send via resend; all sequences → log-to-attio
```
