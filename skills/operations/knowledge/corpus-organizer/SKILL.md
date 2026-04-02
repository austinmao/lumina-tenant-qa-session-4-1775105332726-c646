---
name: corpus-organizer
description: "Classify and file a cleaned transcript into the correct corpus subfolder"
version: "1.0.0"
permissions:
  filesystem: read/write
  network: false
triggers:
  - command: /corpus-organizer
metadata:
  openclaw:
    emoji: "🗂️"
    requires:
      bins: ["python3"]
      os: ["darwin"]
---

# Corpus Organizer Skill

## Overview

Reads a formatted transcript from `corpus/staging/` (the `-formatted` output of
`corpus-formatter`), classifies it into the correct corpus subfolder, generates a
correctly-named filename, and moves the file to its final location.

## Classification Logic

Use the frontmatter `content_type` field first. If `content_type` is missing or
ambiguous, fall back to the contextual signals listed below.

| content_type value | Target subfolder | Notes |
|---|---|---|
| `tedx` | `corpus/speeches/tedx/` | TEDx talk or formal conference keynote |
| `talk` | `corpus/speeches/talks/` | Standalone public talk, workshop, panel |
| `podcast` | `corpus/speeches/podcasts/` | Podcast episode, interview, media appearance |
| `education` | `corpus/retreats/education/` | Retreat orientation recording; the operator teaching solo |
| `prep-call` | `corpus/retreats/prep-calls/<retreat-slug>/` | Group prep call with retreat participants |
| `coaching-intake` | `corpus/coaching/intake/` | 1-on-1 enrollment or discovery call |

**Fallback classification (when content_type is absent or `talk` is ambiguous):**

Scan the frontmatter `context` field and transcript body for these signals:

| Signal | Classification |
|---|---|
| "TEDx", "TED talk" | `tedx` |
| "podcast", "interview", "episode", "host", "guest" | `podcast` |
| "prep call", "preparation call", "group call", "participants joining" | `prep-call` |
| "orientation", "integration", "education session", "solo teaching" | `education` |
| "intake", "enrollment", "discovery call", "1 on 1", "one on one" | `coaching-intake` |
| Conference, summit, symposium, workshop (the operator is primary speaker) | `talk` |

If classification remains ambiguous after both passes, default to `corpus/speeches/talks/`
and include `classification: ambiguous` in the return result (for the operator's review).

## Retreat Slug Derivation (for prep-calls)

When classifying as `prep-call`, derive the retreat slug:

1. Check frontmatter `context` field for retreat name (e.g., "Awaken Retreat January 2026")
2. Check frontmatter `tags` for retreat identifiers
3. Check transcript body for explicit retreat name mentions by the operator

Slug format: `<retreat-name>-<month>-<year>` in kebab-case.
Examples:
- "Awaken January 2026" → `awaken-jan-2026`
- "Heal Retreat February 2025" → `heal-feb-2025`

If slug cannot be determined: use `unknown-retreat` and flag for the operator's review.

Check if the target `corpus/retreats/prep-calls/<slug>/` directory exists:
- If yes: use it
- If no: create it with `mkdir -p <path>` before moving the file

## Filename Convention

Generate the final filename as: `YYYY-MM-DD--<slug>.md`

Where:
- `YYYY-MM-DD` comes from frontmatter `date` field; use `unknown` if date is absent
- `<slug>` is derived from the frontmatter `title` field:
  ```python
  import re
  slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
  # Truncate to 60 characters max
  slug = slug[:60].rstrip("-")
  ```

Examples:
- date: 2025-10-15, title: "TEDx Boulder — Feel Alive Together"
  → `2025-10-15--tedx-boulder-feel-alive-together.md`
- date: unknown, title: "Awaken Prep Call Group 3"
  → `unknown--awaken-prep-call-group-3.md`

## Steps

### Step 1 — Read the formatted file

Read the `-formatted` staging file. Parse frontmatter. Extract: `content_type`, `date`,
`title`, `context`, `tags`.

### Step 2 — Classify

Apply the classification logic above. Derive target subfolder.

If `content_type` is `prep-call`: also derive the retreat slug and confirm/create the
target subdirectory.

### Step 3 — Generate target filename

Apply the filename convention above. Check that a file with the generated name does not
already exist in the target directory:
- If it already exists: append `-v2` to the slug and check again. Repeat up to `-v5`.
- If all variants exist: stop and notify the operator — "Duplicate detected: <filename>. Manual
  review required."

### Step 4 — Move the file

```python
import shutil
shutil.move(str(formatted_path), str(target_path))
```

Do not delete the original (non-formatted) staging file — Curator's pipeline handles
staging cleanup.

### Step 5 — Update triage log

Open the triage log for this file at `corpus/logs/triage/YYYY-MM-DD-<slug>.json` and
update the `corpus_path` field with the final absolute path.

### Step 6 — Return result

Return to the calling agent:
- `corpus_path`: absolute path to the moved file
- `content_type`: classification applied
- `target_subfolder`: directory the file was placed in
- `filename`: final filename used
- `classification_confidence`: `frontmatter` | `contextual` | `ambiguous`
- `retreat_slug`: populated only for `prep-call` classification; null otherwise

## Output

File moved from `corpus/staging/<name>-formatted.md` to the correct corpus subfolder
with the canonical filename.

## Error Handling

| Condition | Response |
|---|---|
| File not found | "corpus-organizer: formatted file not found at <path>. Stopping." |
| All duplicate variants exist (v2-v5) | Stop; notify the operator; leave file in staging |
| Target directory creation fails | "corpus-organizer: cannot create directory <path> — check permissions." |
| File move fails | "corpus-organizer: move failed from <src> to <dst>. File left in staging." |
| python3 not available | "corpus-organizer: python3 required but not found. Install Python 3." |
| Retreat slug cannot be determined | Use `unknown-retreat`; flag in return result |
