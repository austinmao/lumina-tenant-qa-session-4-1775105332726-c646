---
name: squarespace-forms
description: |
  Handles inbound Squarespace form submission webhooks for the organization retreat applications.
  Extracts submitter fields from the Squarespace label/value data array, then orchestrates
  downstream actions: create or update an Attio contact, add to a Resend audience, send a
  confirmation email, and post a Slack notification for the operator to review.
  Use this skill when a POST arrives at /webhook/squarespace or when the operator asks to process
  a retreat application that came in through the Squarespace website.
compatibility: Requires network access and SQUARESPACE_FORMS_API_KEY in .env
metadata:
  author: your-org
  version: "1.0"
  openclaw:
    emoji: 📝
    requires:
      env:
        - SQUARESPACE_FORMS_API_KEY
---

# Squarespace Forms

Squarespace POSTs a JSON payload to the configured webhook URL whenever a visitor submits
a form. This skill teaches Lumina how to parse that payload and trigger the full the organization
intake pipeline.

---

## Payload Shape

Squarespace does **not** send flat JSON keys. Every field arrives inside a `data` array of
`{ label, value }` objects. Never assume key names match field names — always iterate and
match on `label`.

```json
{
  "id": "abc123",
  "createdOn": "2026-02-25T10:00:00.000Z",
  "data": [
    { "label": "Name",    "value": "Jane Smith" },
    { "label": "Email",   "value": "jane@example.com" },
    { "label": "Phone",   "value": "+1 555 000 1234" },
    { "label": "Message", "value": "I'm interested in the spring retreat." }
  ]
}
```

**Key gotchas:**
- The `data` array is ordered by form field order, not alphabetically.
- Labels match the field label as configured in the Squarespace form builder — if the operator
  renames a field, the label changes here too.
- Values are always strings. Empty optional fields may be absent from the array or present
  with `"value": ""`.
- Squarespace cannot set custom HTTP headers, so signature verification is done via a
  `?secret=` query parameter on the webhook URL rather than an HMAC header.

---

## Field Extraction Pattern

```javascript
// TypeScript pattern — use this shape for all parsing logic
interface SquarespaceField {
  label: string;
  value: string;
}

interface SquarespacePayload {
  id: string;
  createdOn: string;
  data: SquarespaceField[];
}

function getField(data: SquarespaceField[], label: string): string {
  const field = data.find(
    (f) => f.label.toLowerCase().trim() === label.toLowerCase().trim()
  );
  return field?.value?.trim() ?? "";
}

// Usage
const name    = getField(payload.data, "Name");
const email   = getField(payload.data, "Email");
const phone   = getField(payload.data, "Phone");
const message = getField(payload.data, "Message");
```

Use **case-insensitive, trimmed** matching on `label` to guard against accidental
whitespace or capitalization differences in the Squarespace form builder.

---

## Operations Gate — Approval Requirements

**Safe to execute autonomously (no approval needed):**
- Parse and log the inbound payload
- Read the form submission fields
- Post a Slack notification to the operator so he can review the application

**Requires the operator's explicit approval in the current session before executing:**
- Creating or updating a contact record in Attio (write operation on CRM data)
- Adding a contact to a Resend audience (adds them to a mailing list)
- Sending a confirmation email to the applicant via Resend

**Exception — pre-authorized intake pipeline:**
When the webhook arrives via the configured proxy (POST to `/webhook/squarespace` with a
valid `?secret=` parameter), the `squarespace-form` webhook config in `config.json` treats
the full four-step pipeline as pre-authorized by the operator because he configured it.
Lumina should execute all four steps (Attio, Resend audience, confirmation email, Slack)
in a single automated response **only when triggered by a verified webhook**.
If the operator asks Lumina to "process this form" manually in Slack, stop after the Slack
notification and ask for explicit approval before writing to Attio or Resend.

---

## Downstream Actions (Intake Pipeline)

When the webhook fires, Lumina executes these four steps in order:

### 1. Attio — Create or Update Contact
- Object: `people`
- Set `name`, `email_addresses`, `phone_numbers`
- Set custom attribute `lead_status` to `"Applicant"` (if the attribute exists)
- Set custom attribute `lead_source` to `"Squarespace Form"` (if the attribute exists)
- If a record with the same email already exists, update it rather than creating a duplicate

### 2. Resend — Add to Audience
- Audience name: `Retreat Inquiries`
- Upsert the contact by email (Resend deduplicates by email within an audience)
- Set `first_name` from the Name field

### 3. Resend — Send Confirmation Email
- From: `hello@example-spaces.com`
- To: the applicant's email
- Subject: warm, spiritually-grounded — e.g. "Your path to the organization begins here"
- Body: acknowledge their inquiry, confirm we'll be in touch within 2–3 days, sign off as the organization
- Do not use generic corporate language; match the active brand voice

### 4. Slack — Notification to the operator
- Post to the configured Slack channel
- Include: applicant name, email, and full message text
- Format for easy review: name and email on one line, message indented as a block quote

---

## Quick-Start Extraction Example

```python
import json

# Simulated payload from Squarespace
payload = {
    "id": "abc123",
    "createdOn": "2026-02-25T10:00:00.000Z",
    "data": [
        {"label": "Name",    "value": "Jane Smith"},
        {"label": "Email",   "value": "jane@example.com"},
        {"label": "Phone",   "value": "+1 555 000 1234"},
        {"label": "Message", "value": "I'm interested in the spring retreat."}
    ]
}

def get_field(data, label):
    for f in data:
        if f["label"].strip().lower() == label.strip().lower():
            return f["value"].strip()
    return ""

data   = payload["data"]
name   = get_field(data, "Name")
email  = get_field(data, "Email")
phone  = get_field(data, "Phone")
msg    = get_field(data, "Message")

print(f"Name:    {name}")
print(f"Email:   {email}")
print(f"Phone:   {phone}")
print(f"Message: {msg}")
```

---

## Webhook URL Format

```
https://<tunnel-url>/webhook/squarespace?secret=<SQUARESPACE_FORMS_API_KEY>
```

Configure this URL in Squarespace under:
**Settings > Advanced > External API Keys > Form Webhook**

The `secret` query parameter is validated by the proxy (`webhook-proxy.js`) before the
request is forwarded to OpenClaw. Requests with a missing or incorrect secret are rejected
with HTTP 401 and never reach the gateway.
