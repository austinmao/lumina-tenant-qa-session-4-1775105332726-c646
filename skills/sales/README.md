# skills/sales/

6 sales skills shared across the sales domain agents.

**Agents that load these skills**: `sales/director`, `sales/enrollment`, `sales/lead-nurture`,
`sales/coach`, `sales/concierge`

---

## Skills

| Skill | Trigger | Purpose | Deps |
|---|---|---|---|
| `sales` (root) | Sales domain routing | Router — selects sub-skill by request | — |
| `deal-management` | Manage deals in Attio | Create/update/close deals; log touchpoints via `log-to-attio` | `ATTIO_API_KEY` |
| `fireflies-sync` | Sync Fireflies transcripts | Pull post-call transcripts, extract action items | — |
| `pipeline-triggers` | Pipeline stage triggers | Rules for stage advancement: lead → prospect → qualified → enrolled | — |
| `sales-messaging` | Write sales message | Consultative, trauma-informed sales copy | — |
| `sales-sequences` | Write follow-up sequence | 4-touch 14-day follow-up cadence (D+1, D+3, D+7, D+14) | — |

## Notes

- `deal-management` delegates all send-logging to `skills/resend/log-to-attio/SKILL.md` — never log touches manually.
- `pipeline-triggers` coordinates with `calendly-direct` for booking events and `fireflies-sync` for post-call state changes.
