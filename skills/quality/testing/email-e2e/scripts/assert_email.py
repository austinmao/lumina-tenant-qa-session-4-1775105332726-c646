#!/usr/bin/env python3
"""
assert_email.py — Run 6 assertion checks on a received email.

Checks: delivery (handled upstream), subject_match, body_nonempty, links_health,
unsubscribe, brand_kill_list.

Usage:
    python3 assert_email.py \\
        --expected-subject "Your Retreat Awaits" \\
        --received-html "<html>...</html>" \\
        --received-subject "[E2E-abc123] Your Retreat Awaits" \\
        [--kill-list-file /path/to/kill-list.txt]

Output: YAML to stdout with overall status and per-check results.
Exit 0 (all PASS), 1 (any FAIL), 2 (script error).
"""

import argparse
import re
import sys
from typing import Optional


def yaml_output(data: dict) -> str:
    """Simple YAML serializer (avoids yaml import requirement for pure-logic script)."""
    try:
        import yaml
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    except ImportError:
        # Fallback: minimal hand-rolled YAML
        lines = []
        for k, v in data.items():
            if isinstance(v, list):
                lines.append(f"{k}:")
                for item in v:
                    lines.append("  - " + "\n    ".join(
                        f"{ik}: {format_val(iv)}" for ik, iv in item.items()
                    ))
            else:
                lines.append(f"{k}: {format_val(v)}")
        return "\n".join(lines) + "\n"


def format_val(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return str(v).lower()
    return repr(v) if isinstance(v, str) and any(c in v for c in ":[]{},\n") else str(v)


def check_subject_match(expected: str, received: str) -> dict:
    """Received subject should contain expected (after stripping E2E prefix)."""
    # Strip [E2E-<uuid>] prefix from received subject
    stripped = re.sub(r"^\[E2E-[0-9a-f-]+\]\s*", "", received, flags=re.IGNORECASE).strip()
    if stripped == expected.strip():
        return {"name": "subject_match", "status": "PASS", "detail": None, "failure_class": None}
    return {
        "name": "subject_match",
        "status": "FAIL",
        "detail": f"Expected: '{expected.strip()}' | Got: '{stripped}'",
        "failure_class": "content",
    }


def check_body_nonempty(html: str) -> dict:
    if html and len(html.strip()) > 0:
        return {"name": "body_nonempty", "status": "PASS", "detail": None, "failure_class": None}
    return {
        "name": "body_nonempty",
        "status": "FAIL",
        "detail": "HTML body is empty",
        "failure_class": "content",
    }


def check_links_health(html: str) -> dict:
    """HEAD request all href links (excluding mailto: and # anchors). Must return 2xx or 3xx."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {
            "name": "links_health",
            "status": "SKIP",
            "detail": "requests or beautifulsoup4 not installed",
            "failure_class": None,
        }

    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("mailto:") or href.startswith("#") or not href.startswith("http"):
            continue
        links.append(href)

    if not links:
        return {"name": "links_health", "status": "PASS", "detail": "No external links to check", "failure_class": None}

    failed = []
    for url in links:
        try:
            resp = requests.head(url, allow_redirects=True, timeout=10)
            if resp.status_code >= 400:
                failed.append(f"{url} ({resp.status_code})")
        except requests.RequestException as exc:
            failed.append(f"{url} (error: {exc})")

    if not failed:
        return {"name": "links_health", "status": "PASS", "detail": f"All {len(links)} links OK", "failure_class": None}
    return {
        "name": "links_health",
        "status": "FAIL",
        "detail": f"{len(failed)} links failed: {', '.join(failed)}",
        "failure_class": "engineering",
    }


def check_unsubscribe(html: str) -> dict:
    """Unsubscribe link must be present and resolve."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {
            "name": "unsubscribe",
            "status": "SKIP",
            "detail": "requests or beautifulsoup4 not installed",
            "failure_class": None,
        }

    soup = BeautifulSoup(html, "html.parser")
    unsub_link = None
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        text = a.get_text().lower()
        if "unsubscribe" in href or "unsubscribe" in text:
            unsub_link = a["href"]
            break

    if not unsub_link:
        return {
            "name": "unsubscribe",
            "status": "FAIL",
            "detail": "No unsubscribe link found in HTML",
            "failure_class": "engineering",
        }

    try:
        resp = requests.head(unsub_link, allow_redirects=True, timeout=10)
        if resp.status_code < 400:
            return {"name": "unsubscribe", "status": "PASS", "detail": None, "failure_class": None}
        return {
            "name": "unsubscribe",
            "status": "FAIL",
            "detail": f"Unsubscribe link returned {resp.status_code}: {unsub_link}",
            "failure_class": "engineering",
        }
    except Exception as exc:
        return {
            "name": "unsubscribe",
            "status": "FAIL",
            "detail": f"Unsubscribe link error: {exc}",
            "failure_class": "engineering",
        }


def check_brand_kill_list(subject: str, html: str, kill_list_file: Optional[str]) -> dict:
    """Check subject and body for prohibited words from the brand kill-list."""
    kill_list = []

    if kill_list_file:
        try:
            from pathlib import Path
            lines = Path(kill_list_file).read_text(encoding="utf-8").splitlines()
            kill_list = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
        except Exception as exc:
            return {
                "name": "brand_kill_list",
                "status": "SKIP",
                "detail": f"Could not read kill-list file: {exc}",
                "failure_class": None,
            }
    else:
        # Default kill-list (sourced from newsletter gate sub-skill patterns)
        kill_list = [
            "sacred container",
            "sacred space",
            "plant medicine",
            "ayahuasca",
            "psychedelic",
            "psilocybin",
            "healing journey",
            "trauma healing",
        ]

    # Extract plain text from HTML for body check
    plain_text = html
    try:
        from bs4 import BeautifulSoup
        plain_text = BeautifulSoup(html, "html.parser").get_text(separator=" ")
    except ImportError:
        # Fallback: strip tags with regex
        plain_text = re.sub(r"<[^>]+>", " ", html)

    content_to_check = f"{subject} {plain_text}".lower()
    found = [word for word in kill_list if word.lower() in content_to_check]

    if not found:
        return {"name": "brand_kill_list", "status": "PASS", "detail": None, "failure_class": None}
    return {
        "name": "brand_kill_list",
        "status": "FAIL",
        "detail": f"Prohibited words found: {', '.join(found)}",
        "failure_class": "content",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run assertion suite on received email")
    parser.add_argument("--expected-subject", required=True)
    parser.add_argument("--received-html", required=True)
    parser.add_argument("--received-subject", required=True)
    parser.add_argument("--kill-list-file", default=None)
    args = parser.parse_args()

    checks = [
        check_subject_match(args.expected_subject, args.received_subject),
        check_body_nonempty(args.received_html),
        check_links_health(args.received_html),
        check_unsubscribe(args.received_html),
        check_brand_kill_list(args.received_subject, args.received_html, args.kill_list_file),
    ]

    any_fail = any(c["status"] == "FAIL" for c in checks)
    result = {
        "overall": "FAIL" if any_fail else "PASS",
        "checks": checks,
    }

    print(yaml_output(result))
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
