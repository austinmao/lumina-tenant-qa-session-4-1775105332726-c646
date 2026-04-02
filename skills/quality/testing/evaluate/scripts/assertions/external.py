from __future__ import annotations

import time
from typing import Any

from .common import elapsed, load_text, outcome


def slack_message_sent(assertion: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    start = time.perf_counter()
    log_path = assertion.get("log_path")
    path, text = load_text(log_path)
    if path is None or text is None:
        return outcome("slack_message_sent", "SKIP", "Slack log unavailable", elapsed=elapsed(start))
    if assertion["channel"] in text and assertion.get("contains", "") in text:
        return outcome("slack_message_sent", "PASS", None, elapsed=elapsed(start))
    return outcome("slack_message_sent", "FAIL", "Matching Slack message not found", elapsed=elapsed(start))


def email_received(assertion: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    start = time.perf_counter()
    log_path = assertion.get("log_path")
    path, text = load_text(log_path)
    if path is None or text is None:
        return outcome("email_received", "SKIP", "Email log unavailable", elapsed=elapsed(start))
    if assertion["to"] in text and assertion.get("subject_contains", "") in text:
        return outcome("email_received", "PASS", None, elapsed=elapsed(start))
    return outcome("email_received", "FAIL", "Matching email evidence not found", elapsed=elapsed(start))


HANDLERS = {
    "slack_message_sent": slack_message_sent,
    "email_received": email_received,
}
