from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

import yaml


REPORT_DIR = Path(__file__).resolve().parents[4] / "memory" / "logs" / "qa"


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _load_report(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a report mapping")
    return loaded


def _increment(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


def _report_status(report: dict[str, Any]) -> str:
    status = str(report.get("status", "")).casefold()
    if status in {"pass", "warn", "fail", "error"}:
        return status
    return "error"


def summarize_reports(*, report_dir: Path | None = None, date: str | None = None) -> dict[str, Any]:
    selected_date = date or _today()
    active_report_dir = report_dir or REPORT_DIR
    files = (
        sorted(active_report_dir.glob(f"{selected_date}-*.yaml"))
        if active_report_dir.exists()
        else []
    )

    summary = {
        "date": selected_date,
        "report_count": 0,
        "reports": {"pass": 0, "warn": 0, "fail": 0, "error": 0, "infrastructure": 0},
        "assertions": {"pass": 0, "warn": 0, "fail": 0, "skip": 0, "error": 0},
        "workflows": {},
        "report_files": [str(path) for path in files],
    }
    workflows: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "reports": {"pass": 0, "warn": 0, "fail": 0, "error": 0, "infrastructure": 0},
            "assertions": {"pass": 0, "warn": 0, "fail": 0, "skip": 0, "error": 0},
            "scenarios": [],
        }
    )

    for path in files:
        report = _load_report(path)
        workflow = str(report.get("workflow") or "unknown")
        status = _report_status(report)
        _increment(summary["reports"], status)
        _increment(workflows[workflow]["reports"], status)
        if report.get("infrastructure_failure"):
            _increment(summary["reports"], "infrastructure")
            _increment(workflows[workflow]["reports"], "infrastructure")
        summary["report_count"] += 1

        workflow_entry = workflows[workflow]
        workflow_entry["scenarios"].append(
            {
                "scenario": report.get("scenario"),
                "status": report.get("status"),
                "run": report.get("run"),
                "report_path": str(path),
            }
        )

        for assertion in report.get("assertions", []) or []:
            if not isinstance(assertion, dict):
                continue
            status = str(assertion.get("status", "error")).casefold()
            if status not in workflow_entry["assertions"]:
                status = "error"
            _increment(summary["assertions"], status)
            _increment(workflow_entry["assertions"], status)

    summary["workflows"] = dict(sorted(workflows.items()))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize QA reports by day and workflow.")
    parser.add_argument("--date", help="Report date in YYYY-MM-DD format; defaults to today")
    args = parser.parse_args(argv)

    payload = summarize_reports(date=args.date)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
