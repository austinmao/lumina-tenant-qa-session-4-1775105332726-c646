---
name: gusto
description: |
  Read payroll, employee, contractor, and company data from Gusto via the official
  Gusto MCP server. Use this skill when the operator asks about payroll runs, employee
  compensation, contractor payments, time tracking, pay schedules, or any other
  Gusto HR/payroll data.
version: "1.0.0"
permissions:
  filesystem: none
  network: true
triggers:
  - command: /gusto
metadata:
  openclaw:
    emoji: "💼"
    homepage: https://docs.gusto.com/app-integrations/docs/mcp
    requires:
      env:
        - GUSTO_CLIENT_ID
        - GUSTO_CLIENT_SECRET
        - GUSTO_ACCESS_TOKEN
        - GUSTO_REFRESH_TOKEN
      bins:
        - curl
---

# Gusto

Read-only access to Gusto payroll and HR data via the official Gusto MCP remote
server at `https://mcp.api.gusto.com/`.

All 37 tools exposed by this skill are **read-only**. There are no write, create,
update, or delete operations available. No Gusto data can be modified through this
skill.

---

## Operations Gate — Approval Requirements

**Safe without the operator's approval (all operations are read-only):**

Every tool listed below is a read-only query. No data is written to Gusto through
this integration.

**Always requires the operator's explicit approval before sharing externally:**

- Any payroll figures, compensation data, or contractor payment amounts
- Employee PII: addresses, hire dates, employment history, termination records
- Contractor payment details and payment group breakdowns
- Time sheet data and leave balances

**Handling rules for sensitive data:**

- Never write raw employee or contractor records to any file outside
  `memory/drafts/` or `memory/logs/`
- Never post payroll figures or employee PII to Slack or any external channel
- Reference individuals by name only — do not paste full record payloads into
  chat responses
- If the operator asks for an export of more than 20 records, confirm scope before
  fetching

---

## Critical Isolation Requirement

Gusto recommends running this MCP server in an **isolated session** — do not
mix it with other MCP servers in the same Claude Code session. This is a Gusto
security requirement, not a preference. Reason: payroll and HR data is highly
sensitive; mixing tool contexts increases prompt injection surface.

**When to start a dedicated Gusto session:**
- Before calling any Gusto tool, confirm no other MCP servers with broad
  permissions are active in the session
- Prefer a fresh Claude Code session when querying employee or payroll data

---

## Authentication — OAuth 2.0 (authorization_code grant)

Gusto requires a browser-based OAuth 2.0 authorization code flow. No static
API key is available for the data categories this skill needs (employee,
payroll, contractor). System Access Tokens are explicitly excluded — they
cover only organization-level operations, not HR or payroll data.

**One-time setup (run once; ~3 minutes):**

