---
name: deployment
description: "Deploy the website / check deployment status / which domain serves what"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /deployment
  - command: /deploy
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["vercel"]
      env: ["VERCEL_API_TOKEN"]
---

# the organization Deployment Reference

Use this skill when deploying, checking domain routing, or generating URLs for the organization web properties.

## Domain Map

| Domain | Purpose | Vercel Config |
|---|---|---|
| `live.[the organization's domain]` | Customer-facing site — all public pages, presentations, events | Production domain in Vercel dashboard |
| `admin.[the organization's domain]` | Admin panel — campaign management, internal dashboards | `vercel.json` alias |
| `preview.[the organization's domain]` | Preview deployments for staging | Vercel preview domain |

All domains point to the same Vercel project: `acme-org-team/web`.

## URL Schema (canonical)

All new links MUST use the event-scoped URL pattern. Never use the legacy `/presentation/{slug}` pattern in new copy or links.

| Page Type | URL Pattern | Example |
|---|---|---|
| Event landing | `/event/{event-slug}` | `/event/have-a-good-trip` |
| Presentation | `/event/{event-slug}/presentation` | `/event/have-a-good-trip/presentation` |
| Presenter view | `/event/{event-slug}/presentation/presenter` | `/event/have-a-good-trip/presentation/presenter` |
| Replay | `/event/{event-slug}/replay` | `/event/have-a-good-trip/replay` |
| Thank you | `/event/{event-slug}/thank-you` | `/event/have-a-good-trip/thank-you` |
| Next steps | `/event/{event-slug}/next-steps` | `/event/have-a-good-trip/next-steps` |
| Registration | `/event/{event-slug}` | `/event/have-a-good-trip` |

Legacy `/presentation/{slug}` URLs redirect via 301 to the event-scoped path. The dynamic `[slug]` route still works for backwards compatibility but should not be used in new links.

## Brand Link Rules

- the organization logo in presentations always links to `https://www.[the organization's domain]`
- CTA / breakthrough call URL: `https://www.[the organization's domain]/start/breakthrough-call`
- Contact email: `info@[the organization's domain]` (never `austin@`)

## Deploy Commands

```bash
# Link to project (required once per machine)
npx vercel link --project web --scope acme-org-team --yes

# Deploy to production
npx vercel --prod --yes

# Check latest deployments
npx vercel ls
```

## Post-Deploy Verification

After deploying, verify the live domain is serving updated content:

```bash
curl -s "https://live.[the organization's domain]/" -o /dev/null -w "HTTP %{http_code}"
```

If stale content persists after a successful Vercel deployment, check:
1. Vercel edge cache (may take 1-2 minutes to propagate)
2. Domain assignment in Vercel dashboard (Settings > Domains)
3. DNS resolution: `dig live.[the organization's domain] +short` should return Vercel IPs (76.76.21.x)
