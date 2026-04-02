---
name: workspace-admin
description: "Onboard or offboard a Google Workspace employee — create account, transfer Drive/Calendar data, set up Gmail delegation, suspend account"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /offboard-employee-google-workspace
  - command: /onboard-employee-google-workspace
metadata:
  openclaw:
    emoji: "🔑"
    requires:
      bins:
        - gws
        - gcloud
        - curl
        - jq
        - python3
      env:
        - GWS_SA_EMAIL
---

# Google Workspace Admin Skill

Onboard new team members and offboard departing ones via the Google Workspace
Admin SDK. Covers user creation/suspension, Drive + Calendar data transfer,
Gmail delegation, and vacation responder — all without requiring the target
user's password or 2FA.

---

## Environment Variables

| Variable | Value |
|---|---|
| `GWS_SA_EMAIL` | Service account email, e.g. `workspace-offboarding@PROJECT.iam.gserviceaccount.com` |

The service account needs **Domain-Wide Delegation** granted in Admin Console
and the caller (austin@) needs `roles/iam.serviceAccountTokenCreator` on it.
No JSON key file required — the signJwt approach avoids the org policy that
blocks key creation. See One-Time Setup below.

---

## Auth — Run Before Every Session

The gws token expires and will fail with `invalid_rapt`. Check first:

```bash
gws auth status | jq '{token_valid, token_error}'
```

If `token_valid` is false, re-authenticate:

```bash
gws auth login --scopes \
  https://www.googleapis.com/auth/admin.directory.user,\
  https://www.googleapis.com/auth/admin.datatransfer,\
  https://www.googleapis.com/auth/gmail.settings.sharing,\
  https://www.googleapis.com/auth/gmail.settings.basic
```

Sign in as `austin@[the organization's domain]`. Then get a live access token:

```bash
CREDS=$(gws auth export --unmasked)
# NOTE: gws auth export returns {client_id, client_secret, refresh_token} —
# NOT a ready-to-use access_token. Must exchange the refresh token:
ADMIN_TOKEN=$(curl -sS -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$(echo $CREDS | jq -r '.client_id')" \
  -d "client_secret=$(echo $CREDS | jq -r '.client_secret')" \
  -d "refresh_token=$(echo $CREDS | jq -r '.refresh_token')" \
  -d "grant_type=refresh_token" | jq -r '.access_token')
```

Verify the token has the scopes you need:

```bash
curl -sS "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=$ADMIN_TOKEN" \
  | jq '.scope' | tr ' ' '\n' | grep -E "directory|datatransfer|gmail"
```

---

## DWD Token — Required for Gmail Operations

Gmail delegation requires impersonating the target user, not authenticating
as the admin. Use the IAM signJwt API (no SA key file needed):

```bash
# Generate token impersonating SOURCE_USER with a given scope
get_dwd_token() {
  local subject="$1"
  local scope="$2"
  python3 scripts/gws_dwd_token.py "$GWS_SA_EMAIL" "$subject" "$scope"
}
```

`scripts/gws_dwd_token.py` is in this repo. It uses `gcloud auth print-access-token`
to call the IAM Credentials API signJwt endpoint, then exchanges the signed
JWT for an OAuth2 access token. No key file. Works around the org policy
`iam.disableServiceAccountKeyCreation`.

---

## /offboard-user

Offboard a departing team member. Transfers Drive + Calendar data to a
destination account, sets up Gmail delegation, sets OOO, and suspends the
account.

**Usage**: `/offboard-user SOURCE_EMAIL DEST_EMAIL`

Example: `/offboard-user liv@[the organization's domain] info@[the organization's domain]`

### Step 1 — Resolve User IDs

`gws` does NOT expose the Admin SDK Directory API. Use curl directly:

```bash
DIR="https://admin.googleapis.com/admin/directory/v1/users"
SOURCE_ID=$(curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  "$DIR/$SOURCE_EMAIL?projection=basic" | jq -r '.id')
DEST_ID=$(curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  "$DIR/$DEST_EMAIL?projection=basic" | jq -r '.id')
echo "Source: $SOURCE_ID   Dest: $DEST_ID"
```

