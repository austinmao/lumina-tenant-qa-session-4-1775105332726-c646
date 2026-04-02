# skills/trend-intelligence/

4 skills (root + 3 sub-skills) for psychedelic/plant medicine trend research.

**Primary consumer**: `newsletter` pipeline (`brief` sub-skill calls `trend-intelligence/scan`)

---

## Skills

| Skill | Purpose | Deps |
|---|---|---|
| `SKILL.md` (root) | Trend intelligence domain router | `BRAVE_API_KEY` |
| `sub-skills/scan` | Web search for trending psychedelic/wellness topics via Brave Search | `BRAVE_API_KEY` |
| `sub-skills/score` | Scores trends by relevance, novelty, and audience fit | — |
| `sub-skills/brief` | Synthesizes scored trends into a structured brief for the newsletter agent | — |

## Pipeline

```
scan (Brave Search) → score → brief → newsletter/brief
```

## Notes

- Rate limits: max 5 searches per batch, 10s between searches, 429 → wait 5min
- Trend scoring criteria: psychedelic/plant medicine relevance, publication recency, audience alignment (the organization's audience)
- Output format: structured markdown brief with headline, context, and suggested newsletter angle per trend
