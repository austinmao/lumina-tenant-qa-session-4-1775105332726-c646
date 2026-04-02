---
name: security-audit
description: "Audit page security: CSP headers, XSS vectors, HTTPS enforcement, and external script review"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /security-audit
metadata:
  openclaw:
    emoji: "🔒"
    requires:
      bins: ["curl"]
      env: []
      os: ["darwin"]
---

# Security Audit Skill

Run a structured security audit against a target URL or page. Produces a weighted score across five categories and routes all issues to Nova (frontend engineer).

## Usage

```
/security-audit <url>
```

Example:

```
/security-audit https://[the organization's domain]
```

---

## HTTP Security Headers (30% weight)

Fetch response headers using:

```bash
curl -sI <url>
```

Check for the following headers and flag any that are absent or misconfigured:

| Header | Required Value | Fail Condition |
|---|---|---|
| `Content-Security-Policy` | Present and restrictive | Missing or contains `unsafe-inline` without hash/nonce |
| `X-Content-Type-Options` | `nosniff` | Missing or any other value |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Missing or set to `ALLOWALL` |
| `Strict-Transport-Security` | `max-age` ≥ 31536000 | Missing or `max-age` below threshold |
| `Referrer-Policy` | `strict-origin-when-cross-origin` recommended | Missing |
| `Permissions-Policy` | Restricts `camera`, `microphone`, `geolocation` | Missing or grants broad access |

Score this section 0–100. Deduct points for each missing or misconfigured header.

---

## HTTPS Enforcement (20% weight)

Verify that the page and all its resources are served over HTTPS:

- Confirm the base URL resolves to `https://`
- Check for mixed content: any resource (`<img>`, `<script>`, `<link>`, `<iframe>`) loaded over `http://` on an HTTPS page is a blocking issue
- Verify HTTP → HTTPS redirect is in place:

```bash
curl -sI http://<domain> | grep -i location
```

- Check HSTS preload eligibility: header must include `includeSubDomains` and `preload`

**Blocking issues**: mixed content, missing HTTPS redirect.

Score this section 0–100.

---

## XSS Prevention (20% weight)

Inspect page source for XSS vectors:

- **Inline event handlers**: attributes like `onclick`, `onload`, `onerror`, `onmouseover` — flag all occurrences
- **Dangerous DOM write patterns**: direct DOM manipulation using legacy write methods that inject raw HTML strings — flag all occurrences
- **Dynamic code execution patterns**: use of the `Function` constructor with string arguments, or similar runtime code generation — flag all occurrences
- **Unescaped user input**: user-controlled data (query params, form data) appearing in rendered HTML without escaping — flag all occurrences
- **CSP inline script check**: verify `script-src` does not allow `'unsafe-inline'` unless paired with a hash or nonce

Note: this audit checks for the _presence_ of dangerous patterns. Remediation is routed to Nova.

**Blocking issues**: confirmed dynamic code execution on user input, unescaped user data in rendered HTML.

Score this section 0–100.

---

## External Script Audit (15% weight)

List all external scripts on the page:

```bash
curl -s <url> | grep -oE '<script[^>]+src="[^"]+"' | grep -oE 'src="[^"]+"'
```

For each external script:

1. Record the source domain
2. Check whether an `integrity` attribute (SRI hash) is present
3. Flag scripts from unknown or untrusted domains
4. Check loaded library versions against known CVE databases (e.g., Retire.js findings, Snyk advisories) if the version is identifiable from the URL or response

Report format per script:

```
- <url> | domain: <domain> | SRI: yes/no | trusted: yes/no | known-vuln: yes/no
```

Score this section 0–100. Deduct for missing SRI on third-party scripts and for any known-vulnerable library versions.

---

## Form Security (15% weight)

Inspect all `<form>` elements on the page:

- Method: sensitive forms must use `POST`, not `GET`
- CSRF token: a hidden `<input>` with a token field name (`csrf_token`, `_token`, `authenticity_token`, or equivalent) must be present on state-changing forms
- Form `action` URLs must use `https://` — flag any `http://` or external-domain actions
- Sensitive fields (`type="password"`, credit card inputs) must have `autocomplete="off"` or `autocomplete="new-password"`
- No form `action` pointing to a domain other than the page's own origin, unless explicitly documented

Score this section 0–100.

---

## Scoring

Calculate the overall security score as a weighted sum:

| Section | Weight |
|---|---|
| HTTP Security Headers | 30% |
| HTTPS Enforcement | 20% |
| XSS Prevention | 20% |
| External Script Audit | 15% |
| Form Security | 15% |

```
overall = (headers * 0.30) + (https * 0.20) + (xss * 0.20) + (scripts * 0.15) + (forms * 0.15)
```

**Score bands:**

| Score | Rating |
|---|---|
| 90–100 | Pass |
| 75–89 | Pass with warnings |
| 50–74 | Fail — remediation required |
| 0–49 | Critical — blocking issues present |

---

## Output Format

Produce a structured audit report:

```
Security Audit: <url>
Date: <YYYY-MM-DD>
Overall Score: <score>/100 (<rating>)

[HTTP Security Headers] <score>/100
  PASS/FAIL — <header>: <finding>
  ...

[HTTPS Enforcement] <score>/100
  PASS/FAIL — <finding>
  ...

[XSS Prevention] <score>/100
  PASS/FAIL — <finding>
  ...

[External Script Audit] <score>/100
  - <script-url> | domain: <domain> | SRI: yes/no | trusted: yes/no | known-vuln: yes/no
  ...

[Form Security] <score>/100
  PASS/FAIL — <finding>
  ...

Blocking Issues:
  - <list or "None">

Recommended Actions:
  - <prioritized list>
```

---

## Issue Routing

All security issues identified by this audit are routed to **Nova** (frontend engineer).

- Blocking issues: flag immediately in the audit report and notify Nova before any other work continues
- Non-blocking issues: include in the recommended actions list for Nova's next sprint
- Do not attempt to fix security issues directly — produce the report and hand off to Nova