If either returns empty, the token is missing `admin.directory.user` scope —
re-run `gws auth login` with that scope and re-export the token.

### Step 2 — Data Transfer (Drive + Calendar)

`gws` does NOT expose the Data Transfer API. Use curl directly:

```bash
DT="https://admin.googleapis.com/admin/datatransfer/v1"

# Discover available app IDs for this domain
APP_LIST=$(curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  "$DT/applications?customerId=my_customer")
echo $APP_LIST | jq '.applications[] | "\(.id)\t\(.name)"'

# Extract Drive and Calendar IDs dynamically
DRIVE_ID=$(echo $APP_LIST | jq -r '.applications[] | select(.name|test("Drive";"i")) | .id' | head -1)
CAL_ID=$(echo $APP_LIST | jq -r '.applications[] | select(.name|test("Calendar";"i")) | .id' | head -1)

# Create transfer
TRANSFER=$(curl -sS -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"oldOwnerUserId\": \"$SOURCE_ID\",
    \"newOwnerUserId\": \"$DEST_ID\",
    \"applicationDataTransfers\": [
      {\"applicationId\": \"$DRIVE_ID\", \"applicationTransferParams\": [{\"key\": \"PRIVACY_LEVEL\", \"value\": [\"PRIVATE\",\"SHARED\"]}]},
      {\"applicationId\": \"$CAL_ID\",  \"applicationTransferParams\": [{\"key\": \"RELEASE_RESOURCES\", \"value\": [\"TRUE\"]}]}
    ]
  }" \
  "$DT/transfers")
TRANSFER_ID=$(echo $TRANSFER | jq -r '.id')
echo "Transfer ID: $TRANSFER_ID"
```

Poll status (completes in 1–10 min for typical accounts):

```bash
curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  "$DT/transfers/$TRANSFER_ID" | jq '{overallTransferStatusCode, applicationDataTransfers: [.applicationDataTransfers[].applicationTransferStatus]}'
```

If the token is missing `admin.datatransfer` scope, re-run `gws auth login`
and add that scope before re-exporting the token.

### Step 3 — Gmail Delegation

Gives DEST_EMAIL read/send/delete access to SOURCE_EMAIL's mailbox.
Requires DWD (impersonates SOURCE so the delegate is set to `accepted`
immediately — no verification email sent to SOURCE).

```bash
DWD_TOKEN=$(get_dwd_token "$SOURCE_EMAIL" \
  "https://www.googleapis.com/auth/gmail.settings.sharing")

# Call Gmail API directly with curl — do NOT call gws here.
# gws wraps the Gmail API but adds a serviceusage.serviceUsageConsumer check
# against your GCP project that fails until IAM propagates (~5 min).
# Calling curl directly bypasses that check.
curl -sS -X POST \
  -H "Authorization: Bearer $DWD_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"delegateEmail\": \"$DEST_EMAIL\"}" \
  "https://gmail.googleapis.com/gmail/v1/users/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SOURCE_EMAIL'))")/settings/delegates" \
  | jq .
```

Expected response: `{"delegateEmail": "...", "verificationStatus": "accepted"}`

DEST_EMAIL can now access SOURCE_EMAIL's mailbox via Gmail → avatar menu →
account switcher. Allow up to 1 minute for it to appear.

### Step 4 — Set Vacation Responder (OOO)

```bash
DWD_BASIC=$(get_dwd_token "$SOURCE_EMAIL" \
  "https://www.googleapis.com/auth/gmail.settings.basic")

curl -sS -X PUT \
  -H "Authorization: Bearer $DWD_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "enableAutoReply": true,
    "responseSubject": "I am no longer with the organization",
    "responseBodyPlainText": "Thank you for your message. This person is no longer with the organization. Please contact info@[the organization's domain].",
    "restrictToContacts": false,
    "restrictToDomain": false
  }' \
  "https://gmail.googleapis.com/gmail/v1/users/$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SOURCE_EMAIL'))")/settings/vacation" \
  | jq '{enableAutoReply, responseSubject}'
```

