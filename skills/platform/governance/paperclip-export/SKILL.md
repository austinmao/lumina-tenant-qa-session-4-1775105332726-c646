---
name: paperclip-export
description: "Generate Paperclip export from governance records"
version: "1.0.0"
permissions:
  filesystem: write
  network: false
triggers:
  - command: /paperclip-export
metadata:
  openclaw:
    emoji: "\U0001F4CE"
    requires:
      bins: ["python3"]
      env: []
      os: ["darwin"]
---

# Paperclip Export

Generates YAML export artifacts in `governance/exports/paperclip/` from governance records.

## How to Run

```bash
python3 scripts/scaffold.py export-paperclip
```

## Output Files

- `governance/exports/paperclip/company.yaml` — tenant metadata
- `governance/exports/paperclip/agents.yaml` — all exported agent records
- `governance/exports/paperclip/teams.yaml` — team structure

## Export Policy

Exported by default:
- Active agents with `paperclip.export: true`

Not exported:
- Sub-skills
- Deprecated records
- Non-active records
- Records with `paperclip.export: false`
