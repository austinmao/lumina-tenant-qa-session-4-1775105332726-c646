#!/usr/bin/env python3
"""
read_state.py — Read retry state file for a given workflow+step.

Usage:
    python3 read_state.py --workflow <workflow> --step <step>

Output: JSON to stdout.
  If file exists: {"exists": true, "run_id": ..., "workflow": ..., "step": ...,
                   "max_attempts": ..., "cooldown_seconds": ..., "escalation_channel": ...,
                   "escalation_target": ..., "started_at": ..., "resolved_at": ...,
                   "status": ..., "attempts": [...]}
  If not found:   {"exists": false}
  On parse error: {"exists": false, "error": "<message>"}

State files live at: memory/logs/retry/YYYY-MM-DD-<workflow>-<step>.md
The date is today's local date (matches the date the gate was first invoked).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def find_state_file(workflow: str, step: str) -> Path | None:
    """Find an existing state file for this workflow+step (any date, most recent first)."""
    logs_dir = Path("memory/logs/retry")
    if not logs_dir.exists():
        return None
    pattern = re.compile(rf"^\d{{4}}-\d{{2}}-\d{{2}}-{re.escape(workflow)}-{re.escape(step)}\.md$")
    matches = sorted(
        [f for f in logs_dir.iterdir() if pattern.match(f.name)],
        key=lambda f: f.name,
        reverse=True,
    )
    return matches[0] if matches else None


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a Markdown file (between --- delimiters)."""
    import yaml  # lazy import — only needed here

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("No YAML frontmatter found")
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("Unclosed YAML frontmatter")
    yaml_text = "\n".join(lines[1:end])
    return yaml.safe_load(yaml_text) or {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Read retry gate state file")
    parser.add_argument("--workflow", required=True, help="Workflow identifier")
    parser.add_argument("--step", required=True, help="Step identifier")
    args = parser.parse_args()

    state_file = find_state_file(args.workflow, args.step)
    if state_file is None:
        print(json.dumps({"exists": False}))
        return

    try:
        content = state_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
    except Exception as exc:
        print(json.dumps({"exists": False, "error": str(exc)}))
        return

    output = {
        "exists": True,
        "path": str(state_file),
        "run_id": fm.get("run_id"),
        "workflow": fm.get("workflow"),
        "step": fm.get("step"),
        "max_attempts": fm.get("max_attempts"),
        "cooldown_seconds": fm.get("cooldown_seconds"),
        "escalation_channel": fm.get("escalation_channel"),
        "escalation_target": fm.get("escalation_target"),
        "started_at": fm.get("started_at"),
        "resolved_at": fm.get("resolved_at"),
        "status": fm.get("status"),
        "attempts": fm.get("attempts", []),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
