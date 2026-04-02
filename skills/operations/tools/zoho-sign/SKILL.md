---
name: zoho-sign
description: Zoho Sign document signing via OAuth 2.0 — send templates for signature, track status, download signed PDFs.
compatibility: Requires network access and Zoho Sign OAuth credentials in .env
metadata:
  author: your-org
  version: "1.0"
  openclaw:
    emoji: "\u270D\uFE0F"
    requires:
      env:
        - ZOHO_SIGN_CLIENT_ID
        - ZOHO_SIGN_CLIENT_SECRET
        - ZOHO_SIGN_REFRESH_TOKEN
      bins: []
---

# Zoho Sign

Send documents for signature using Zoho Sign templates, track signing status, and download completed PDFs.

## Authentication

OAuth 2.0 with refresh token. Access tokens are fetched per invocation (never cached to disk).

- **Auth server**: `https://accounts.zoho.com/oauth/v2/token` (US region, configurable via `ZOHO_SIGN_REGION`)
- **Token type**: `Zoho-oauthtoken` (NOT `Bearer`)
- **Access token lifetime**: 1 hour
- **Refresh token lifetime**: Indefinite (unless revoked or unused for 90 days)

### First-time setup

**Option A — Self Client (recommended):**
1. Go to [Zoho API Console](https://api-console.zoho.com/) → Add Client → Self Client
2. Generate authorization code with scope: `ZohoSign.documents.ALL,ZohoSign.templates.ALL,ZohoSign.account.READ`
3. Run: `node scripts/zoho-sign/zoho-sign-oauth.js exchange <code>`
4. Add the printed `ZOHO_SIGN_REFRESH_TOKEN` to `.env`

**Option B — Server-based Application:**
1. Go to Zoho API Console → Add Client → Server-based Application
2. Set Homepage URL: `https://[the organization's domain]`
3. Set Redirect URI: `http://localhost:18791/oauth/zoho-sign/callback`
4. Run: `node scripts/zoho-sign/zoho-sign-oauth.js authorize`
5. Complete browser consent → refresh token prints to terminal → add to `.env`

**Verify:**
```bash
node scripts/zoho-sign/zoho-sign-oauth.js verify
```

## Operations Gate

### Safe (no approval needed)
- List templates
- Get template details
- Check signing request status
- List signing requests

### Requires approval
- Send a document for signature
- Download signed PDFs

## CLI Reference

All commands use the CLI at `scripts/zoho-sign/zoho-sign-cli.js`.

### List templates
```bash
node scripts/zoho-sign/zoho-sign-cli.js templates
```

### Get template details
```bash
node scripts/zoho-sign/zoho-sign-cli.js template-info <template_id>
```

### Send template for signing
```bash
node scripts/zoho-sign/zoho-sign-cli.js send <template_id> <recipient_email> <recipient_name> [--field key=value ...]
```

Example with prefill fields:
```bash
node scripts/zoho-sign/zoho-sign-cli.js send 12345 participant@example.com "Jane Doe" \
  --field "Retreat Date=March 2026" \
  --field "Location=Sacred Valley"
```

### Check signing status
```bash
node scripts/zoho-sign/zoho-sign-cli.js status <request_id>
```

### Download signed PDF
```bash
node scripts/zoho-sign/zoho-sign-cli.js download <request_id> /tmp/signed-document.pdf
```

### List signing requests
```bash
node scripts/zoho-sign/zoho-sign-cli.js list-requests
node scripts/zoho-sign/zoho-sign-cli.js list-requests --status completed
```

Status values: `completed`, `inprogress`, `recalled`, `declined`, `expired`

## API Reference

- **Base URL**: `https://sign.zoho.com/api/v1/` (US region)
- **Auth header**: `Authorization: Zoho-oauthtoken <access_token>`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/templates` | GET | List all templates |
| `/templates/{id}` | GET | Get template details |
| `/templates/{id}/createdocument` | POST | Send template for signing |
| `/requests` | GET | List signing requests |
| `/requests/{id}` | GET | Get request status |
| `/requests/{id}/pdf` | GET | Download signed PDF |

## Region Configuration

Set `ZOHO_SIGN_REGION` in `.env` to match your Zoho data center:

| Region | Auth Domain | API Domain |
|--------|------------|------------|
| `us` (default) | accounts.zoho.com | sign.zoho.com |
| `eu` | accounts.zoho.eu | sign.zoho.eu |
| `in` | accounts.zoho.in | sign.zoho.in |
| `au` | accounts.zoho.com.au | sign.zoho.com.au |
| `jp` | accounts.zoho.jp | sign.zoho.jp |

## Signing Workflow

The intended pipeline for the organization participant documents:

```
Squarespace form → OpenClaw webhook → Lumina
  → Zoho Sign: send template for signing (this skill)
  → Zoho Sign webhook: signing completed
  → Zoho Sign: download signed PDF (this skill)
  → File to Cloudflare R2 or Google Drive
  → Update Attio CRM record
  → Notify via Slack
```

## Webhook Events

Zoho Sign delivers signing lifecycle events to the proxy at `POST /webhook/zoho-sign` (port 18790). The proxy verifies the HMAC signature and forwards authenticated events to OpenClaw at `/webhook/zoho-sign-event`.

### Registering the webhook in Zoho Sign UI

1. Go to [Zoho Sign](https://sign.zoho.com) → Settings → Webhooks
2. Click "Add Webhook"
3. **Notification URL**: `https://<your-tunnel-domain>/webhook/zoho-sign`
4. **Secret key**: the value of `ZOHO_SIGN_WEBHOOK_SECRET` from `.env`
5. Select event types: all document events (sent, viewed, signed, declined, expired, completed, recalled)

### Signature verification

Zoho Sign sends the header:
```
X-Zoho-Webhook-Signature: t=<unix_timestamp>,v=<hmac_hex>
```

The HMAC is computed as:
```
HMAC-SHA256(key=ZOHO_SIGN_WEBHOOK_SECRET, message="${timestamp}.${rawBody}")
```

The proxy verifies this using `crypto.timingSafeEqual` before forwarding. Requests with missing or invalid signatures are rejected with 401.

### Payload structure

```json
{
  "notifications": {
    "operation_type": "RequestCompleted",
    "operation_time": "2026-02-26T12:00:00Z"
  },
  "requests": {
    "request_id": "3000000001234",
    "request_name": "the organization Participant Agreement",
    "request_status": "completed",
    "actions": [
      {
        "action_type": "SIGN",
        "signing_order": 1,
        "status": "SIGNED",
        "email_id": "participant@example.com"
      }
    ]
  }
}
```

### Event types (`notifications.operation_type`)

| Value | When fired |
|-------|-----------|
| `RequestSent` | Document sent for signature |
| `RequestViewed` | Signer opened the document |
| `RequestSigned` | One signer completed signing (may still be in progress for multi-signer flows) |
| `RequestDeclined` | Signer declined to sign |
| `RequestExpired` | Document passed its expiry date without completion |
| `RequestCompleted` | All signers completed — document is fully executed |
| `RequestRecalled` | Sender recalled (cancelled) the document |

### Document status values (`requests.request_status`)

| Value | Meaning |
|-------|---------|
| `inprogress` | Awaiting one or more signatures |
| `completed` | All signatures collected |
| `declined` | At least one signer declined |
| `expired` | Passed expiry without completion |
| `recalled` | Recalled by sender |

## Verification

```bash
# Verify OAuth credentials are valid
node scripts/zoho-sign/zoho-sign-oauth.js verify

# List templates (confirms API access)
node scripts/zoho-sign/zoho-sign-cli.js templates

# Full send test (use a test template)
node scripts/zoho-sign/zoho-sign-cli.js send <test_template_id> your@email.com "Test User"
```
