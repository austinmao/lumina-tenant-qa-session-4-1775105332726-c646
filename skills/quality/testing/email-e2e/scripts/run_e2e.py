#!/usr/bin/env python3
"""
run_e2e.py — Main entrypoint for email E2E testing.

Orchestrates:  send_test.py → check_inbox.py → assert_email.py

Usage:
    python3 run_e2e.py \\
        --subject "Your Retreat Awaits" \\
        --html-file /path/to/rendered.html \\
        [--inbox lumina.qa@agentmail.to] \\
        [--timeout 60] \\
        [--poll-interval 10] \\
        [--kill-list-file /path/to/kill-list.txt]

Output: YAML to stdout per contracts/email-e2e-assertion.md
Exit 0 (all PASS), 1 (any check FAIL), 2 (script/API error)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def yaml_output(data: dict) -> str:
    try:
        import yaml
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    except ImportError:
        # minimal fallback
        lines = [f"overall: {data['overall']}"]
        if data.get("test_email_id"):
            lines.append(f"test_email_id: {data['test_email_id']}")
        if data.get("sent_at"):
            lines.append(f"sent_at: '{data['sent_at']}'")
        if data.get("received_at"):
            lines.append(f"received_at: '{data['received_at']}'")
        else:
            lines.append("received_at: null")
        lines.append("checks:")
        for c in data.get("checks", []):
            lines.append(f"  - name: {c['name']}")
            lines.append(f"    status: {c['status']}")
            detail = c.get("detail")
            lines.append(f"    detail: {repr(detail) if detail else 'null'}")
            fc = c.get("failure_class")
            lines.append(f"    failure_class: {fc if fc else 'null'}")
        return "\n".join(lines) + "\n"


def load_qa_config() -> dict:
    defaults = {
        "agentmail_inbox": "lumina.qa@agentmail.to",
        "email_e2e_timeout_seconds": 60,
        "email_e2e_poll_interval_seconds": 10,
    }
    config_path = Path("config/org.yaml")
    if not config_path.exists():
        return defaults
    try:
        import yaml
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        qa = raw.get("qa", {})
        return {
            "agentmail_inbox": qa.get("agentmail_inbox", defaults["agentmail_inbox"]),
            "email_e2e_timeout_seconds": qa.get("email_e2e_timeout_seconds", defaults["email_e2e_timeout_seconds"]),
            "email_e2e_poll_interval_seconds": qa.get("email_e2e_poll_interval_seconds", defaults["email_e2e_poll_interval_seconds"]),
        }
    except Exception:
        return defaults


def run_script(script_path: str, args: list[str]) -> tuple[int, str, str]:
    """Run a Python script as subprocess. Returns (returncode, stdout, stderr)."""
    cmd = [sys.executable, script_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def ensure_inbox_capacity(inbox: str, api_key: str, cap: int = 6) -> None:
    """Ensure AgentMail inbox has room for at least 1 new message.
    AgentMail free tier caps at 6 messages. Only deletes the minimum necessary
    (oldest threads first) to avoid triggering AgentMail's anti-abuse lockout.
    Mass-deleting all threads causes a cooldown that blocks new delivery for ~5 minutes."""
    try:
        import httpx
        headers = {"Authorization": f"Bearer {api_key}"}
        resp = httpx.get(
            f"https://api.agentmail.to/v0/inboxes/{inbox}/threads",
            headers=headers,
            params={"limit": 50},
            timeout=10.0,
        )
        if resp.status_code != 200:
            return  # Non-fatal — continue anyway
        threads = resp.json().get("threads", [])
        # Only delete the oldest threads to free exactly enough space
        need_to_delete = max(0, len(threads) - (cap - 1))
        for t in threads[-need_to_delete:] if need_to_delete else []:
            tid = t.get("thread_id", "")
            if tid:
                httpx.delete(
                    f"https://api.agentmail.to/v0/inboxes/{inbox}/threads/{tid}",
                    headers=headers,
                    timeout=10.0,
                )
    except Exception:
        pass  # Capacity check failure is non-fatal; send will proceed


def main() -> None:
    config = load_qa_config()

    parser = argparse.ArgumentParser(description="Run full email E2E test pipeline")
    parser.add_argument("--subject", required=True, help="Expected subject line (without E2E prefix)")
    parser.add_argument("--html-file", required=True, help="Path to rendered HTML email file")
    parser.add_argument("--inbox", default=config["agentmail_inbox"])
    parser.add_argument("--timeout", type=int, default=config["email_e2e_timeout_seconds"])
    parser.add_argument("--poll-interval", type=int, default=config["email_e2e_poll_interval_seconds"])
    parser.add_argument("--kill-list-file", default=None)
    args = parser.parse_args()

    # Resolve script paths relative to this file
    scripts_dir = Path(__file__).parent
    send_script = str(scripts_dir / "send_test.py")
    check_script = str(scripts_dir / "check_inbox.py")
    assert_script = str(scripts_dir / "assert_email.py")

    sent_at = now_iso()
    test_email_id = None
    received_at = None

    # ── Stage 0: Ensure inbox capacity (AgentMail free tier caps at 6 messages) ─
    api_key = os.environ.get("AGENTMAIL_API_KEY", "")
    if api_key:
        ensure_inbox_capacity(args.inbox, api_key)

    # ── Stage 1: Send test email ─────────────────────────────────────────────
    send_args = ["--subject", args.subject, "--html-file", args.html_file, "--to-inbox", args.inbox]
    rc, stdout, stderr = run_script(send_script, send_args)
    if rc != 0:
        delivery_check = {
            "name": "delivery",
            "status": "FAIL",
            "detail": stderr or stdout or "send_test.py failed",
            "failure_class": "infrastructure",
        }
        result = {
            "overall": "FAIL",
            "test_email_id": None,
            "sent_at": sent_at,
            "received_at": None,
            "checks": [delivery_check] + [
                {"name": n, "status": "SKIP", "detail": "send failed", "failure_class": None}
                for n in ("subject_match", "body_nonempty", "links_health", "unsubscribe", "brand_kill_list")
            ],
        }
        print(yaml_output(result))
        sys.exit(1)

    try:
        send_data = json.loads(stdout)
        test_email_id = send_data["test_email_id"]
    except (json.JSONDecodeError, KeyError) as exc:
        print(f"run_e2e.py: failed to parse send_test.py output: {exc}", file=sys.stderr)
        sys.exit(2)

    # ── Stage 2: Poll inbox for email arrival ────────────────────────────────
    # Wait 30s before polling — AgentMail's anti-abuse system throttles deliveries
    # when rapid API polling is detected immediately after a send.
    time.sleep(30)
    check_args = [
        "--inbox", args.inbox,
        "--test-id", test_email_id,
        "--timeout", str(args.timeout),
        "--poll-interval", str(args.poll_interval),
    ]
    rc, stdout, stderr = run_script(check_script, check_args)

    if rc != 0:
        # Delivery failed or timed out
        try:
            check_data = json.loads(stdout or stderr)
            fc = check_data.get("failure_class", "external")
            detail = check_data.get("error", "email not received")
        except json.JSONDecodeError:
            fc = "external"
            detail = "email not received within timeout"

        delivery_check = {
            "name": "delivery",
            "status": "FAIL",
            "detail": detail,
            "failure_class": fc,
        }
        result = {
            "overall": "FAIL",
            "test_email_id": test_email_id,
            "sent_at": sent_at,
            "received_at": None,
            "checks": [delivery_check] + [
                {"name": n, "status": "SKIP", "detail": "delivery failed", "failure_class": None}
                for n in ("subject_match", "body_nonempty", "links_health", "unsubscribe", "brand_kill_list")
            ],
        }
        print(yaml_output(result))
        sys.exit(1)

    try:
        inbox_data = json.loads(stdout)
        received_at = inbox_data.get("received_at", now_iso())
        received_html = inbox_data.get("html", "")
        received_subject = inbox_data.get("subject", "")
    except json.JSONDecodeError as exc:
        print(f"run_e2e.py: failed to parse check_inbox.py output: {exc}", file=sys.stderr)
        sys.exit(2)

    delivery_check = {
        "name": "delivery",
        "status": "PASS",
        "detail": f"Email received at {received_at}",
        "failure_class": None,
    }

    # ── Stage 3: Run assertion suite ────────────────────────────────────────
    assert_args = [
        "--expected-subject", args.subject,
        "--received-html", received_html,
        "--received-subject", received_subject,
    ]
    if args.kill_list_file:
        assert_args += ["--kill-list-file", args.kill_list_file]

    rc, assert_stdout, assert_stderr = run_script(assert_script, assert_args)

    if not assert_stdout:
        print(f"run_e2e.py: assert_email.py produced no output (stderr: {assert_stderr})", file=sys.stderr)
        sys.exit(2)

    # Parse assertion checks from assert_email.py YAML output
    try:
        import yaml
        assert_data = yaml.safe_load(assert_stdout) or {}
    except Exception:
        # Fallback: if yaml unavailable, relay raw output
        print(f"overall: FAIL\ntest_email_id: {test_email_id}\nsent_at: '{sent_at}'\nreceived_at: '{received_at}'\n{assert_stdout}")
        sys.exit(rc)

    assert_checks = assert_data.get("checks", [])
    all_checks = [delivery_check] + assert_checks

    any_fail = any(c["status"] == "FAIL" for c in all_checks)
    final_result = {
        "overall": "FAIL" if any_fail else "PASS",
        "test_email_id": test_email_id,
        "sent_at": sent_at,
        "received_at": received_at,
        "checks": all_checks,
    }

    print(yaml_output(final_result))
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
