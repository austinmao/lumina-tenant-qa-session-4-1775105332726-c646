from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec

bootstrap_clawspec()

from clawspec.runner import evaluate as clawspec_evaluate
from clawspec.schema_validator import validate_contract_file


REPORT_DIR = Path(__file__).resolve().parents[4] / "memory" / "logs" / "qa"
_utc_now = clawspec_evaluate._utc_now


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _sync_evaluate_module() -> None:
    clawspec_evaluate._utc_now = _utc_now


def evaluate_contract(
    contract_path: str | Path,
    *,
    run_number: int = 1,
    scenario_name: str | None = None,
    extra_context: dict[str, object] | None = None,
) -> list[dict[str, object]]:
    _sync_evaluate_module()
    return clawspec_evaluate.evaluate_contract(
        contract_path,
        run_number=run_number,
        scenario_name=scenario_name,
        extra_context=extra_context,
        report_dir=REPORT_DIR,
        repo_root=_repo_root(),
    )


def main(argv: list[str] | None = None) -> int:
    _sync_evaluate_module()
    parser = argparse.ArgumentParser(description="Evaluate QA contracts against existing artifacts.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scenario-file")
    group.add_argument("--handoff")
    group.add_argument("--pipeline")
    parser.add_argument("--scenario-name")
    parser.add_argument("--run-number", type=int, default=1)
    parser.add_argument(
        "--evaluate-only",
        action="store_true",
        help="Accepted for CLI compatibility; evaluation mode is the default behavior.",
    )
    args = parser.parse_args(argv)

    contract_path = args.scenario_file or args.handoff or args.pipeline
    validation = validate_contract_file(contract_path)
    if not validation.valid:
        print(yaml.safe_dump(validation.to_dict(), sort_keys=False))
        return 3

    try:
        reports = evaluate_contract(
            contract_path,
            run_number=args.run_number,
            scenario_name=args.scenario_name,
        )
    except Exception as exc:
        print(
            yaml.safe_dump(
                {"status": "ERROR", "detail": str(exc), "contract_path": contract_path},
                sort_keys=False,
            )
        )
        return 2

    print(yaml.safe_dump(reports, sort_keys=False))
    statuses = [str(report["status"]) for report in reports]
    if any(status == "FAIL" for status in statuses):
        return 1
    if any(status == "ERROR" for status in statuses):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
