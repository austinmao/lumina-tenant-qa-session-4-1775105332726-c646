---
name: paperclip-release-watch
description: "Check if Paperclip PR #1413 merged or a new npm release dropped"
version: "1.0.0"
permissions:
  filesystem: read
  network: true
triggers:
  - command: /paperclip-release-watch
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins: ["curl", "jq"]
      env: []
---

# Paperclip Release Watch

Check whether PR #1413 (conversations feature) has merged and whether a new `paperclipai` npm release includes migration `0045_issue_kind`.

## When to Run

- On every heartbeat cycle (add to HEARTBEAT.md)
- On manual `/paperclip-release-watch` command

## Steps

### 1. Check PR #1413 Status

```bash
PR_STATE=$(curl -sf "https://api.github.com/repos/paperclipai/paperclip/pulls/1413" | jq -r '.state')
PR_MERGED=$(curl -sf "https://api.github.com/repos/paperclipai/paperclip/pulls/1413" | jq -r '.merged')
```

- If `merged == true`: PR has been merged. Proceed to step 2.
- If `state == open`: Still waiting. Report "PR #1413 still open" and stop.
- If `state == closed` and `merged == false`: PR was closed without merge. Alert operator.

### 2. Check npm Release Version

```bash
LATEST=$(curl -sf "https://registry.npmjs.org/paperclipai" | jq -r '.["dist-tags"].latest')
CURRENT="2026.325.0"
```

- If `LATEST != CURRENT`: A new version was published.
- Download and check if it includes the conversations migration:
  ```bash
  npm pack paperclipai@$LATEST --pack-destination /tmp 2>/dev/null
  tar -tzf /tmp/paperclipai-*.tgz | grep -q "0045_issue_kind" && echo "HAS_CONVERSATIONS=true"
  ```

### 3. Action on New Release with Conversations

If a new release includes the conversations feature:

1. **Notify operator via Slack**: "Paperclip $LATEST released with conversations (PR #1413). Ready to switch from submodule to npm package."
2. **Provide upgrade commands**:
   ```
   npm install -g paperclipai@$LATEST
   # Then remove submodule:
   git submodule deinit services/paperclip
   git rm services/paperclip
   rm -rf .git/modules/services/paperclip
   ```
3. **Mark this heartbeat task as DONE** — remove from HEARTBEAT.md.

### 4. No Action Needed

If PR is still open or release doesn't include conversations: log check timestamp and do nothing.

## State File

Write check results to `memory/logs/paperclip-watch/YYYY-MM-DD.yaml`:

```yaml
checked_at: "2026-03-26T12:00:00Z"
pr_1413_state: open|merged|closed
npm_latest: "2026.325.0"
has_conversations: false
action: none|notify_operator
```
