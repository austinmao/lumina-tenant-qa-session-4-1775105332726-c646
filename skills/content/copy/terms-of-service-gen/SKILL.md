---
name: terms-of-service-gen
description: "Generate terms of service for a website — requires operator review before publish"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /terms-of-service-gen
metadata:
  openclaw:
    emoji: "📄"
---

## Overview

Generates a terms of service (ToS) document as a Markdown file covering service description, user obligations, payment terms, refund policy, IP ownership, and limitation of liability. Always marked DRAFT — never publish without operator and legal review. Prompts for jurisdiction to set governing law correctly.

## IMPORTANT: Legal Disclaimer

**ALWAYS state this to the user before generating and include it in the output:**

> This is an AI-generated DRAFT for reference purposes only. It is not legal advice. Have a qualified legal professional review this document before publishing it on your site.

## Steps

### 1. Gather Details

Ask the user for:
- Company/organisation legal name
- Registered address
- Primary contact email
- **Jurisdiction** (state/country for governing law, e.g., "California, USA", "England and Wales", "Ontario, Canada") — this is mandatory; do not assume
- Service description: what the site offers (e.g., "in-person wellness retreats and online programs")
- Whether payments are accepted on the site (yes/no)
- Refund policy: full refund window, partial refund terms, no-refund items
- Whether user-generated content is accepted (yes/no)
- Age restriction: minimum age for users (default: 18)

### 2. Generate Terms of Service

Write `docs/legal/terms-of-service.md`:

---

**[DRAFT — NOT FOR PUBLICATION WITHOUT LEGAL REVIEW]**

# Terms of Service

**Effective date:** [INSERT DATE]
**Last updated:** [INSERT DATE]

## 1. Acceptance of Terms

By accessing or using [Site Name] (the "Site"), you agree to be bound by these Terms of Service. If you do not agree, do not use the Site.

## 2. Description of Service

[Company legal name] ("we", "us", "our") provides [service description]. We reserve the right to modify or discontinue any part of the Service at any time with reasonable notice.

## 3. Eligibility

You must be at least [minimum age, default 18] years of age to use this Site. By using the Site, you represent that you meet this requirement.

## 4. User Obligations

You agree to:
- Provide accurate, current, and complete information
- Not misrepresent your identity or affiliation
- Not use the Site for any unlawful purpose
- Not attempt to gain unauthorised access to any part of the Site
- Not transmit harmful, offensive, or disruptive content

## 5. Payment Terms

[Include only if payments accepted:]

All prices are listed in [currency, default USD] and are inclusive/exclusive of applicable taxes as stated at checkout. Payment is processed by Stripe. By submitting payment, you authorise us to charge the stated amount.

Subscriptions (if applicable) renew automatically at the stated interval until cancelled. You may cancel via your account dashboard or by contacting us at [email].

## 6. Refund Policy

**[Operator must customise this section with their actual refund policy before publishing.]**

- Full refund if cancelled more than [X] days before the event/programme start date
- [X]% refund if cancelled between [X] and [Y] days before start date
- No refund for cancellations within [X] days of start date, except where required by applicable law
- Digital downloads and online courses are non-refundable once accessed

## 7. Intellectual Property

All content on the Site — including text, images, logos, designs, and materials — is owned by or licensed to [Company name] and protected by applicable copyright and intellectual property laws.

You may not reproduce, distribute, or create derivative works from our content without express written permission.

## 8. User-Generated Content

[Include only if UGC is accepted:]

By submitting content to the Site, you grant us a non-exclusive, royalty-free, worldwide licence to use, display, and distribute that content in connection with our services. You retain ownership of your content.

## 9. Disclaimer of Warranties

THE SITE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED. WE DO NOT WARRANT THAT THE SITE WILL BE UNINTERRUPTED, ERROR-FREE, OR FREE OF HARMFUL COMPONENTS.

## 10. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, [COMPANY NAME] SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES ARISING FROM YOUR USE OF THE SITE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

OUR TOTAL LIABILITY TO YOU FOR ANY CLAIM SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO US IN THE 12 MONTHS PRECEDING THE CLAIM.

## 11. Governing Law

These Terms are governed by the laws of [JURISDICTION — e.g., "the State of California, USA"]. Any disputes shall be resolved in the courts of [JURISDICTION].

## 12. Changes to Terms

We may update these Terms at any time. Continued use of the Site after changes constitutes acceptance of the updated Terms.

## 13. Contact

For questions about these Terms: [email address]

---

**[END OF DRAFT — REQUIRES LEGAL REVIEW BEFORE PUBLICATION]**

---

### 3. Create `app/terms/page.tsx` Placeholder

Write a minimal placeholder page at `app/terms/page.tsx`. Do not render the draft content live.

## Output

- `docs/legal/terms-of-service.md` — DRAFT ToS (requires legal review)
- `app/terms/page.tsx` — placeholder page

## Error Handling

- User does not provide jurisdiction → ask again; do not default to any jurisdiction, as this is legally material
- Refund policy details not provided → insert `[REQUIRED: define refund terms with your legal advisor]` placeholder
- User asks to publish immediately → remind them this is a DRAFT requiring legal review; refuse to create a deployment step
