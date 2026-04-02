#!/usr/bin/env python3
"""
cleanup_retention.py — Prune old retry state files per retention policy.

Reads retention config from config/org.yaml:
  retry_gate.retention_days            — days to keep PASSED files (default: 30)
  retry_gate.retention_keep_exhausted  — whether to keep EXHAUSTED files longer (default: true)
  retry_gate.retention_exhausted_days  — days to keep EXHAUSTED files (default: 90)

Usage:
    python3 cleanup_retention.py [--dry-run]

Output: JSON with {"deleted": [<paths>], "kept": <count>, "errors": [<messages>]}
Exit 0 always (cleanup errors are non-fatal).
"""

import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def load_config() -> dict:
    """Load retry_gate section from config/org.yaml. Returns defaults if missing."""
    defaults = {
        "retention_days": 30,
        "retention_keep_exhausted": True,
        "retention_exhausted_days": 90,
    }
    config_path = Path("config/org.yaml")
    if not config_path.exists():
        return defaults
    try:
        import yaml
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        rg = raw.get("retry_gate", {})
        return {
            "retention_days": rg.get("retention_days", defaults["retention_days"]),
            "retention_keep_exhausted": rg.get(
                "retention_keep_exhausted", defaults["retention_keep_exhausted"]
            ),
            "retention_exhausted_days": rg.get(
                "retention_exhausted_days", defaults["retention_exhausted_days"]
            ),
        }
    except Exception:
        return defaults


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter. Returns empty dict on failure."""
    try:
        import yaml
        lines = content.splitlines()
        if not lines or lines[0].strip() != "---":
            return {}
        end = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                end = i
                break
        if end is None:
            return {}
        return yaml.safe_load("\n".join(lines[1:end])) or {}
    except Exception:
        return {}


def main() -> None:
    parser = argparse.ArgumentParser(description="Cleanup old retry state files")
    parser.add_argument("--dry-run", action="store_true", help="Report without deleting")
    args = parser.parse_args()

    config = load_config()
    retention_days = config["retention_days"]
    keep_exhausted = config["retention_keep_exhausted"]
    exhausted_days = config["retention_exhausted_days"]

    logs_dir = Path("memory/logs/retry")
    if not logs_dir.exists():
        print(json.dumps({"deleted": [], "kept": 0, "errors": []}))
        return

    now = datetime.now(timezone.utc)
    deleted = []
    kept = 0
    errors = []

    for md_file in sorted(logs_dir.glob("*.md")):
        if md_file.name == ".gitkeep":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            fm = parse_frontmatter(content)
            status = fm.get("status", "")
            started_at_raw = fm.get("started_at") or fm.get("resolved_at")

            if not started_at_raw:
                # Fall back to file modification time
                mtime = datetime.fromtimestamp(md_file.stat().st_mtime, tz=timezone.utc)
                file_age_days = (now - mtime).days
            else:
                started_at = datetime.fromisoformat(
                    started_at_raw.replace("Z", "+00:00")
                )
                file_age_days = (now - started_at).days

            should_delete = False
            if status == "PASSED" and file_age_days > retention_days:
                should_delete = True
            elif status == "EXHAUSTED":
                if keep_exhausted:
                    if file_age_days > exhausted_days:
                        should_delete = True
                else:
                    if file_age_days > retention_days:
                        should_delete = True
            elif status == "IN_PROGRESS":
                # Never auto-delete in-progress files
                should_delete = False
            else:
                # Unknown status — apply standard retention
                if file_age_days > retention_days:
                    should_delete = True

            if should_delete:
                if not args.dry_run:
                    md_file.unlink()
                deleted.append(str(md_file))
            else:
                kept += 1

        except Exception as exc:
            errors.append(f"{md_file.name}: {exc}")
            kept += 1  # Keep files we can't parse

    result = {"deleted": deleted, "kept": kept, "errors": errors}
    if args.dry_run:
        result["dry_run"] = True
    print(json.dumps(result))


if __name__ == "__main__":
    main()
