---
name: email-campaign-html
description: "Generate a multi-email campaign sequence / build HTML for an email drip sequence with shared design tokens"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /email-campaign
metadata:
  openclaw:
    emoji: "📨"
    requires:
      bins: ["node"]
      os: ["darwin"]
---

# Email Campaign HTML Skill

Generates complete multi-email campaign sequences: 3-7 emails with shared design tokens, progressive narrative arc, consistent header/footer, cross-client HTML, and a campaign manifest. Each email is a standalone React Email template linked by a shared campaign identity. Ported from Naksha-studio's /email-campaign command.

---

## Prerequisites

1. Read `memory/site-context.yaml` for active site. If missing: prompt `/site <name>`.
2. Read `skills/engineering/email/email-design-system/SKILL.md` for token references.
3. Read `templates/email/render.ts` for the existing template registry.

---

## Steps

### 1. Define campaign parameters

| Input | Required | Default |
|---|---|---|
| Campaign name | Yes | N/A |
| Campaign type | Yes | N/A (welcome, launch, nurture, re-engagement, event, post-purchase) |
| Email count | No | Determined by campaign type |
| Send cadence | No | Determined by campaign type |
| Shared variables | No | `firstName`, `brandName` |

Default email counts by type:
- **Welcome**: 5 emails over 14 days (day 0, 1, 3, 7, 14)
- **Launch**: 7 emails over 10 days (day -3, -1, 0, 0+6h, 1, 3, 7)
- **Nurture**: 6 emails over 30 days (day 0, 5, 10, 17, 24, 30)
- **Re-engagement**: 3 emails over 7 days (day 0, 3, 7)
- **Event**: 4 emails (confirmation, reminder -3d, reminder -1d, follow-up +1d)
- **Post-purchase**: 3 emails (thank you, feedback request +7d, referral +14d)

### 2. Design the narrative arc

Each campaign follows a storytelling progression:

| Position | Purpose | Tone | CTA strength |
|---|---|---|---|
| Email 1 | Welcome/hook — establish relationship | Warm, inviting | Soft (explore) |
| Email 2 | Value delivery — teach something useful | Educational, helpful | Medium (learn more) |
| Email 3 | Social proof — show others' results | Inspirational, credible | Medium (see stories) |
| Email 4 | Overcome objections — address concerns | Empathetic, honest | Medium (get answers) |
| Email 5 | Urgency/scarcity — create momentum | Energetic, direct | Strong (act now) |
| Email 6 | Final push — last chance | Urgent, personal | Strong (don't miss out) |
| Email 7 | Graceful close — respect the decision | Respectful, warm | Soft (stay connected) |

### 3. Generate each email template

For each email in the sequence:
- React Email TSX file following the email design system
- Unique subject line + preview text
- Content sections appropriate to the narrative position
- Shared campaign header (campaign name/branding)
- Consistent footer across all emails
- Variable interpolation for personalization

### 4. Generate campaign manifest

```yaml
campaign:
  name: <campaign-name>
  type: <type>
  created: YYYY-MM-DD
  emails:
    - sequence: 1
      template_name: "<campaign>-email-1"
      subject: "..."
      preview: "..."
      send_delay: "0d"
      file: "<CampaignName>Email1.tsx"
    - sequence: 2
      template_name: "<campaign>-email-2"
      subject: "..."
      preview: "..."
      send_delay: "1d"
      file: "<CampaignName>Email2.tsx"
  shared_variables:
    - firstName
    - brandName
    - campaignUrl
```

---

## Output

Write to `templates/email/<domain>/<CampaignName>/` and report to `memory/reports/email-campaign-<name>.md`:

```markdown
## Email Campaign — <name>
Type: <type> | Emails: N | Cadence: [days]

### Sequence
| # | Subject | Preview | Delay | Narrative role |
[table]

### Shared Variables
[list]

### Files Generated
[list]
```

---

## Guidelines

- All emails share the same design tokens and header/footer treatment.
- Subject lines: max 50 chars, no ALL-CAPS, no spam triggers.
- Preview text: 90-130 chars, unique per email, complements subject.
- Each email must stand alone if read in isolation (subscriber may skip emails).
- Unsubscribe link in every email footer (CAN-SPAM compliance).
- Campaign manifest enables automation tools to schedule the sequence.
- TSX escape rules: never use unescaped `{` or `}` as literal text in JSX — use `{'{'}`/`{'}'}`. Escape apostrophes with `&apos;` or `{'\''}`. CSS style objects must use string values for properties containing braces. Always verify TSX compiles under strict mode before delivery.

---

## Error Handling

- No site context: prompt `/site <name>`.
- Invalid campaign type: show supported types.
- Template name collision: ask to rename or overwrite.
