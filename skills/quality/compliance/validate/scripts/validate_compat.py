from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from clawspec.models import ValidationReport


def resolve_target_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_dir():
        skill_path = candidate / "SKILL.md"
        agent_path = candidate / "SOUL.md"
        if skill_path.exists():
            return skill_path
        if agent_path.exists():
            return agent_path
        raise FileNotFoundError(f"No SKILL.md or SOUL.md found in {candidate}")
    return candidate


def to_legacy_report(report: ValidationReport) -> dict[str, Any]:
    checks = [
        {
            "name": check.name,
            "status": check.status.upper(),
            "detail": check.detail,
        }
        for check in report.checks
    ]
    errors = sum(1 for check in checks if check["status"] == "FAIL")
    warnings = sum(1 for check in checks if check["status"] == "WARN")
    info = sum(1 for check in checks if check["status"] == "INFO")
    status = "FAIL" if errors else "WARN" if warnings else "PASS"
    return {
        "target": report.target,
        "target_type": report.target_type,
        "status": status,
        "checks": checks,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "info": info,
        },
    }


def emit_report(report: dict[str, Any], *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print(yaml.safe_dump(report, sort_keys=False))


def exit_code_for(report: dict[str, Any]) -> int:
    return 1 if report["status"] == "FAIL" else 0
