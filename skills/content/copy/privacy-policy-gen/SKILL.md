---
name: privacy-policy-gen
description: "Generate a GDPR-compliant privacy policy for a website — requires operator review before publish"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /privacy-policy-gen
metadata:
  openclaw:
    emoji: "🔒"
---

## Overview

Generates a GDPR-compliant privacy policy document as a Markdown file. Covers all required sections including legal basis, user rights, and third-party processors. Output is always marked DRAFT — operator must review and approve before publishing. This skill does not provide legal advice.

## IMPORTANT: Legal Disclaimer

**ALWAYS include this notice at the top of the generated document and state it verbally to the user:**

> This is an AI-generated DRAFT for reference purposes only. It does not constitute legal advice. Have a qualified legal professional review and approve this document before publishing it on your site.

## Steps

### 1. Gather Site Details

Ask the user for:
- Company/organisation legal name
- Registered address
- Primary contact email for privacy enquiries
- Country of establishment (determines governing law)
- List of third-party services in use (prompt with common options: GA4, Stripe, Attio, Resend, Calendly, Sanity, Vercel)
- Whether the site collects data from EU residents (determines GDPR applicability)
- Data retention period for contact/lead data (e.g., 2 years after last interaction)

### 2. Generate Privacy Policy

Write `docs/legal/privacy-policy.md`:

---

**[DRAFT — NOT FOR PUBLICATION WITHOUT LEGAL REVIEW]**

# Privacy Policy

**Effective date:** [INSERT DATE]
**Last updated:** [INSERT DATE]

## 1. Who We Are

[Company legal name] ("we", "us", "our") is registered at [address]. For privacy enquiries, contact [email].

## 2. What Data We Collect

We collect the following categories of personal data:

- **Contact information**: name, email address, phone number (collected via contact forms and booking widgets)
- **Payment information**: processed by Stripe; we do not store card details directly
- **Usage data**: pages visited, time on site, referral source (collected via Google Analytics 4)
- **Communications**: email correspondence you send to us

## 3. Legal Basis for Processing (GDPR Article 6)

| Purpose | Legal basis |
|---|---|
| Processing enquiries and bookings | Article 6(1)(b) — performance of a contract |
| Sending marketing emails | Article 6(1)(a) — consent (you may withdraw at any time) |
| Analytics and site improvement | Article 6(1)(f) — legitimate interests |
| Legal compliance | Article 6(1)(c) — legal obligation |

## 4. How We Use Your Data

We use your personal data to: respond to enquiries, process bookings, send confirmation emails, improve our website, and (with your consent) send marketing communications.

We do not sell your personal data to third parties.

## 5. Data Retention

We retain personal data for [retention period, e.g., 2 years] after your last interaction with us, unless a longer retention period is required by law.

## 6. Third-Party Processors

We share your data with the following processors who act on our behalf:

| Processor | Purpose | Location | Privacy Policy |
|---|---|---|---|
| Google Analytics 4 | Website analytics | USA | [google.com/privacy](https://google.com/privacy) |
| Stripe | Payment processing | USA | [stripe.com/privacy](https://stripe.com/privacy) |
| Attio | CRM | USA | [attio.com/privacy](https://attio.com/privacy) |
| Resend | Transactional email | USA | [resend.com/privacy](https://resend.com/privacy) |
| Calendly | Appointment scheduling | USA | [calendly.com/privacy](https://calendly.com/privacy) |
| Sanity | Content management | USA/EU | [sanity.io/privacy](https://sanity.io/privacy) |
| Vercel | Website hosting | USA | [vercel.com/legal/privacy-policy](https://vercel.com/legal/privacy-policy) |

[Remove any processors not applicable to this site.]

## 7. Your Rights

Under GDPR, if you are an EU/UK resident, you have the right to:
- **Access**: request a copy of data we hold about you
- **Rectification**: correct inaccurate data
- **Erasure**: request deletion of your data ("right to be forgotten")
- **Portability**: receive your data in a machine-readable format
- **Objection**: object to processing based on legitimate interests
- **Withdrawal of consent**: withdraw marketing consent at any time

To exercise these rights, contact [privacy email]. We will respond within 30 days.

## 8. Cookies

We use cookies for analytics (GA4) and session management. See our [Cookie Policy](/cookies) for details. You can manage cookie preferences via our consent banner.

## 9. Data Security

We use industry-standard security measures including HTTPS, encrypted storage, and access controls to protect your personal data.

## 10. Changes to This Policy

We may update this policy. Significant changes will be communicated via email or a prominent notice on our site.

## 11. Contact

For privacy enquiries: [email address]
For complaints: you may lodge a complaint with your national data protection authority.

---

**[END OF DRAFT — REQUIRES LEGAL REVIEW BEFORE PUBLICATION]**

---

### 3. Create `app/privacy/page.tsx` Placeholder

Write a minimal Next.js page at `app/privacy/page.tsx` that renders the policy content. Leave the content as `[DRAFT — import from docs/legal/privacy-policy.md after review]`. Do not render the draft content directly on the live site.

## Output

- `docs/legal/privacy-policy.md` — DRAFT policy document (requires legal review)
- `app/privacy/page.tsx` — placeholder page

## Error Handling

- User does not provide required details → insert `[REQUIRED: insert <field>]` placeholders; never fabricate legal details
- User asks to publish immediately → remind them this is a DRAFT requiring legal review; do not create a deployment step
