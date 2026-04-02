---
name: vercel-deployment
description: >
  Set up a Vercel project, configure deployment settings, run preview deploys,
  manage environment variables, and promote to production. Use when deploying a
  Next.js site to Vercel or managing Vercel project configuration.
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /vercel-deployment
metadata:
  openclaw:
    emoji: "rocket"
    requires:
      bins: ["vercel"]
      env:
        - VERCEL_TOKEN
        - VERCEL_ORG_ID
---

# Vercel Deployment

## Overview

Manage Vercel project setup and deployments for Next.js applications. This
skill handles project initialization, environment variable configuration,
preview deployments, production promotion, and rollback. All production
deployments require explicit operator approval. Preview deploys can proceed
without approval.

## Approval Gate

- **Preview deploys**: allowed without operator approval.
- **Production deploys**: require explicit operator approval in the current
  session. I will present the preview URL, build status, and a summary of
  changes before asking for approval.
- **Environment variable changes**: require operator approval before applying
  to production. Staging/preview changes can proceed without approval.

## Steps

1. **Verify prerequisites.** Confirm `vercel` CLI is installed and
   `VERCEL_TOKEN` and `VERCEL_ORG_ID` are set. Run `vercel whoami` to
   verify authentication.

2. **Project setup** (if new project):
   - Run `vercel link` to connect the local directory to a Vercel project.
   - Set the framework preset to Next.js.
   - Configure the root directory if the app is in a subdirectory.
   - Set Node.js version to match the project's `.nvmrc` or `engines` field.

3. **Configure environment variables.** For each required variable:
   - Set for the appropriate scope: `production`, `preview`, or `development`.
   - Never log or display variable values — only confirm the variable name
     and scope were set.
   - Use `vercel env add` for new variables.
   - Use `vercel env rm` + `vercel env add` for updates (no in-place edit).

4. **Run preview deployment.**
   ```bash
   vercel --token $VERCEL_TOKEN --yes
   ```
   - Capture the preview URL from the output.
   - Wait for the build to complete.
   - Report: preview URL, build duration, any build warnings.

5. **Validate preview.** Before requesting production approval:
   - Confirm the preview URL loads successfully (HTTP 200).
   - Check for build warnings or errors in the deployment log.
   - If the QA Engineer is available, request a preview audit.

6. **Promote to production** (after operator approval):
   ```bash
   vercel --prod --token $VERCEL_TOKEN --yes
   ```
   - Report: production URL, build duration, deployment ID.
   - Verify the production URL returns HTTP 200.

7. **Rollback** (if production deploy is broken):
   - Identify the last known-good deployment ID.
   - Run `vercel rollback [deployment-id] --token $VERCEL_TOKEN`.
   - Verify the rollback succeeded.
   - Notify the operator with the rollback details.

8. **Domain configuration** (if needed):
   - Add custom domain: `vercel domains add [domain]`.
   - Verify DNS is pointed correctly.
   - Confirm SSL certificate is provisioned.

## Output

- **For preview deploys**: preview URL, build status, build duration, warnings.
- **For production deploys**: production URL, deployment ID, build status.
- **For rollbacks**: previous deployment ID, rollback deployment ID, status.
- **For project setup**: project ID, linked directory, framework preset, node version.

## Error Handling

- If `VERCEL_TOKEN` is not set: stop and ask the operator to set it.
- If `vercel` CLI is not installed: recommend `npm i -g vercel` and stop.
- If build fails: report the error summary from the build log. Do not retry
  automatically — the error likely requires code changes.
- If preview URL returns non-200: report the status code and check the
  deployment function logs for errors.
- If production deploy fails after approval: immediately attempt rollback to
  the previous deployment and notify the operator.
- If domain DNS is not configured: report the required DNS records and stop.
