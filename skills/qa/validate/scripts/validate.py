from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec
    from skills.qa.validate.scripts.validate_compat import (
        emit_report,
        exit_code_for,
        resolve_target_path,
        to_legacy_report,
    )
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec
    from .validate_compat import (
        emit_report,
        exit_code_for,
        resolve_target_path,
        to_legacy_report,
    )

bootstrap_clawspec()

from clawspec.api import validate as clawspec_validate


def validate_target(path: str | Path) -> dict[str, object]:
    target_path = resolve_target_path(path)
    return to_legacy_report(clawspec_validate(target_path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md or SOUL.md structure.")
    parser.add_argument("target_positional", nargs="?", help="Path to SKILL.md or SOUL.md")
    parser.add_argument("--target", dest="target_flag", help="Path to SKILL.md or SOUL.md")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of YAML")
    parser.add_argument("--verbose", action="store_true", help="Accepted for compatibility.")
    args = parser.parse_args(argv)

    target = args.target_flag or args.target_positional
    if not target:
        parser.error("a target path is required")

    report = validate_target(target)
    emit_report(report, as_json=args.json)
    return exit_code_for(report)


if __name__ == "__main__":
    raise SystemExit(main())
