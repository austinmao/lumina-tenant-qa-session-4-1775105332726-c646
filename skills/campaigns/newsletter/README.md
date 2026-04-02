# skills/newsletter/

9 skills (root + 8 sub-skills) that power the full newsletter pipeline.

**Replaces**: deprecated `email-newsletter` skill.

---

## Skills

| Skill | Trigger / Purpose | Deps |
|---|---|---|
| `SKILL.md` (root) | Newsletter domain router | `RESEND_API_KEY` |
| `sub-skills/brief` | Research and summarize weekly trends into a newsletter brief | — |
| `sub-skills/draft` | Write newsletter draft from brief using Chain-of-Draft | — |
| `sub-skills/subject-line` | Generate and score 5 subject line variants via Chain-of-Draft | — |
| `sub-skills/gate` | Slack approval gate — pause pipeline until Austin approves | `SLACK_BOT_TOKEN` |
| `sub-skills/segment` | Segment subscriber list for targeting | — |
| `sub-skills/deliver` | Send newsletter via Resend in batches ≤ 50 | `RESEND_API_KEY` |
| `sub-skills/re-engage` | Re-engagement sequence for inactive subscribers | — |
| `sub-skills/analytics` | Post-send analytics: opens, clicks, unsubscribes | — |

## Pipeline Order

```
brief → draft → subject-line → gate (Slack approval) → segment → deliver → analytics
```

The `gate` step is mandatory — nothing sends without Austin's explicit approval.

## Notes

- Delivery batches: max 50 recipients per Resend API call
- All sends logged to `memory/logs/sends/YYYY-MM-DD.md`
- Hard bounces → immediate list removal; soft bounces → retry after 24h, remove after 3 consecutive
