---
name: deliverability
description: "Configure SPF, DKIM, DMARC, and monitor email deliverability health"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Ensure emails reach inboxes. Configure DNS authentication records, monitor reputation, and troubleshoot delivery issues.

## When to Use
- Setting up a new sending domain
- Diagnosing delivery failures
- Implementing authentication (SPF, DKIM, DMARC)

## Key Records
- SPF: v=spf1 include:_spf.resend.com ~all
- DKIM: resend._domainkey CNAME
- DMARC: v=DMARC1; p=quarantine; rua=mailto:dmarc@domain
