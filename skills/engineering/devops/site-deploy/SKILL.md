---
name: site-deploy
description: "Deploy site to Vercel / deploy to staging / deploy to production"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /deploy-site
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["vercel"]
      env: ["VERCEL_TOKEN"]
      os: ["darwin"]
---

# Site Deploy Skill

Deploys the active site to Vercel (preview or production).

---

## Prerequisites

1. Read `memory/site-context.yaml` to resolve the active site.
   - If the file does not exist: respond "No active site set. Run `/site <name>` first." and stop.
2. Extract `vercel.project`, `vercel.team`, and `site_dir` from site context.
3. Verify the `sites/<site_dir>` directory exists.

---

## Steps

### Preview deploy (default)

1. **Requires the operator approval before deploy.** Summarize what will be deployed (site name, directory, project) and wait for confirmation.
2. Run:
   ```
   vercel deploy --token $VERCEL_TOKEN --scope <team> <site_dir> --yes
   ```
3. Capture the preview URL from stdout.
4. Report: site name, preview URL, deployment status.

### Production deploy

1. User must explicitly say "production" or "prod".
2. **Requires the operator approval before deploy.** Warn that this pushes to the live domain.
3. Run:
   ```
   vercel deploy --token $VERCEL_TOKEN --scope <team> <site_dir> --prod --yes
   ```
4. Capture the production URL from stdout.
5. Report: site name, production URL, deployment status.

### Check deployment status

1. Run:
   ```
   vercel ls --token $VERCEL_TOKEN --scope <team> <site_dir> --limit 5
   ```
2. Display the 5 most recent deployments with status, URL, and timestamp.

---

## Output

- **Preview**: Preview URL, deployment ID, build time.
- **Production**: Production URL, deployment ID, confirmation that the live domain is updated.
- **Status**: Table of recent deployments (state, URL, created date).

---

## Error Handling

- If `memory/site-context.yaml` is missing: prompt user to run `/site <name>`.
- If `VERCEL_TOKEN` is not set: notify user to add it to `~/.openclaw/.env`.
- If `site_dir` does not exist: report the expected path and stop.
- If `vercel` CLI returns a build error: display the full error output and suggest checking build logs.
- If deploy fails with 403: token may lack deploy permissions for the project -- advise checking token scopes.
