---
name: gdpr-compliance-check
description: "Audit a website for GDPR compliance gaps: consent, cookies, data collection forms"
version: "1.0.0"
permissions:
  filesystem: read
  network: false
triggers:
  - command: /gdpr-compliance-check
metadata:
  openclaw:
    emoji: "✅"
---

## Overview

Audits a Next.js website project for GDPR compliance gaps by inspecting source files: cookie consent implementation, privacy policy presence, form opt-in checkboxes, analytics configuration, and data retention notices. Outputs a compliance report with pass/fail/warning per item.

## Steps

### 1. Gather Scope

Ask the user for the site root path if not running from the project root. Also ask which third-party services are in use (GA4, Stripe, Calendly, Attio, Resend, etc.) — this determines which processors to check for.

### 2. Run Checks

Perform all checks below by reading source files. Do not run the site live.

#### Check Group A — Cookie Consent

| ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| A1 | Cookie consent banner exists | `components/CookieConsent.tsx` or similar file found, or `@cookie-consent` library installed in `package.json` | No banner component found |
| A2 | Analytics loads conditionally | GA4 script load gated on consent flag (check for consent check before `GoogleAnalytics` or `gtag` call) | GA4 loads unconditionally |
| A3 | Consent stored in localStorage | `localStorage.setItem` with a consent key present in banner component | Consent not persisted |

#### Check Group B — Privacy Policy

| ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| B1 | Privacy policy page exists | `app/privacy/page.tsx` or similar route found | No privacy page found |
| B2 | Privacy policy linked in footer | Footer component contains `href` pointing to `/privacy` | No privacy link in footer |
| B3 | Policy covers third-party processors | `docs/legal/privacy-policy.md` lists all configured third-party services | Missing processors (compare against user's declared services list) |

#### Check Group C — Forms

| ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| C1 | Explicit consent checkbox on marketing forms | Form components that collect email contain a `type="checkbox"` for marketing consent | Email collection without consent checkbox |
| C2 | Contact forms state data retention | Form or nearby text references data retention period | No retention notice near form |
| C3 | No pre-ticked consent boxes | Consent checkboxes default to `defaultChecked={false}` or no `defaultChecked` prop | `defaultChecked={true}` on any consent checkbox |

#### Check Group D — Analytics

| ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| D1 | GA4 ID is env var not hardcoded | `NEXT_PUBLIC_GA4_ID` used, not a literal `G-XXXXXXXXXX` string in source | Hardcoded GA4 ID found |
| D2 | IP anonymisation note | `memory/site-analytics.yaml` or GA4 config comments note that GA4 anonymises IP by default in EU | Not documented (warning, not fail) |

#### Check Group E — Legal Pages

| ID | Check | Pass condition | Fail condition |
|---|---|---|---|
| E1 | Terms of service page exists | `app/terms/page.tsx` or similar route | Not found |
| E2 | Cookie policy page exists | `app/cookies/page.tsx` or cookie section in privacy policy | Not found (warning) |
| E3 | Legal pages linked in footer | Footer contains links to `/privacy` and `/terms` | Missing links |

### 3. Score and Report

Output a compliance report:

```
GDPR Compliance Audit — <site name>
Date: <today>

PASS  A1  Cookie consent banner exists
FAIL  A2  Analytics loads before consent — GA4 must be gated on consent
PASS  A3  Consent stored in localStorage
PASS  B1  Privacy policy page exists
WARN  B2  Privacy policy not found in footer — add link to footer component
...

Summary: 10 checks — 7 PASS, 2 FAIL, 1 WARN

CRITICAL ACTIONS (fix before launch):
1. [A2] Gate GA4 load on cookie consent — use /cookie-consent skill
2. [C1] Add explicit marketing consent checkbox to newsletter signup form

RECOMMENDED ACTIONS:
1. [B2] Add privacy policy link to footer
2. [D2] Document IP anonymisation behaviour in memory/site-analytics.yaml
```

### 4. Suggest Remediation Skills

For each FAIL item, suggest the relevant skill to fix it:
- A2 (GA4 not gated) → `cookie-consent` skill
- B1 (no privacy policy) → `privacy-policy-gen` skill
- E1 (no ToS) → `terms-of-service-gen` skill
- B3 (missing processors) → re-run `privacy-policy-gen` skill with updated processor list

## Output

- Compliance report printed to console with pass/fail/warning per item
- Summary: N checks, N pass, N fail, N warn
- Prioritised action list

## Error Handling

- Source files not found → mark check as UNKNOWN rather than PASS or FAIL; note that manual review is needed
- Ambiguous results (e.g., consent logic in an unusual location) → mark as WARN with explanation
- No form files found → mark all Form checks as UNKNOWN; ask user to point to form components
