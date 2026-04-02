---
name: sms-copy
description: "Write SMS messages within 160-char limits with TCPA compliance and opt-out language"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Write SMS marketing and transactional messages. Every character counts.

## Constraints
- 160 characters max (single segment)
- Must include opt-out: "Reply STOP to unsubscribe"
- TCPA compliance: only send to opted-in contacts
- No ALL CAPS (spam filter trigger)
- No URL shorteners from unknown domains

## Structure (160 chars)
[Brand] [Message] [CTA] [Opt-out]
Example: "the organization: Your webinar starts in 2 hours. Join at [the organization's domain]/live Reply STOP to opt out"
