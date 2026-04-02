#!/usr/bin/env python3
"""
write_state.py — Write or update a retry state file for a given workflow+step.

Uses atomic writes (write to .tmp, then os.replace() to final path) to prevent
corruption if the process is interrupted.

Usage:
    python3 write_state.py \\
        --workflow <workflow> \\
        --step <step> \\
        --run-id <uuid4>              \\  # Required
        --max-attempts <int>          \\
        --cooldown-seconds <int>      \\
        --escalation-channel <str>    \\
        --escalation-target <str>     \\
        --attempt-result PASS|FAIL    \\
        --attempt-number <int>        \\  # Required when FAIL
        --failures '<json_list>'      \\  # Optional: list of {class, detail, routed_to}
        --remediation '<text>'        \\  # Optional: what was fixed before this attempt
        --status IN_PROGRESS|PASSED|EXHAUSTED

Output: JSON with {"path": "<state_file_path>", "status": "<new_status>"}
Exit 0 on success, 1 on error.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def state_file_path(workflow: str, step: str) -> Path:
    logs_dir = Path("memory/logs/retry")
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / f"{today_str()}-{workflow}-{step}.md"


def load_existing(path: Path) -> dict:
    """Load existing frontmatter and attempts list. Returns empty dict if not found."""
    if not path.exists():
        return {}
    try:
        import yaml
        content = path.read_text(encoding="utf-8")
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


def load_existing_body(path: Path) -> str:
    """Load the Markdown body (after frontmatter) from existing state file."""
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return content
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return ""
    # Skip blank line after closing ---
    body_lines = lines[end + 1:]
    return "\n".join(body_lines).strip()


def build_frontmatter(data: dict) -> str:
    import yaml
    return "---\n" + yaml.dump(data, default_flow_style=False, allow_unicode=True) + "---"


def build_attempt_section(attempt_number: int, result: str, failures: list, remediation: str) -> str:
    lines = [f"\n## Attempt {attempt_number} — {result}"]
    lines.append(f"- **timestamp**: {now_iso()}")
    if result == "FAIL" and failures:
        lines.append("- **failures**:")
        for f in failures:
            cls = f.get("class", "unknown")
            detail = f.get("detail", "")
            routed = f.get("routed_to")
            route_str = f" → routed to {routed}" if routed else ""
            lines.append(f"  - [{cls}] {detail}{route_str}")
    elif result == "PASS":
        lines.append("- **result**: All checks passed")
    if remediation:
        lines.append(f"- **remediation**: {remediation}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write retry gate state file")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--step", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument("--cooldown-seconds", type=int, default=0)
    parser.add_argument("--escalation-channel", default="imessage")
    parser.add_argument("--escalation-target", default="austin")
    parser.add_argument("--attempt-result", required=True, choices=["PASS", "FAIL"])
    parser.add_argument("--attempt-number", type=int, default=1)
    parser.add_argument("--failures", default="[]", help="JSON list of failure objects")
    parser.add_argument("--remediation", default="")
    parser.add_argument("--status", required=True, choices=["IN_PROGRESS", "PASSED", "EXHAUSTED"])
    args = parser.parse_args()

    try:
        failures = json.loads(args.failures)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"Invalid --failures JSON: {exc}"}), file=sys.stderr)
        sys.exit(1)

    path = state_file_path(args.workflow, args.step)
    existing = load_existing(path)
    existing_body = load_existing_body(path)

    # Build attempts list (structured data in frontmatter)
    attempts_list = existing.get("attempts", [])
    new_attempt = {
        "n": args.attempt_number,
        "timestamp": now_iso(),
        "result": args.attempt_result,
    }
    if failures:
        new_attempt["failures"] = failures
    if args.remediation:
        new_attempt["remediation"] = args.remediation
    attempts_list.append(new_attempt)

    resolved_at = None
    if args.status in ("PASSED", "EXHAUSTED"):
        resolved_at = now_iso()

    frontmatter_data = {
        "run_id": args.run_id,
        "workflow": args.workflow,
        "step": args.step,
        "max_attempts": args.max_attempts,
        "cooldown_seconds": args.cooldown_seconds,
        "escalation_channel": args.escalation_channel,
        "escalation_target": args.escalation_target,
        "started_at": existing.get("started_at") or now_iso(),
        "resolved_at": resolved_at,
        "status": args.status,
        "attempts": attempts_list,
    }

    # Build new Markdown body section for this attempt
    new_section = build_attempt_section(
        args.attempt_number, args.attempt_result, failures, args.remediation
    )

    # Compose full file content
    header = f"# Retry State: {args.workflow} / {args.step}"
    if existing_body:
        body = existing_body + new_section
    else:
        body = header + new_section

    content = build_frontmatter(frontmatter_data) + "\n\n" + body + "\n"

    # Atomic write
    tmp_path = path.with_suffix(".md.tmp")
    try:
        tmp_path.write_text(content, encoding="utf-8")
        os.replace(tmp_path, path)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    print(json.dumps({"path": str(path), "status": args.status}))


if __name__ == "__main__":
    main()