### Step 5 — Suspend Account

**Irreversible-ish**: prevents login immediately. Data is preserved. Reversible
via unsuspend. Wait 10 seconds before running:

```bash
curl -sS -X PATCH \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"suspended": true}' \
  "https://admin.googleapis.com/admin/directory/v1/users/$SOURCE_EMAIL" \
  | jq '{primaryEmail, suspended}'
```

### Step 6 — Notify the operator

Post to #lumina-bot:
```
Offboarding complete for $SOURCE_EMAIL → $DEST_EMAIL
• Drive + Calendar transfer: $TRANSFER_ID ($TRANSFER_STATUS)
• Gmail delegation: accepted ($DEST_EMAIL can now read $SOURCE_EMAIL's inbox)
• OOO: enabled
• Account: suspended
Next: verify transfer complete, retain account 30–90 days, then delete manually.
```

---

## If Migration Tool Asks for Liv's 2FA

The Google Workspace Data Migration tool may trigger a **login challenge** even
when 2SV is already off. This is a suspicious-login detection, not 2FA.

**Two-step fix (Admin Console only — no API available for this):**

1. Admin Console → Users → [User] → **Security** tab → scroll to **"Login challenge"**
   → click → **"Turn off identity questions for 10 minutes"**

2. Also reset the user's password from the same Security tab so you have
   credentials for the migration tool without needing the user's old password.

Start the migration tool immediately after — the 10-minute window starts when
you click it.

Check 2SV status before assuming it's the blocker:
- "2-step verification" shows **Off** = 2SV is not the issue
- The login challenge is the more common blocker for admin-initiated migrations

---

## /onboard-user

Create a new Google Workspace user and configure their account.

**Usage**: `/onboard-user FULL_NAME EMAIL TEMP_PASSWORD`

### Step 1 — Create User

```bash
curl -sS -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"primaryEmail\": \"$EMAIL\",
    \"name\": {
      \"givenName\": \"$(echo $FULL_NAME | cut -d' ' -f1)\",
      \"familyName\": \"$(echo $FULL_NAME | cut -d' ' -f2-)\"
    },
    \"password\": \"$TEMP_PASSWORD\",
    \"changePasswordAtNextLogin\": true,
    \"orgUnitPath\": \"/\"
  }" \
  "https://admin.googleapis.com/admin/directory/v1/users" \
  | jq '{id, primaryEmail, creationTime}'
```

### Step 2 — Add to Groups (if applicable)

```bash
# List existing groups to find the right group email
curl -sS -H "Authorization: Bearer $ADMIN_TOKEN" \
  "https://admin.googleapis.com/admin/directory/v1/groups?domain=[the organization's domain]" \
  | jq '.groups[] | {email, name}'

# Add user to a group
curl -sS -X POST \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"role\": \"MEMBER\"}" \
  "https://admin.googleapis.com/admin/directory/v1/groups/GROUP_EMAIL/members" \
  | jq .
```

### Step 3 — Send Welcome Instructions

