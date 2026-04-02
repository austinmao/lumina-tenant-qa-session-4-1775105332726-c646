---
name: zoom
description: Manage Zoom meetings — list, create, get, update, delete. Uses Server-to-Server OAuth with credentials from .env.
version: "1.0.0"
permissions:
  filesystem: none
  network: true
metadata:
  openclaw:
    requires:
      env:
        - ZOOM_ACCOUNT_ID
        - ZOOM_CLIENT_ID
        - ZOOM_CLIENT_SECRET
      bins:
        - node
---

# Zoom Meeting Manager

Create, list, inspect, update, and delete Zoom meetings via the Zoom v2 REST API.

## Required environment variables

These must be set in `.env` (already configured for this project):

| Variable | Description |
|---|---|
| `ZOOM_ACCOUNT_ID` | Server-to-Server OAuth account ID |
| `ZOOM_CLIENT_ID` | OAuth client ID |
| `ZOOM_CLIENT_SECRET` | OAuth client secret |
| `ZOOM_USER_ID` | (optional) Zoom user — defaults to `me` |

## Commands

### List upcoming meetings

```bash
node ./skills/zoom/scripts/zoom-cli.js list
```

### Create a meeting

```bash
node ./skills/zoom/scripts/zoom-cli.js create "<topic>" "<start_time_ISO>" <duration_minutes>
```

- `start_time_ISO`: ISO 8601 format, e.g. `2026-03-15T14:00:00Z`
- `duration_minutes`: integer 1–1440

Example:
```bash
node ./skills/zoom/scripts/zoom-cli.js create "Team Sync" "2026-03-15T14:00:00Z" 60
```

### Get meeting details

```bash
node ./skills/zoom/scripts/zoom-cli.js info <meeting_id>
```

### Update a meeting

```bash
node ./skills/zoom/scripts/zoom-cli.js update <meeting_id> <start_time_ISO> <duration_minutes> [new_topic]
```

### Delete a meeting

```bash
node ./skills/zoom/scripts/zoom-cli.js delete <meeting_id>
```

## Notes

- All credentials are loaded from environment variables only. No `config.json` files.
- `auto_recording` is intentionally off by default. Enable explicitly if needed.
- The script fetches a fresh OAuth token per invocation; tokens are never written to disk.
- `ZOOM_SECRET_TOKEN` is for Zoom webhook verification (not used by this CLI).

## Preflight check

```bash
node -e "
  ['ZOOM_ACCOUNT_ID','ZOOM_CLIENT_ID','ZOOM_CLIENT_SECRET'].forEach(k => {
    if (!process.env[k]) console.error('Missing:', k);
  });
  console.log('env ok');
"
```

## Error recovery

| Error | Fix |
|---|---|
| `Zoom OAuth failed (401)` | Wrong CLIENT_ID or CLIENT_SECRET |
| `Zoom OAuth failed (400)` | Wrong ACCOUNT_ID or missing Server-to-Server OAuth app scopes |
| `GET /users/me/meetings failed (404)` | ZOOM_USER_ID doesn't exist or app lacks user:read scope |
| `Invalid meeting ID` | Meeting ID must be all digits |
| `Invalid ISO date-time` | Use ISO 8601, e.g. `2026-03-15T14:00:00Z` |
