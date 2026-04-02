---
name: zoom-recording
description: "Fetch zoom recording / get webinar recording / activate replay page"
version: "1.1.0"
permissions:
  filesystem: write
  network: true
triggers:
  - command: /zoom-recording
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["curl", "jq", "python3"]
      env: ["ZOOM_ACCOUNT_ID", "ZOOM_CLIENT_ID", "ZOOM_CLIENT_SECRET"]
      os: ["darwin"]
---

# Zoom Recording Skill

Fetches the cloud recording URL for a Zoom meeting via Server-to-Server OAuth, writes it to `web/data/replay-config.json`, and notifies the operator via Slack.

## Trigger Phrases

- "fetch zoom recording"
- "fetch zoom recording for meeting {meetingId}"
- "get webinar recording"
- "activate replay page"

## Parameters

| Parameter | Source | Default |
|---|---|---|
| `MEETING_ID` | Lobster step argument `${meeting_id}` | None — required |
| `EXPIRES_AT` | Lobster step argument `${expires_at}` | 48 hours from fetch time |
| Config path | Relative to workspace root | `web/data/replay-config.json` |

## Algorithm

### Step 1 — Get OAuth token

```bash
ZOOM_TOKEN=$(curl -s -X POST \
  "https://zoom.us/oauth/token?grant_type=account_credentials&account_id=${ZOOM_ACCOUNT_ID}" \
  -H "Authorization: Basic $(echo -n "${ZOOM_CLIENT_ID}:${ZOOM_CLIENT_SECRET}" | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  | jq -r '.access_token')
```

### Step 2 — Fetch recordings

```bash
RECORDING_RESPONSE=$(curl -s \
  "https://api.zoom.us/v2/meetings/${MEETING_ID}/recordings" \
  -H "Authorization: Bearer ${ZOOM_TOKEN}")
```

### Step 3 — Check availability

If HTTP 404 or `recording_files` is empty or null:

> Reply: "Recording not yet available for meeting {MEETING_ID}. Zoom typically takes 5–30 minutes to process after the session ends. Try again in 15 minutes."

Stop here.

### Step 4 — Extract share URL

```bash
SHARE_URL=$(echo "$RECORDING_RESPONSE" | jq -r '.share_url // empty')
```

If `share_url` is empty or null, try per-file play URL:

```bash
SHARE_URL=$(echo "$RECORDING_RESPONSE" | jq -r '.recording_files[] | select(.file_type == "MP4" and .status == "completed") | .play_url' | head -1)
```

If still empty:

> Reply: "Recording files found but no shareable URL available yet. The MP4 may still be processing. Try again in 15 minutes."

Stop here.

### Step 4b — Extract transcript and summary

```bash
# Extract download_access_token (used for authenticated downloads, discarded after)
DOWNLOAD_TOKEN=$(echo "$RECORDING_RESPONSE" | jq -r '.download_access_token // empty')

# Extract transcript URL (file_type == "TRANSCRIPT", .vtt format)
TRANSCRIPT_URL=$(echo "$RECORDING_RESPONSE" | jq -r '.recording_files[] | select(.file_type == "TRANSCRIPT" and .status == "completed") | .download_url' | head -1)

# Extract summary URL (file_type == "SUMMARY", .json format)
SUMMARY_URL=$(echo "$RECORDING_RESPONSE" | jq -r '.recording_files[] | select(.file_type == "SUMMARY" and .status == "completed") | .download_url' | head -1)
```

If transcript or summary URLs are empty, these are optional — continue without them.

### Step 4c — Download transcript and summary to local files

**Security**: The `download_access_token` is a bearer token. It MUST NOT be written to `replay-config.json` or any file on disk. Use it for downloads, then discard.

```bash
# Download transcript VTT if available
if [ -n "$TRANSCRIPT_URL" ] && [ -n "$DOWNLOAD_TOKEN" ]; then
  curl -s -o web/data/replay-transcript.vtt \
    "${TRANSCRIPT_URL}?access_token=${DOWNLOAD_TOKEN}"
fi

# Download and parse summary JSON if available
if [ -n "$SUMMARY_URL" ] && [ -n "$DOWNLOAD_TOKEN" ]; then
  SUMMARY_JSON=$(curl -s "${SUMMARY_URL}?access_token=${DOWNLOAD_TOKEN}")
fi

# Token is no longer needed — do not store it
```

### Step 5 — Write replay-config.json

Write to `web/data/replay-config.json` (relative to workspace root):

```python
import json, datetime, os

# Compute expiry: use EXPIRES_AT arg if provided, else 48h from now
expires_at = os.environ.get("EXPIRES_AT") or (
    datetime.datetime.utcnow() + datetime.timedelta(hours=48)
).strftime("%Y-%m-%dT%H:%M:%SZ")

config = {
    "url": share_url,
    "fetchedAt": datetime.datetime.utcnow().isoformat() + "Z",
    "expiresAt": expires_at,
    "meetingId": meeting_id,
    "status": "active"
}

# Add transcript path if downloaded
transcript_path = "web/data/replay-transcript.vtt"
if os.path.exists(transcript_path):
    config["transcript_vtt_path"] = transcript_path

# Add summary if fetched
if summary_json:
    try:
        config["summary"] = json.loads(summary_json)
    except json.JSONDecodeError:
        pass  # Summary not available or malformed — skip

config_path = "web/data/replay-config.json"
with open(config_path, "w") as f:
    json.dump(config, f, indent=2)
```

### Step 6 — Notify Slack

Post to `#lumina-bot`:

```
✅ Replay activated: {SHARE_URL}
Meeting: {MEETING_ID} | Fetched: {NOW} | Expires: Sat Mar 7 12pm MT
Page live at: https://[configured replay page URL]
```

Use the `slack` skill for this post.

### Step 7 — Confirm to user

> "Replay page is now live. The recording has been embedded at [configured replay page URL] and will be available until Saturday, March 7 at 12:00 pm MT. the operator has been notified in #lumina-bot."

## Error Handling

| Condition | Response |
|---|---|
| OAuth token fetch fails | "Zoom authentication failed — check ZOOM_CLIENT_ID and ZOOM_CLIENT_SECRET in .env" |
| 404 on recordings endpoint | "Recording not yet available. Try again in 15 minutes." |
| `recording_files` empty | "Recording not yet available (processing). Try again in 15 minutes." |
| No MP4 with status=completed | "Files found but MP4 not yet processed. Try again in 15 minutes." |
| File write fails | "Could not write replay-config.json — check file path and permissions" |

## Constitution Check

- **Principle I (Human-in-the-Loop)**: Zoom read + local file write is not an external send. Autonomous OK.
- **Principle V (Transparency)**: Skill posts to Slack #lumina-bot on every successful run.
- **Principle VI (Silence Over Noise)**: Only runs when triggered (manually or via heartbeat on Thu Mar 5).

## Notes

- Zoom `share_url` is at the response root (not per-file) — use this first
- Token expiry: 1 hour — skill fetches a fresh token on every invocation
- `expiresAt` defaults to 48h from fetch time (configurable via `EXPIRES_AT` param)
- Replay config file path: `web/data/replay-config.json` (relative to workspace root)
- Transcript (`.vtt`) and summary (`.json`) are optional — Zoom AI features must be enabled on the account
- `download_access_token` is NEVER written to disk — fetched, used for downloads, discarded
