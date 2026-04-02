#!/usr/bin/env python3
"""
send_test.py — Send a test email via Resend to the QA inbox.

Generates a unique E2E-<uuid> test identifier and prepends it to the subject line.
This allows check_inbox.py to match the exact test email by subject.

Usage:
    python3 send_test.py \\
        --subject "Your Retreat Awaits" \\
        --html-file /path/to/rendered.html \\
        [--from-address "info@mail.example.org"] \\
        [--to-inbox "lumina.qa@agentmail.to"]

Output: JSON with {"message_id": "<resend_id>", "test_email_id": "E2E-<uuid>"}
Exit 0 on success, 2 on error.
"""

import argparse
import json
import os
import sys
import uuid
from pathlib import Path


def load_qa_config() -> dict:
    """Load qa section from config/org.yaml. Returns defaults if missing."""
    defaults = {
        "agentmail_inbox": "lumina.qa@agentmail.to",
    }
    config_path = Path("config/org.yaml")
    if not config_path.exists():
        return defaults
    try:
        import yaml
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        qa = raw.get("qa", {})
        contact = raw.get("contact", {})
        return {
            "agentmail_inbox": qa.get("agentmail_inbox", defaults["agentmail_inbox"]),
            "resend_from": contact.get("resend_from", "info@mail.example.org"),
        }
    except Exception:
        return defaults


def main() -> None:
    parser = argparse.ArgumentParser(description="Send test email via Resend to QA inbox")
    parser.add_argument("--subject", required=True, help="Expected subject line (without E2E prefix)")
    parser.add_argument("--html-file", required=True, help="Path to rendered HTML email file")
    parser.add_argument("--from-address", default=None, help="From address (reads from config if not set)")
    parser.add_argument("--to-inbox", default=None, help="QA inbox address (reads from config if not set)")
    args = parser.parse_args()

    resend_api_key = os.environ.get("RESEND_API_KEY")
    if not resend_api_key:
        print(json.dumps({"error": "RESEND_API_KEY not set"}), file=sys.stderr)
        sys.exit(2)

    html_path = Path(args.html_file)
    if not html_path.exists():
        print(json.dumps({"error": f"HTML file not found: {args.html_file}"}), file=sys.stderr)
        sys.exit(2)

    config = load_qa_config()
    to_inbox = args.to_inbox or config["agentmail_inbox"]
    from_address = args.from_address or config.get("resend_from", "info@mail.example.org")

    test_email_id = f"E2E-{uuid.uuid4()}"
    subject_with_id = f"[{test_email_id}] {args.subject}"
    html_content = html_path.read_text(encoding="utf-8")

    try:
        import httpx
    except ImportError:
        print(json.dumps({"error": "httpx not installed. Run: pip install httpx"}), file=sys.stderr)
        sys.exit(2)

    # Strip HTML tags to produce a plain-text fallback (improves deliverability
    # and spam filter pass-through when sending to inboxes with strict HTML policies)
    try:
        from bs4 import BeautifulSoup
        text_content = BeautifulSoup(html_content, "html.parser").get_text(separator="\n").strip()
    except ImportError:
        import re
        text_content = re.sub(r"<[^>]+>", " ", html_content).strip()

    try:
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": from_address,
                "to": [to_inbox],
                "subject": subject_with_id,
                "html": html_content,
                "text": text_content,
            },
            timeout=15.0,
        )
    except httpx.ConnectError as exc:
        print(json.dumps({"error": f"Cannot reach Resend API: {exc}"}), file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(json.dumps({"error": f"Resend API error: {exc}"}), file=sys.stderr)
        sys.exit(2)

    if resp.status_code >= 400:
        print(json.dumps({"error": f"Resend {resp.status_code}: {resp.text[:200]}"}), file=sys.stderr)
        sys.exit(2)

    message_id = resp.json().get("id")
    if not message_id:
        print(json.dumps({"error": f"Resend returned no message ID: {resp.text[:200]}"}), file=sys.stderr)
        sys.exit(2)

    print(json.dumps({"message_id": message_id, "test_email_id": test_email_id}))


if __name__ == "__main__":
    main()