1. Go to [dev.gusto.com](https://dev.gusto.com/) and open (or create) your
   application under "Applications".
2. Under "Redirect URIs", register exactly:
   ```
   http://localhost:9004/callback
   ```
   (No wildcards, no trailing slash, no URL fragments — Gusto enforces an
   exact string match.)
3. Copy your Client ID and Client Secret from the app settings page.
4. Add them to `.env`:
   ```
   GUSTO_CLIENT_ID=<your_client_id>
   GUSTO_CLIENT_SECRET=<your_client_secret>
   ```
5. Run the OAuth helper script:
   ```bash
   python3 scripts/gusto-oauth.py
   ```
   The script opens a browser, you log in with a Primary Admin or Full Access
   Admin account, and the callback is captured automatically. The script
   writes `GUSTO_ACCESS_TOKEN` and `GUSTO_REFRESH_TOKEN` to `.env` and
   prints the expiry time.
6. Verify the token works:
   ```bash
   source .env && ./scripts/verify-gusto-mcp.sh
   ```

**Token refresh (access token expires in 2 hours):**

The refresh token is single-use — each refresh returns a new pair.

Manual refresh:
```bash
python3 scripts/gusto-token-refresh.py
```

Automated cron refresh (every 110 minutes):
```
*/110 * * * * cd /Users/luminamao/Documents/Github/openclaw && python3 scripts/gusto-token-refresh.py >> logs/gusto-refresh.log 2>&1
```

If a refresh fails with HTTP 401, the refresh token was likely already
consumed or has expired. Re-run `gusto-oauth.py` to re-authorize.

**Endpoints:**

```
Authorization (main API): https://api.gusto.com/oauth/authorize
Token (main API):         https://api.gusto.com/oauth/token
Token info:               https://api.gusto.com/v1/token_info
MCP server (Claude):      https://mcp.api.gusto.com/anthropic
MCP server (Demo):        https://mcp.api.gusto-demo.com
```

The main API access token works for both the REST API and the MCP server —
both accept `Authorization: Bearer <token>` with the same token.

---

## Rate Limits

**200 requests per 60-second rolling window.**

- Exceeding this returns HTTP 429 with a `Retry-After` header
- Do not issue more than 20 API calls in a single task without pausing to
  summarize results and confirm continuation with the operator
- If a 429 is received: read the `Retry-After` value, wait that many seconds,
  then retry once; if it recurs, stop and notify the operator

---

## Quick Start — Add to MCP Client

Add the following to your MCP client configuration (e.g., `~/.claude.json`
under `mcpServers`):

```json
{
  "mcpServers": {
    "gusto": {
      "type": "http",
      "url": "https://mcp.api.gusto.com/anthropic",
      "headers": {
        "Authorization": "Bearer ${GUSTO_ACCESS_TOKEN}"
      }
    }
  }
}
```

To use the demo environment (no real Gusto account required):

```json
{
  "mcpServers": {
    "gusto-demo": {
      "type": "http",
      "url": "https://mcp.api.gusto-demo.com",
      "headers": {
        "Authorization": "Bearer ${GUSTO_ACCESS_TOKEN}"
      }
    }
  }
}
```

---

## Tool Reference — 37 Tools by Category

### Company and Organization (5 tools)

| Tool | What it returns |
|---|---|
| `list_gusto_companies` | All companies the authenticated user can access |
| `list_company_locations` | Physical locations registered under the company |
| `list_company_departments` | All departments in the company |
| `get_department` | Single department by ID (name, members) |
| `get_location` | Single location by ID (address, timezone) |

**Common queries:**

- "What departments does the organization have in Gusto?" → `list_company_departments`
- "What is the address of our main Gusto location?" → `list_company_locations` then `get_location`

---

### Employees (14 tools)

| Tool | What it returns |
|---|---|
| `list_company_employees` | All active and terminated employees |
| `get_gusto_employee` | Full employee profile by ID |
| `list_employee_jobs` | All jobs (roles) held by an employee |
| `get_job` | Single job record (title, start date, pay rate) |
| `list_job_compensations` | All compensation records tied to a job |
| `get_compensation` | Single compensation record (rate, type, FLSA) |
| `list_employee_employment_history` | Historical employment status changes |
| `list_employee_terminations` | Termination records for an employee |
| `get_employee_rehire` | Rehire record for a terminated employee |
| `list_employee_custom_fields` | Custom field values set on an employee |
| `list_employee_home_addresses` | Home address history |
| `get_employee_home_address` | Single home address record |
| `list_employee_work_addresses` | Work address history |
| `get_employee_work_address` | Single work address record |

**Common queries:**

- "List all employees" → `list_company_employees`
- "What is [employee]'s current compensation?" → `get_gusto_employee` to get ID, then `list_employee_jobs`, then `list_job_compensations`
- "When did [employee] start?" → `get_gusto_employee` or `list_employee_employment_history`

---

### Contractors (6 tools)

| Tool | What it returns |
|---|---|
| `list_company_contractors` | All contractors associated with the company |
| `get_contractor` | Single contractor profile by ID |
| `list_company_contractor_payments` | All contractor payments across all contractors |
| `get_contractor_payment` | Single contractor payment record |
| `list_company_contractor_payment_groups` | Payment groups (batch payment runs) |
| `get_contractor_payment_group` | Single payment group with itemized payments |

**Common queries:**

- "Who are our active contractors?" → `list_company_contractors`
- "How much did we pay contractors last month?" → `list_company_contractor_payments` filtered by date

---

### Payroll (7 tools)

| Tool | What it returns |
|---|---|
| `list_company_payrolls` | All payroll runs (processed and unprocessed) |
| `get_payroll` | Single payroll run with full detail (totals, deductions) |
| `list_company_pay_schedules` | All pay schedules (weekly, biweekly, etc.) |
| `get_pay_schedule` | Single pay schedule details |
| `list_company_pay_periods` | Pay periods for a given schedule |
| `list_company_pay_schedule_assignments` | Which employees are on which schedule |
| `list_company_earning_types` | Custom earning types configured for the company |

**Common queries:**

- "When is the next payroll run?" → `list_company_pay_periods` for upcoming periods
- "What was the total payroll for last month?" → `list_company_payrolls` then `get_payroll`
- "What pay schedule are employees on?" → `list_company_pay_schedules`

---

### Time Tracking (2 tools)

| Tool | What it returns |
|---|---|
| `list_company_time_sheets` | All time sheets for the company |
| `get_time_sheet` | Single time sheet (hours, employee, period) |

**Common queries:**

- "Show me recent time sheets" → `list_company_time_sheets`

---

### Utility (2 tools)

| Tool | What it returns |
|---|---|
| `get_token_info` | OAuth scopes and token metadata for the current session |
| `list_company_custom_fields_schema` | Custom field definitions for the company |

Run `get_token_info` first to verify the token is valid and to confirm which
data categories were granted during the OAuth flow.

---

## Usage Examples — the organization Context

**"How many employees does the organization have in Gusto?"**

```
1. list_gusto_companies → get company_id
2. list_company_employees (company_id) → count active records
```

**"What is our payroll schedule?"**

```
1. list_gusto_companies → get company_id
2. list_company_pay_schedules (company_id) → show all schedules
3. list_company_pay_schedule_assignments (company_id) → show who is on each
```

**"Pull the most recent payroll summary"**

```
1. list_gusto_companies → get company_id
2. list_company_payrolls (company_id, processed=true) → get most recent
3. get_payroll (payroll_id) → full breakdown
```

**"Who are our current contractors and what do we pay them?"**

```
1. list_gusto_companies → get company_id
2. list_company_contractors (company_id)
3. list_company_contractor_payments (company_id) → filter to last 90 days
```

**"Verify my Gusto token is working"**

```
1. get_token_info → confirm scopes and expiry
```

---

## Error Handling

| Status | Meaning | Response |
|---|---|---|
| 401 | Token expired or invalid | Re-run OAuth flow; update GUSTO_ACCESS_TOKEN in .env |
| 403 | Data category not granted during OAuth | Re-authorize and select the missing category |
| 429 | Rate limited | Read Retry-After header; wait; retry once; notify the operator if persists |
| 5xx | Gusto server error | Wait 30s; retry once; if persists, check status.gusto.com |

---

## Security Notes

- Never hardcode `GUSTO_ACCESS_TOKEN` in any file — always read from `process.env`
  or `.env`
- The token grants read access to real HR and payroll data — treat it with the
  same sensitivity as banking credentials
- Opt out of model training in your Claude/LLM client settings before connecting
  to the Gusto MCP server (Gusto requirement)
- Do not share the token across team members — each user should complete their
  own OAuth flow
- Rotate the token if the laptop is lost, stolen, or access is transferred

---

## Resources

- [Gusto MCP Documentation](https://docs.gusto.com/app-integrations/docs/mcp)
- [Gusto API Reference](https://docs.gusto.com/app-integrations/reference)
- [Gusto Status Page](https://status.gusto.com)
