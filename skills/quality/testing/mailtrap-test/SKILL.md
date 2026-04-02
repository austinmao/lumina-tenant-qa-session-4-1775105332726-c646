---
name: mailtrap-test
description: "Send rendered email to Mailtrap sandbox and validate quality + ClawWrap readiness"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /mailtrap-test
metadata:
  openclaw:
    emoji: "🧪"
    requires:
      env:
        - MAILTRAP_API_KEY
        - MAILTRAP_INBOX_ID
      bins:
        - python3
---

# Mailtrap Test

Send a rendered email template to the Mailtrap sandbox inbox, then run a two-layer validation suite: email quality checks and ClawWrap outbound-gate readiness checks. All 10 checks must pass before the email is considered production-ready.

## Prerequisites

- `MAILTRAP_API_KEY` — Mailtrap API token with sandbox send permissions
- `MAILTRAP_INBOX_ID` — numeric inbox ID from the Mailtrap sandbox project
- `python3` with the `mailtrap` SDK installed (`pip install mailtrap`)
- Read access to `clawwrap/config/targets.yaml` for ClawWrap readiness checks

## Inputs

| Parameter | Required | Description |
|---|---|---|
| `template` | yes | Template identifier (e.g. `MailchimpL2V2`, `ResendWelcome`) |
| `subject` | yes | Expected subject line |
| `html` | yes | Rendered HTML string or path to `.html` file |
| `from_address` | yes | Sender address to validate against targets.yaml |
| `context_key` | yes | ClawWrap routing context key (e.g. `acme-event`) |
| `audience` | yes | ClawWrap routing audience (e.g. `waitlist`, `alumni`) |
| `provider` | yes | Email provider: `resend` or `mailchimp` |

## Workflow

### Step 1 — Send to Mailtrap Sandbox

Use the Mailtrap Python SDK to deliver the rendered email into the sandbox inbox. This validates that the email is structurally valid and deliverable.

```python
import mailtrap as mt

API_KEY = os.environ["MAILTRAP_API_KEY"]
INBOX_ID = os.environ["MAILTRAP_INBOX_ID"]

client = mt.MailtrapClient(token=API_KEY, sandbox=True, inbox_id=INBOX_ID)
mail = mt.Mail(
    sender=mt.Address(email="test@sandbox.example.com"),
    to=[mt.Address(email="qa@sandbox.example.com")],
    subject=subject,
    html=html,
)
client.send(mail)
```

### Step 2 — Run Layer 1: Email Quality Checks

After the email arrives in the sandbox, run six quality checks against the delivered message.

#### Check 1: `delivery`

Confirm the email arrived in the Mailtrap sandbox inbox. Query the inbox API and verify the message exists with a matching subject line. Fail if the message is not found within 15 seconds.

#### Check 2: `subject_match`

Compare the delivered message's subject line against the expected `subject` input. Must be an exact string match. Fail if subjects differ.

#### Check 3: `body_non_empty`

Verify the HTML body of the delivered message is not empty. The body must contain at least one non-whitespace character after stripping HTML tags. Fail if body is blank or contains only whitespace.

#### Check 4: `links_valid`

Extract all `href` attribute values from anchor tags in the HTML body. For each URL:
- Skip mailto: links and anchor-only links (starting with `#`)
- Skip merge-tag URLs containing `{{`, `*|`, or `%7B%7B`
- Send an HTTP HEAD request with a 10-second timeout
- Require a 2xx response status

Fail if any URL returns a non-2xx status or times out. Report all failing URLs in the failure detail.

#### Check 5: `images_have_alt`

Parse all `<img>` tags in the HTML body. Every image must have a non-empty `alt` attribute. Fail if any `<img>` tag is missing `alt` or has an empty `alt=""` value. Report the `src` of each offending image in the failure detail.

#### Check 6: `html_size_under_100kb`

Measure the byte length of the rendered HTML string (UTF-8 encoded). Must be under 102,400 bytes (100 KB). Fail if the HTML exceeds this limit. Report the actual size in the failure detail.

### Step 3 — Run Layer 2: ClawWrap Readiness Checks

These checks validate that the email is compatible with the ClawWrap outbound gate before it reaches production dispatch.

#### Check 7: `from_address_registered`

