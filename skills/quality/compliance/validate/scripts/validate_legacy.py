from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Callable

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa.validate.scripts.checks.agent_checks import run_agent_checks
    from skills.qa.validate.scripts.checks.skill_checks import run_skill_checks
else:
    from .checks.agent_checks import run_agent_checks
    from .checks.skill_checks import run_skill_checks


CheckRunner = Callable[[str | Path], list[dict[str, str | None]]]


def _detect_target_type(path: Path) -> tuple[str, CheckRunner]:
    if path.name == "SKILL.md":
        return "skill", run_skill_checks
    if path.name == "SOUL.md":
        return "agent", run_agent_checks
    raise ValueError("Target must be a SKILL.md or SOUL.md file")


def validate_target(path: str | Path) -> dict[str, object]:
    target_path = Path(path)
    target_type, runner = _detect_target_type(target_path)
    checks = runner(target_path)
    errors = sum(1 for check in checks if check["status"] == "FAIL")
    warnings = sum(1 for check in checks if check["status"] == "WARN")
    info = sum(1 for check in checks if check["status"] == "INFO")
    status = "FAIL" if errors else "WARN" if warnings else "PASS"
    return {
        "target": str(target_path),
        "target_type": target_type,
        "status": status,
        "checks": checks,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "info": info,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md or SOUL.md structure.")
    parser.add_argument("target_positional", nargs="?", help="Path to SKILL.md or SOUL.md")
    parser.add_argument("--target", dest="target_flag", help="Path to SKILL.md or SOUL.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of YAML")
    args = parser.parse_args(argv)

    target = args.target_flag or args.target_positional
    if not target:
        parser.error("a target path is required")

    report = validate_target(target)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(yaml.safe_dump(report, sort_keys=False))
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
