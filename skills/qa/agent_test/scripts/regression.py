from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
from typing import Any

import yaml


REPORT_DIR = Path(__file__).resolve().parents[4] / "memory" / "logs" / "qa"

_FAIL_STATUSES = {"FAIL", "ERROR"}
_IGNORED_ASSERTION_FIELDS = {
    "detail",
    "elapsed",
    "name",
    "score",
    "status",
    "threshold",
}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "scenario"


def _load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a top-level mapping")
    return _json_safe_value(loaded)


def _json_safe_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe_value(item) for item in value]
    if isinstance(value, (datetime,)):
        return value.isoformat()
    if hasattr(value, "isoformat") and not isinstance(value, (str, bytes)):
        try:
            return value.isoformat()
        except TypeError:
            return value
    return value


def _sorted_reports(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        reports,
        key=lambda report: (
            str(report.get("workflow") or ""),
            str(report.get("scenario") or ""),
            int(report.get("run") or 0),
        ),
    )


def _load_report_set(source: str | Path) -> dict[str, Any]:
    path = Path(source)
    if not path.exists():
        raise FileNotFoundError(f"Report source does not exist: {path}")

    if path.is_dir():
        reports = [_load_yaml(report_path) for report_path in sorted(path.glob("*.yaml"))]
        return {"metadata": {"source": str(path.resolve())}, "reports": _sorted_reports(reports)}

    payload = _load_yaml(path)
    reports = payload.get("reports")
    if isinstance(reports, list):
        normalized = [item for item in reports if isinstance(item, dict)]
        return {
            "metadata": payload.get("metadata", {}) if isinstance(payload.get("metadata"), dict) else {},
            "reports": _sorted_reports(normalized),
        }
    return {"metadata": {"source": str(path.resolve())}, "reports": [payload]}


def _report_key(report: dict[str, Any]) -> tuple[str, str]:
    return (str(report.get("workflow") or "unknown"), str(report.get("scenario") or "unknown"))


def _report_failed(report: dict[str, Any]) -> bool:
    status = str(report.get("status") or "").upper()
    return status in _FAIL_STATUSES or bool(report.get("infrastructure_failure"))


