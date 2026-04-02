---
name: campaign-calendar
description: "Detect scheduling conflicts across all active campaign pipelines"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /campaign-calendar
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins:
        - python3
---

# Campaign Calendar / Conflict Detection

Reads ALL active pipeline state files, builds a unified send calendar, and
detects scheduling conflicts before the operator approves a campaign send.

## When to Use

- Before approving any campaign send (automatic via Lobster `calendar-check` stage)
- When planning a new campaign to check for date conflicts
- During campaign strategy sessions to visualize the send calendar

## Conflict Types

### Error Severity (blocks pipeline)

| Conflict | Detection | Rule |
|---|---|---|
| **Within-3h-of-event** | Broadcast scheduled < 3h before `event_date` | Beacon cadence rule: distraction zone |
| **Same-audience-same-day** | Two sends to same ClawWrap `context_key.audience` on same date | Prevents inbox fatigue |
| **Double-send-24h** | Same contact receives 2+ emails within 24h window | Combining scheduled broadcasts across providers |

### Warning Severity (operator review)

| Conflict | Detection | Rule |
|---|---|---|
| **Marketing+registrant overlap** | MailChimp broadcast + Resend registrant email on same day | Registrants appear in both audiences |
| **Adjacent-day sends** | Sends on consecutive days to overlapping audiences | May cause fatigue but not a hard violation |
| **Weekend send** | Broadcast scheduled for Saturday or Sunday | Brand audience prefers Tue/Thu/Mon sends |

## Algorithm

### Step 1 — Collect all scheduled sends

```python
import os, yaml, glob
from datetime import datetime

pipelines = glob.glob("memory/pipelines/*/state.yaml")
scheduled_sends = []

for state_path in pipelines:
    with open(state_path) as f:
        state = yaml.safe_load(f)
    if not state or state.get("status") == "completed":
        continue

    pipeline_id = state.get("pipeline_id", "unknown")

    # Check for scheduled MailChimp campaign
    if state.get("mailchimp_scheduled"):
        scheduled_sends.append({
            "pipeline_id": pipeline_id,
            "provider": "mailchimp",
            "audience": "acme-webinar.full-list",
            "scheduled_at": state.get("mailchimp_schedule_time"),
        })

    # Check for scheduled Resend broadcast
    if state.get("resend_scheduled"):
        scheduled_sends.append({
            "pipeline_id": pipeline_id,
            "provider": "resend",
            "audience": "acme-webinar.registrants",
            "scheduled_at": state.get("resend_schedule_time"),
        })

    # Check event_date for within-3h validation
    event_date = state.get("event_date")
    if event_date:
        scheduled_sends.append({
            "pipeline_id": pipeline_id,
            "type": "event",
            "event_date": event_date,
        })
```

### Step 2 — Detect conflicts

For each pair of scheduled sends, check:
1. Same audience + same calendar date → ERROR
2. Any send within 3h of any event_date → ERROR
3. Same contact within 24h → ERROR (requires audience overlap analysis)
4. Marketing + registrant on same day → WARNING
5. Send on Saturday/Sunday → WARNING

### Step 3 — Output calendar + conflicts

```yaml
calendar:
  2026-03-24:
    - pipeline: have-a-good-trip-v2
      provider: mailchimp
      audience: full-list
      time: "17:00 UTC"
  2026-03-26:
    - pipeline: have-a-good-trip-v2
      provider: mailchimp
      audience: full-list
      time: "16:00 UTC"
  2026-03-30:
    - pipeline: have-a-good-trip-v2
      provider: mailchimp
      audience: full-list
      time: "17:00 UTC"
    - pipeline: have-a-good-trip-v2
      provider: resend
      audience: registrants
      time: "16:00 UTC"

conflicts:
  - severity: warning
    type: marketing-registrant-overlap
    date: 2026-03-30
    detail: "MailChimp broadcast + Resend registrant email on same day"
    pipelines: [have-a-good-trip-v2]

verdict: warning  # pass | warning | error
```

## Lobster Integration

New stage in `campaign-webinar.lobster` BEFORE `approval`:

```yaml
- id: calendar-check
  command: scripts/lobster-calendar-check.sh ${pipeline_id}
```

If verdict is `error`, the pipeline halts before approval with specific
conflict details. If `warning`, conflicts are displayed in the approval
prompt for operator review. If `pass`, pipeline continues silently.

## Output Location

Report written to: `memory/logs/qa/calendar-check-{pipeline_id}.yaml`

## Related Skills

- `campaign-strategy` — cadence rules (Tue/Thu/Mon send days, 2h gap minimum)
- `mailtrap-test` — validates individual emails; calendar-check validates scheduling
- `behavioral-automation` — behavioral triggers respect calendar constraints
