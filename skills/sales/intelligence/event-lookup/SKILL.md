---
name: event-lookup
description: "Look up upcoming the organization retreat and event details, dates, locations, and availability"
version: "1.0.0"
permissions:
  filesystem: none
  network: true
metadata:
  openclaw:
    emoji: "📅"
    requires:
      env: ["AIRTABLE_API_KEY", "AIRTABLE_BASE_ID"]
      bins: ["curl", "jq"]
---

# event-lookup

Retrieve upcoming event details from the organization events database (Airtable/DB). Use this when a contact asks about specific dates, locations, or event availability.

## Usage

When a contact asks about retreat dates, locations, or seat availability, call this skill to fetch current event data.

```bash
# Fetch upcoming events
curl -s "https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/Events?filterByFormula=IS_AFTER({Start Date}, TODAY())&sort[0][field]=Start+Date&sort[0][direction]=asc&maxRecords=5" \
  -H "Authorization: Bearer ${AIRTABLE_API_KEY}" | jq '.records[] | {name: .fields.Name, date: .fields["Start Date"], location: .fields.Location, seats: .fields["Seats Available"]}'
```

## What to Return to Contact

Always convert raw dates to human-readable format:
- "March 14-21, 2026 in Asheville, NC (3 seats remaining)"
- "Next retreat: April 4-8, 2026 in Costa Rica (waitlist open)"

## Rules
- If event data is unavailable, say: "Let me check on the latest dates — someone from our team will confirm the specifics."
- Never promise seats — always say "as of our last update" or "subject to availability"
- If the contact expresses strong interest in a specific date, note this in memory via memory-update skill