def _assertion_index(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for assertion in report.get("assertions", []) or []:
        if not isinstance(assertion, dict):
            continue
        name = str(assertion.get("name") or assertion.get("type") or "")
        if name:
            index[name] = assertion
    return index


def _failing_assertions(report: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for assertion in report.get("assertions", []) or []:
        if not isinstance(assertion, dict):
            continue
        if str(assertion.get("status") or "").upper() in _FAIL_STATUSES:
            names.append(str(assertion.get("name") or assertion.get("type") or "unknown"))
    return names


def create_baseline_snapshot(
    *,
    report_source: str | Path,
    output_path: str | Path,
    date: str | None = None,
    gateway_version: str | None = None,
    model_versions: dict[str, str] | None = None,
) -> dict[str, Any]:
    loaded = _load_report_set(report_source)
    snapshot = {
        "metadata": {
            "date": date or _today(),
            "gateway_version": gateway_version or "unknown",
            "model_versions": model_versions or {},
        },
        "reports": _sorted_reports(loaded["reports"]),
    }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(snapshot, sort_keys=False), encoding="utf-8")
    return snapshot


def compare_report_sets(baseline_source: str | Path, current_source: str | Path) -> dict[str, Any]:
    baseline = _load_report_set(baseline_source)
    current = _load_report_set(current_source)

    baseline_index = {_report_key(report): report for report in baseline["reports"]}
    current_index = {_report_key(report): report for report in current["reports"]}

    new_failures: list[dict[str, Any]] = []
    resolved_failures: list[dict[str, Any]] = []
    changed_semantic_scores: list[dict[str, Any]] = []

    for key in sorted(set(baseline_index) | set(current_index)):
        baseline_report = baseline_index.get(key)
        current_report = current_index.get(key)

        if current_report and _report_failed(current_report) and not (
            baseline_report and _report_failed(baseline_report)
        ):
            new_failures.append(
                {
                    "workflow": key[0],
                    "scenario": key[1],
                    "baseline_status": baseline_report.get("status") if baseline_report else None,
                    "current_status": current_report.get("status"),
                    "failing_assertions": _failing_assertions(current_report),
                }
            )

        if baseline_report and _report_failed(baseline_report) and current_report and not _report_failed(current_report):
            resolved_failures.append(
                {
                    "workflow": key[0],
                    "scenario": key[1],
                    "baseline_status": baseline_report.get("status"),
                    "current_status": current_report.get("status"),
                    "resolved_assertions": _failing_assertions(baseline_report),
                }
            )

        if not baseline_report or not current_report:
            continue

        baseline_assertions = _assertion_index(baseline_report)
        current_assertions = _assertion_index(current_report)
        for assertion_name in sorted(set(baseline_assertions) & set(current_assertions)):
            baseline_assertion = baseline_assertions[assertion_name]
            current_assertion = current_assertions[assertion_name]
            baseline_score = baseline_assertion.get("score")
            current_score = current_assertion.get("score")
            if not isinstance(baseline_score, (int, float)) or not isinstance(current_score, (int, float)):
                continue
            if float(baseline_score) == float(current_score):
                continue
            changed_semantic_scores.append(
                {
                    "workflow": key[0],
                    "scenario": key[1],
                    "assertion": assertion_name,
                    "baseline_score": float(baseline_score),
                    "current_score": float(current_score),
                    "delta": round(float(current_score) - float(baseline_score), 4),
                    "baseline_threshold": baseline_assertion.get("threshold"),
                    "current_threshold": current_assertion.get("threshold"),
                }
            )

    changed_semantic_scores.sort(
        key=lambda item: (-abs(float(item["delta"])), item["workflow"], item["scenario"], item["assertion"])
    )

    return {
        "status": "FAIL" if new_failures else "PASS",
        "baseline": {
            "report_count": len(baseline["reports"]),
            "metadata": baseline.get("metadata", {}),
        },
        "current": {
            "report_count": len(current["reports"]),
            "metadata": current.get("metadata", {}),
        },
        "summary": {
            "new_failures": len(new_failures),
            "resolved_failures": len(resolved_failures),
            "changed_semantic_scores": len(changed_semantic_scores),
        },
        "new_failures": new_failures,
        "resolved_failures": resolved_failures,
        "changed_semantic_scores": changed_semantic_scores,
    }


def _normalize_path_for_scenario(path_value: str, *, repo_root: Path, failure_date: str) -> str:
    normalized = path_value
    try:
        relative = Path(path_value).resolve().relative_to(repo_root.resolve())
        normalized = "{{repo_root}}/" + relative.as_posix()
    except Exception:
        normalized = path_value
    return normalized.replace(failure_date, "{{today}}")


def _copy_failure_artifacts(
    failing_assertions: list[dict[str, Any]],
    *,
    repo_root: Path,
    workflow: str,
    scenario: str,
    failure_date: str,
) -> list[str]:
    copied: list[str] = []
    fixture_dir = repo_root / "tests" / "fixtures" / "regressions"
    fixture_dir.mkdir(parents=True, exist_ok=True)
    seen_sources: set[Path] = set()

    for assertion in failing_assertions:
        raw_path = assertion.get("path")
        if not isinstance(raw_path, str):
            continue
        source = Path(raw_path)
        if not source.exists():
            continue
        resolved = source.resolve()
        if resolved in seen_sources:
            continue
        seen_sources.add(resolved)
        destination = fixture_dir / (
            f"{failure_date}-{_slug(workflow)}-{_slug(scenario)}-{source.name}"
        )
        shutil.copy2(resolved, destination)
        copied.append(str(destination.relative_to(repo_root)))

    return copied


def _supported_assertion(assertion: dict[str, Any]) -> dict[str, Any]:
    assertion_type = str(assertion.get("type") or assertion.get("name") or "").strip()
    if not assertion_type:
        raise ValueError("Failing assertion is missing a type/name")

    scenario_assertion: dict[str, Any] = {"type": assertion_type}
    for key, value in assertion.items():
        if key in _IGNORED_ASSERTION_FIELDS or key == "type":
            continue
        scenario_assertion[key] = value
    return scenario_assertion


def _find_target_scenarios_file(repo_root: Path, workflow: str) -> Path:
    candidates = sorted(repo_root.glob("skills/**/tests/scenarios.yaml")) + sorted(
        repo_root.glob("agents/**/tests/scenarios.yaml")
    )
    matches: list[Path] = []
    for path in candidates:
        contract = _load_yaml(path)
        target = contract.get("target", {})
        if isinstance(target, dict):
            target_path = str(target.get("path") or "")
            if Path(target_path).name == workflow:
                matches.append(path)
                continue
        if path.parents[1].name == workflow:
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"Could not locate scenarios.yaml for workflow {workflow}")
    if len(matches) > 1:
        raise ValueError(f"Multiple scenario files matched workflow {workflow}: {matches}")
    return matches[0]


def _unique_scenario_name(existing: list[dict[str, Any]], base_name: str) -> str:
    existing_names = {
        str(item.get("name"))
        for item in existing
        if isinstance(item, dict) and item.get("name")
    }
    if base_name not in existing_names:
        return base_name

    suffix = 2
    while f"{base_name}-{suffix}" in existing_names:
        suffix += 1
    return f"{base_name}-{suffix}"