Send the new user their login credentials via iMessage or Slack. Include:
- Their email address
- Temporary password (they'll be forced to change on first login)
- Link to set up 2SV: https://myaccount.google.com/security

### Step 4 — Log to Attio

Add a note to their Attio contact record (if one exists) noting account
creation date and role.

---

## One-Time Setup (run once per environment)

### 1. Install gws
```bash
npm install -g @googleworkspace/cli
```

### 2. Install Python venv for DWD helper
```bash
python3.12 -m venv ~/gws-offboard-venv
~/gws-offboard-venv/bin/pip install google-auth
# Add alias so 'python3' in scripts uses the venv:
# OR: update scripts/gws_dwd_token.py shebang to ~/gws-offboard-venv/bin/python3
```

Note: `pip3 install google-auth` will fail with PEP 668 on macOS — use a venv.

### 3. Create service account (gcloud — no Console UI needed)
```bash
gcloud iam service-accounts create workspace-offboarding \
  --project=acme-project-id \
  --display-name="Workspace Offboarding"

# Grant caller permission to sign JWTs as the SA (bypasses key creation)
gcloud iam service-accounts add-iam-policy-binding \
  workspace-offboarding@acme-project-id.iam.gserviceaccount.com \
  --member="user:austin@[the organization's domain]" \
  --role="roles/iam.serviceAccountTokenCreator"

# Grant SA permission to use project APIs via gws
gcloud projects add-iam-policy-binding acme-project-id \
  --member="serviceAccount:workspace-offboarding@acme-project-id.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageConsumer"

# Enable IAM Credentials API (needed for signJwt)
gcloud services enable iamcredentials.googleapis.com --project=acme-project-id

# Get the SA's numeric client_id for the DWD grant:
gcloud iam service-accounts describe \
  workspace-offboarding@acme-project-id.iam.gserviceaccount.com \
  --format="value(uniqueId)"
```

No JSON key file needed or created. The org policy `iam.disableServiceAccountKeyCreation`
is enforced at the org level and cannot be overridden at project level.

### 4. Grant Domain-Wide Delegation in Admin Console
(One browser step — no API available for this)

1. Go to: `admin.google.com` → Security → Access and data control → API Controls
   → **Domain-wide Delegation** → **Add new**
   (direct URL: `admin.google.com/ac/owl/domainwidedelegation`)
2. Client ID: `<uniqueId from step 3>`
3. Scopes:
   ```
   https://www.googleapis.com/auth/gmail.settings.sharing,https://www.googleapis.com/auth/gmail.settings.basic
   ```
4. Click **Authorize**

Note: the "Add new" button is small and top-left of the table. If the URL
`/ac/owl/domainwidedelegation` returns 404, navigate from the main Admin
Console home rather than directly via URL.

### 5. Set env var
```bash
export GWS_SA_EMAIL="workspace-offboarding@acme-project-id.iam.gserviceaccount.com"
# Add to ~/.openclaw/.env for persistence
```

---

## Rollback

**Unsuspend account:**
```bash
curl -sS -X PATCH \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"suspended": false}' \
  "https://admin.googleapis.com/admin/directory/v1/users/SUSPENDED_EMAIL" \
  | jq '{primaryEmail, suspended}'
```

**Remove Gmail delegate:**
```bash
DWD_TOKEN=$(get_dwd_token "SOURCE_EMAIL" \
  "https://www.googleapis.com/auth/gmail.settings.sharing")
curl -sS -X DELETE \
  -H "Authorization: Bearer $DWD_TOKEN" \
  "https://gmail.googleapis.com/gmail/v1/users/SOURCE_EMAIL/settings/delegates/DELEGATE_EMAIL"
```

**Data transfer** — no undo. Reassign Drive file ownership manually via Google
Drive UI if needed.

---

## Known Gotchas (learned in production)

- `gws` does NOT expose Admin SDK Directory or Data Transfer — use curl directly
- `gws auth export --unmasked` returns `{client_id, client_secret, refresh_token}`,
  NOT a live `access_token` — must call `/oauth2/token` to exchange it
- The gws `GOOGLE_WORKSPACE_CLI_TOKEN` env var bypass works for Gmail calls
  but fails with a `serviceusage.serviceUsageConsumer` 403 until IAM propagates
  (~5 min) — call the Gmail API directly via curl instead
- DWD grant URLs like `/ac/users/detail/uid/{id}/security` often return 404 —
  navigate from the Admin Console home → Users → search
- `admin.datatransfer` scope must be explicitly included in `gws auth login` or
  the Transfer API calls will return 401
- `iam.disableServiceAccountKeyCreation` is enforced org-wide — use `signJwt`
  via IAM Credentials API instead of a JSON key file
- Login challenge (not 2SV) is the most common blocker for the Data Migration
  tool — check 2SV status first; if it's already Off, use the Login Challenge
  bypass (10-minute window) in the Security tab
