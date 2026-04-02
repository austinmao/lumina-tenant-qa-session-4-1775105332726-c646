---
name: form-testing
description: "Test form submissions, validation edge cases, and multi-step flows"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
metadata:
  openclaw:
    source: "new (045-hierarchy-v2)"
---

Test web forms comprehensively. Cover validation, edge cases, submission handling, and multi-step flows.

## Test Checklist
- Required field validation (empty submit)
- Email format validation
- Phone number formats (international)
- Max length enforcement
- XSS prevention in text inputs
- File upload size/type restrictions
- Multi-step form state persistence
- Submit button disabled during processing
- Error message clarity and positioning
- Success/failure redirect behavior