def convert_failure_report(report_path: str | Path, *, repo_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else _repo_root()
    report = _load_yaml(Path(report_path))
    if not _report_failed(report):
        raise ValueError(f"{report_path} does not describe a failing report")

    workflow = str(report.get("workflow") or "unknown")
    scenario = str(report.get("scenario") or "scenario")
    completed_at = str(report.get("completed_at") or "")
    failure_date = completed_at[:10] if len(completed_at) >= 10 else _today()

    failing_assertions = [
        assertion
        for assertion in report.get("assertions", []) or []
        if isinstance(assertion, dict) and str(assertion.get("status") or "").upper() in _FAIL_STATUSES
    ]
    if not failing_assertions:
        raise ValueError(f"{report_path} does not contain any failing assertions")

    copied_fixtures = _copy_failure_artifacts(
        failing_assertions,
        repo_root=root,
        workflow=workflow,
        scenario=scenario,
        failure_date=failure_date,
    )

    scenario_assertions: list[dict[str, Any]] = []
    for assertion in failing_assertions:
        generated = _supported_assertion(assertion)
        raw_path = generated.get("path")
        if isinstance(raw_path, str):
            generated["path"] = _normalize_path_for_scenario(
                raw_path,
                repo_root=root,
                failure_date=failure_date,
            )
        scenario_assertions.append(generated)

    scenarios_path = _find_target_scenarios_file(root, workflow)
    contract = _load_yaml(scenarios_path)
    scenarios = contract.get("scenarios", [])
    if not isinstance(scenarios, list):
        raise ValueError(f"{scenarios_path} is missing a scenarios list")

    base_name = f"regression-{failure_date}-{_slug(scenario)}"
    scenario_name = _unique_scenario_name(scenarios, base_name)
    when_block = report.get("when")
    if not isinstance(when_block, dict):
        when_block = {
            "invoke": report.get("trigger") or "",
            "params": {},
        }

    scenarios.append(
        {
            "name": scenario_name,
            "tags": ["regression", failure_date],
            "when": when_block,
            "then": scenario_assertions,
        }
    )
    contract["scenarios"] = scenarios
    scenarios_path.write_text(yaml.safe_dump(contract, sort_keys=False), encoding="utf-8")

    return {
        "scenario_file": str(scenarios_path.relative_to(root)),
        "scenario_name": scenario_name,
        "copied_fixtures": copied_fixtures,
        "failure_date": failure_date,
    }


def _parse_model_versions(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"Model version must be key=value: {value}")
        key, version = value.split("=", 1)
        key = key.strip()
        version = version.strip()
        if not key or not version:
            raise ValueError(f"Model version must be key=value: {value}")
        parsed[key] = version
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture baselines, diff QA reports, and convert failures to regressions.")
    parser.add_argument("--baseline", help="Baseline report snapshot or directory")
    parser.add_argument("--current", help="Current report snapshot or directory")
    parser.add_argument("--snapshot", help="Write a baseline snapshot to this path")
    parser.add_argument(
        "--report-source",
        default=str(REPORT_DIR),
        help="Directory or snapshot used when creating a baseline snapshot",
    )
    parser.add_argument("--date", help="Baseline date metadata (YYYY-MM-DD)")
    parser.add_argument("--gateway-version", help="Gateway version metadata for snapshots")
    parser.add_argument(
        "--model-version",
        action="append",
        default=[],
        help="Model version metadata in key=value form; repeatable",
    )
    parser.add_argument("--convert", help="Failure report to convert into a regression scenario")
    parser.add_argument(
        "--repo-root",
        default=str(_repo_root()),
        help="Override repository root for failure conversion",
    )
    args = parser.parse_args(argv)

    if args.snapshot:
        snapshot = create_baseline_snapshot(
            report_source=args.report_source,
            output_path=args.snapshot,
            date=args.date,
            gateway_version=args.gateway_version,
            model_versions=_parse_model_versions(args.model_version),
        )
        print(json.dumps(snapshot, indent=2, sort_keys=True))
        return 0

    if args.convert:
        conversion = convert_failure_report(args.convert, repo_root=args.repo_root)
        print(json.dumps(conversion, indent=2, sort_keys=True))
        return 0

    if not args.baseline or not args.current:
        parser.error("Either --snapshot, --convert, or both --baseline and --current are required")

    diff = compare_report_sets(args.baseline, args.current)
    print(json.dumps(diff, indent=2, sort_keys=True))
    return 1 if diff["summary"]["new_failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
