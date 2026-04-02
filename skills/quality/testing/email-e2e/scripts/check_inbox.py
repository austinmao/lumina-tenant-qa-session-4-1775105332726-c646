#!/usr/bin/env python3
"""
check_inbox.py — Poll the AgentMail QA inbox until the test email arrives.

Matches on subject containing the E2E-<uuid> test identifier.

Usage:
    python3 check_inbox.py \\
        --inbox lumina.qa@agentmail.to \\
        --test-id E2E-<uuid> \\
        [--timeout 60] \\
        [--poll-interval 10]

Output: JSON with message content on success, or error on timeout.
  Success: {"found": true, "subject": "...", "html": "...", "text": "...", "received_at": "..."}
  Timeout: {"found": false, "error": "timeout after <N>s", "failure_class": "external"}
  API err:  {"found": false, "error": "<message>", "failure_class": "infrastructure"}
Exit 0 on found, 1 on not found (timeout), 2 on API/config error.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


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


def main() -> None:
    config = load_qa_config()

    parser = argparse.ArgumentParser(description="Poll AgentMail inbox for test email")
    parser.add_argument("--inbox", default=config["agentmail_inbox"])
    parser.add_argument("--test-id", required=True, help="E2E-<uuid> identifier to match in subject")
    parser.add_argument("--timeout", type=int, default=config["email_e2e_timeout_seconds"])
    parser.add_argument("--poll-interval", type=int, default=config["email_e2e_poll_interval_seconds"])
    args = parser.parse_args()

    api_key = os.environ.get("AGENTMAIL_API_KEY")
    if not api_key:
        print(json.dumps({"found": False, "error": "AGENTMAIL_API_KEY not set", "failure_class": "infrastructure"}), file=sys.stderr)
        sys.exit(2)

    try:
        from agentmail import AgentMail
    except ImportError:
        print(json.dumps({"found": False, "error": "agentmail package not installed. Run: pip install agentmail", "failure_class": "infrastructure"}), file=sys.stderr)
        sys.exit(2)

    client = AgentMail(api_key=api_key)
    deadline = time.monotonic() + args.timeout
    poll_count = 0

    while time.monotonic() < deadline:
        try:
            messages = client.messages.list(inbox_id=args.inbox)
            # Handle both list and object responses
            items = messages if isinstance(messages, list) else getattr(messages, "messages", []) or []
            for msg in items:
                subject = getattr(msg, "subject", "") or (msg.get("subject", "") if isinstance(msg, dict) else "")
                if args.test_id in subject:
                    # Extract body content
                    html_body = getattr(msg, "html", "") or (msg.get("html", "") if isinstance(msg, dict) else "")
                    text_body = getattr(msg, "text", "") or (msg.get("text", "") if isinstance(msg, dict) else "")
                    received_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    result = {
                        "found": True,
                        "subject": subject,
                        "html": html_body,
                        "text": text_body,
                        "received_at": received_str,
                    }
                    print(json.dumps(result))
                    sys.exit(0)
        except Exception as exc:
            print(json.dumps({"found": False, "error": str(exc), "failure_class": "infrastructure"}), file=sys.stderr)
            sys.exit(2)

        poll_count += 1
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(args.poll_interval, max(0, remaining)))

    print(json.dumps({
        "found": False,
        "error": f"timeout after {args.timeout}s ({poll_count} polls)",
        "failure_class": "external",
    }))
    sys.exit(1)


if __name__ == "__main__":
    main()
