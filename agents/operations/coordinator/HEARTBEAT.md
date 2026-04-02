# HEARTBEAT.md

## Paperclip Release Watch

Check if Paperclip PR #1413 (conversations feature) has merged and whether a new npm release includes it. When the release lands, notify Austin via Slack so we can switch from the git submodule back to the npm package.

**How**: Run `bash scripts/paperclip-release-watch.sh` and read the output.
**When done**: Remove this task once we've upgraded to the npm release with conversations.
