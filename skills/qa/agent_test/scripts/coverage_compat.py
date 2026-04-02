from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from clawspec.coverage.ledger import load_ledger, resolve_repo_root
from clawspec.coverage.reporter import (
    build_summary as clawspec_build_summary,
    find_contract_gaps as clawspec_find_contract_gaps,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


DEFAULT_LEDGER_PATH = _repo_root() / "docs" / "testing" / "coverage-ledger.yaml"


def _shape_legacy_summary(payload: dict[str, Any]) -> dict[str, Any]:
    shaped = dict(payload)
    shaped.pop("missing_targets", None)
    for wave_payload in shaped.get("waves", {}).values():
        if isinstance(wave_payload, dict):
            wave_payload.pop("missing_targets", None)
    return shaped


def find_contract_gaps(entry: dict[str, Any], *, repo_root: Path | None = None) -> dict[str, Any]:
    gaps = dict(clawspec_find_contract_gaps(entry, repo_root=repo_root))
    gaps.pop("missing_targets", None)
    return gaps


def build_summary(
    ledger_path: str | Path,
    report_root: str | Path,
    date: str | None = None,
    wave: str | None = None,
) -> dict[str, Any]:
    payload = clawspec_build_summary(
        ledger_path=ledger_path,
        report_root=report_root,
        date=date,
        wave=wave,
    )
    return _shape_legacy_summary(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Summarize Marketing Wave coverage from the coverage ledger."
    )
    parser.add_argument(
        "--ledger",
        default=str(DEFAULT_LEDGER_PATH),
        help="Path to docs/testing/coverage-ledger.yaml",
    )
    parser.add_argument("--wave", help="Filter to a specific wave id")
    parser.add_argument("--date", help="Optional report date in YYYY-MM-DD format")
    parser.add_argument(
        "--report-root", help="Override the QA report directory used for recent report counts"
    )
    parser.add_argument(
        "--write-json", action="store_true", help="Write the summary to coverage-summary.json"
    )
    args = parser.parse_args(argv)

    active_report_root = (
        Path(args.report_root)
        if args.report_root
        else resolve_repo_root(args.ledger) / "memory" / "logs" / "qa"
    )

    try:
        payload = build_summary(
            ledger_path=args.ledger,
            report_root=active_report_root,
            date=args.date,
            wave=args.wave,
        )
    except KeyError:
        print(json.dumps({"status": "ERROR", "detail": f"Wave not found: {args.wave}"}, indent=2))
        return 2
    except Exception as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}, indent=2))
        return 2

    if args.write_json:
        output_path = active_report_root / "coverage-summary.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0