Load `clawwrap/config/targets.yaml` and verify that the `from_address` input matches a registered target entry. The from address must appear as an email target in the file. Fail if the address is not found in any target entry.

#### Check 8: `unsubscribe_present`

Scan the HTML body for the presence of an unsubscribe merge tag. The expected tag depends on the provider:
- **Resend**: `{{{RESEND_UNSUBSCRIBE_URL}}}`
- **Mailchimp**: `*|UNSUB|*`

At least one of the provider-appropriate tags must be present in the HTML. Fail if the tag for the declared provider is missing.

#### Check 9: `target_resolvable`

Using the `context_key` and `audience` inputs, attempt to resolve a target in `clawwrap/config/targets.yaml` following the ClawWrap shared route mode (`context_key + audience + channel=email`). Fail if no matching target entry exists.

#### Check 10: `provider_match`

Validate that the declared `provider` input matches the email's design patterns:
- **Resend**: HTML contains `{{{RESEND_UNSUBSCRIBE_URL}}}` or Resend-specific merge tags
- **Mailchimp**: HTML contains `*|` merge tag patterns (e.g. `*|UNSUB|*`, `*|FNAME|*`, `*|MC:SUBJECT|*`)

Fail if the declared provider does not match the merge tag patterns found in the HTML. This catches misconfigured templates that claim one provider but use another's merge tags.

## Output Format

The skill produces a YAML verdict report:

```yaml
template: MailchimpL2V2
verdict: pass
checks:
  delivery: pass
  subject_match: pass
  body_non_empty: pass
  links_valid: pass
  images_have_alt: pass
  html_size_under_100kb: pass
  from_address_registered: pass
  unsubscribe_present: pass
  target_resolvable: pass
  provider_match: pass
failures: []
```

When checks fail, the verdict is `fail` and the `failures` list contains detail entries:

```yaml
template: ResendWelcome
verdict: fail
checks:
  delivery: pass
  subject_match: pass
  body_non_empty: pass
  links_valid: fail
  images_have_alt: fail
  html_size_under_100kb: pass
  from_address_registered: pass
  unsubscribe_present: fail
  target_resolvable: pass
  provider_match: pass
failures:
  - check: links_valid
    detail: "https://example.com/broken-link returned 404"
  - check: images_have_alt
    detail: "Missing alt on <img src='hero.png'>"
  - check: unsubscribe_present
    detail: "Expected {{{RESEND_UNSUBSCRIBE_URL}}} for provider=resend but not found in HTML"
```

## Pipeline Behavior

On any failure, halt Lobster pipeline before brand-gate with message: `Email not ClawWrap-ready: {check_name} failed`

The mailtrap-test skill runs as a pipeline gate between template rendering and brand-gate review. If any of the 10 checks fail, the Lobster pipeline must not proceed to the brand-gate stage. The halt message identifies the first failing check so the operator can fix and re-run.

Integration point in a Lobster workflow:

```yaml
- step: render-template
- step: mailtrap-test        # <-- this skill; halts here on failure
- step: brand-gate
- step: outbound-dispatch
```

## Failure Triage

| Check | Common cause | Fix |
|---|---|---|
| `delivery` | Invalid Mailtrap credentials or inbox ID | Verify `MAILTRAP_API_KEY` and `MAILTRAP_INBOX_ID` env vars |
| `subject_match` | Template renders a different subject than expected | Check template variables and rendering logic |
| `body_non_empty` | Template rendering returned empty string | Debug the template render step; check for missing data |
| `links_valid` | Broken URL or staging-only link in template | Replace with production URL or add to skip list |
| `images_have_alt` | Image tag missing alt attribute | Add descriptive alt text to every `<img>` tag |
| `html_size_under_100kb` | Inlined images or excessive CSS | Extract images to CDN; minify CSS; remove unused styles |
| `from_address_registered` | Sender not in targets.yaml | Add the from address to `clawwrap/config/targets.yaml` |
| `unsubscribe_present` | Missing unsubscribe merge tag | Add `{{{RESEND_UNSUBSCRIBE_URL}}}` or `*\|UNSUB\|*` to template footer |
| `target_resolvable` | context_key + audience combo not registered | Add routing entry to `clawwrap/config/targets.yaml` |
| `provider_match` | Template uses wrong provider's merge tags | Align merge tags with the declared provider |
