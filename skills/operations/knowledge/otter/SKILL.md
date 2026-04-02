---
name: otter
description: >
  Access Otter.ai transcriptions — list speeches, fetch full transcripts,
  download exports, search within recordings, and manage speakers and folders.
  Use this skill when processing meeting recordings, extracting action items
  from Zoom calls, or routing transcript content to Attio, Slack, or the
  sales pipeline. Falls back to this skill when Fireflies is unavailable.
version: 1.0.0
metadata:
  openclaw:
    emoji: "microphone"
    requires:
      env:
        - OTTER_USERNAME
        - OTTER_PASSWORD
      bins: []
---

# Otter.ai Integration

List, fetch, download, search, and manage Otter.ai transcriptions via the
`otterai` Python library. Primary use cases in this workspace:

1. Pull Zoom call transcripts for the sales pipeline (Fireflies fallback)
2. Extract action items and summaries for Attio CRM notes
3. Search within recordings for specific decisions or follow-ups

## Required environment variables

| Variable | Description |
|---|---|
| `OTTER_USERNAME` | Otter.ai account email |
| `OTTER_PASSWORD` | Otter.ai account password |

Both are set in `.env`.

## Usage

All operations use `OtterClient` from `src/otter/client.py`.

```python
from src.otter.client import OtterClient

client = OtterClient()  # reads OTTER_USERNAME / OTTER_PASSWORD from env
```

## Operations

### List recent speeches

```python
speeches = client.list_speeches(page_size=20)
for s in speeches:
    print(s["id"], s.get("title"))
```

Filter by source:

```python
# Zoom recordings only
speeches = client.list_speeches(source="zoom", page_size=20)
```

Filter by folder:

```python
speeches = client.list_speeches(folder=5, page_size=20)
```

### Get a speech by ID

```python
speech = client.get_speech("SPEECH_ID")
# transcript data lives at speech["data"]["speech"]
```

### Search within a transcript

```python
results = client.query_speech("action items", "SPEECH_ID")
results = client.query_speech("decision", "SPEECH_ID", size=100)
```

### Download transcript text

```python
content = client.download_speech("SPEECH_ID", fileformat="txt")
text = content.decode("utf-8")
```

Supported `fileformat` values: `txt`, `pdf`, `mp3`, `docx`, `srt`.
Use `txt,pdf,mp3,docx,srt` to download all formats as a zip archive.

### Upload an audio file for transcription

```python
result = client.upload_speech("/path/to/recording.mp4")
new_speech_id = result.get("speech_id")
```

### Manage speakers

```python
# List all speaker profiles
speakers = client.get_speakers()

# Create a new speaker
speaker = client.create_speaker("Austin Mao")
```

### List folders

```python
folders = client.get_folders()
```

## Common patterns for this workspace

### Post-Zoom sales call — transcript → Attio note

```python
from src.otter.client import OtterClient

client = OtterClient()
speeches = client.list_speeches(source="zoom", page_size=5)

# Take the most recent recording
latest = speeches[0]
content = client.download_speech(latest["id"], fileformat="txt")
transcript_text = content.decode("utf-8")

# Pass transcript_text to the sales-director agent / deal-management skill
# for summary extraction and Attio CRM note creation
```

### Fireflies fallback — pull latest transcript when Fireflies is unavailable

The `fireflies-sync` sales skill should fall back to this skill when
Fireflies sync fails. Use the same transcript → Attio note pipeline above.

### Search all recent recordings for a contact name

```python
speeches = client.list_speeches(page_size=45)
for speech in speeches:
    results = client.query_speech("Jane Doe", speech["id"])
    if results.get("data"):
        print(f"Found in: {speech.get('title')} ({speech['id']})")
```

## Error handling

```python
from src.otter.client import OtterClient
from otterai import OtterAIException

try:
    client = OtterClient()
    speeches = client.list_speeches()
except OtterAIException as e:
    print(f"Otter API error: {e}")
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Preflight check

```python
import os
for var in ["OTTER_USERNAME", "OTTER_PASSWORD"]:
    status = "OK" if os.environ.get(var) else "MISSING"
    print(f"{status}: {var}")
```

## Error recovery

| Error | Fix |
|---|---|
| `ValueError: OTTER_USERNAME is required` | Add `OTTER_USERNAME` to `.env` |
| `ValueError: OTTER_PASSWORD is required` | Add `OTTER_PASSWORD` to `.env` |
| `OtterAIException` on login | Verify credentials are correct at otter.ai |
| `OtterAIException` on get_speech | Speech ID may be invalid or deleted |
