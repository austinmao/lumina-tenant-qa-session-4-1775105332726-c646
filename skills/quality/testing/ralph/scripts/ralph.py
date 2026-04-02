from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any

import httpx
import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa.agent_test.scripts import run_compat as run_module
    from skills.qa.evaluate.scripts.evaluate import evaluate_contract
else:
    from ...agent_test.scripts import run_compat as run_module
    from ...evaluate.scripts.evaluate import evaluate_contract


STATE_DIR = Path(__file__).resolve().parents[4] / "memory" / "logs" / "qa" / "ralph"
LAST_POLL = Path(__file__).resolve().parents[4] / "memory" / "logs" / "qa" / ".last-poll"
SLACK_API = "https://slack.com/api/chat.postMessage"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _today() -> str:
    return _utc_now().date().isoformat()


def _load_yaml(path: str | Path) -> dict[str, Any]:
    loaded = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a top-level mapping")
    return loaded


def _scenario_lookup(path: str | Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    contract = _load_yaml(path)
    mapping = {
        str(item.get("name")): item
        for item in contract.get("scenarios", [])
        if isinstance(item, dict) and item.get("name")
    }
    return contract, mapping


def _failed_assertions_signature(report: dict[str, Any]) -> set[tuple[str, str]]:
    signature: set[tuple[str, str]] = set()
    for assertion in report.get("assertions", []) or []:
        if not isinstance(assertion, dict) or assertion.get("status") != "FAIL":
            continue
        signature.add((str(assertion.get("name", "")), str(assertion.get("detail", ""))))
    return signature


def _write_state(
    *,
    workflow: str,
    scenario: str,
    report_paths: list[str],
    run_count: int,
    action: str,
    reason: str | None,
) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{workflow}-{scenario}.json"
    payload = {
        "workflow": workflow,
        "scenario": scenario,
        "run_count": run_count,
        "action": action,
        "reason": reason,
        "report_paths": report_paths,
        "updated_at": _utc_now().isoformat().replace("+00:00", "Z"),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _build_feedback_payload(report: dict[str, Any], *, run_number: int) -> dict[str, Any]:
    feedback = report.get("feedback") or {}
    return {
        "qa_feedback": feedback.get("for_orchestrator", ""),
        "qa_feedback_structured": feedback.get("structured", []),
        "qa_report_path": report.get("report_path"),
        "qa_run_number": run_number,
    }


def _reinvoke_with_feedback(
    *,
    entry: dict[str, Any],
    scenario: dict[str, Any],
    report: dict[str, Any],
    next_run_number: int,
    repo_root: Path,
    gateway_base: str,
    hooks_token: str | None,
) -> dict[str, Any]:
    enriched = json.loads(json.dumps(scenario))
    params = dict(enriched.get("when", {}).get("params", {}) or {})
    params.update(_build_feedback_payload(report, run_number=next_run_number - 1))
    params["test_mode"] = True
    enriched.setdefault("when", {})["params"] = params
    return run_module._trigger_scenario(
        entry,
        enriched,
        repo_root=repo_root,
        gateway_base=gateway_base,
        hooks_token=hooks_token,
    )


def _send_escalation(
    *,
    workflow: str,
    scenario: str,
    reason: str,
    report_paths: list[str],
    slack_channel: str,
    slack_token: str | None,
) -> dict[str, Any]:
    message = (
        f"QA escalation for {workflow}/{scenario}: {reason}. "
        f"Reports: {', '.join(report_paths) if report_paths else 'none'}"
    )
    if not slack_token:
        return {"ok": False, "message": message, "detail": "SLACK_BOT_TOKEN not configured"}

    response = httpx.post(
        SLACK_API,
        headers={
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={"channel": slack_channel, "text": message},
        timeout=15.0,
    )
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok", False):
        raise RuntimeError(payload.get("error", "Slack escalation failed"))
    return payload


def _candidate_patterns(repo_root: Path) -> list[str]:
    today = _today()
    return [
        str(repo_root / "memory" / "drafts" / f"{today}-*.md"),
        str(repo_root / "memory" / "drafts" / "copy" / f"{today}-*.md"),
        str(repo_root / "memory" / "drafts" / "webinars" / f"{today}-*.md"),
        str(repo_root / "memory" / "campaigns" / f"{today}-*.md"),
        str(repo_root / "memory" / "staging" / f"{today}-*.yaml"),
    ]


def _last_poll_time() -> float:
    if not LAST_POLL.exists():
        return 0.0
    return LAST_POLL.stat().st_mtime


def _touch_last_poll() -> None:
    LAST_POLL.parent.mkdir(parents=True, exist_ok=True)
    LAST_POLL.write_text(_utc_now().isoformat().replace("+00:00", "Z"), encoding="utf-8")


def _infer_scenario_file(output_path: Path, repo_root: Path) -> Path | None:
    relative = output_path.relative_to(repo_root) if output_path.is_absolute() else output_path
    parts = set(relative.parts)
    if "webinars" in parts:
        return repo_root / "skills" / "webinar-orchestrator" / "tests" / "scenarios.yaml"
    if "campaigns" in parts or "copy" in parts or "staging" in parts or "campaign" in output_path.name:
        return repo_root / "skills" / "campaign-workflow" / "tests" / "scenarios.yaml"
    return repo_root / "skills" / "newsletter" / "tests" / "scenarios.yaml"


def scan_outputs(*, repo_root: Path, patterns: list[str] | None = None) -> list[dict[str, str]]:
    cutoff = _last_poll_time()
    discovered: list[dict[str, str]] = []
    for pattern in patterns or _candidate_patterns(repo_root):
        for path in sorted(Path().glob(pattern) if not Path(pattern).is_absolute() else Path("/").glob(pattern.lstrip("/"))):
            if not path.is_file() or path.stat().st_mtime <= cutoff:
                continue
            scenario_file = _infer_scenario_file(path, repo_root)
            if scenario_file is None:
                continue
            discovered.append({"output_path": str(path), "scenario_file": str(scenario_file)})
    _touch_last_poll()
    return discovered


def run_candidate(
    *,
    scenario_file: str | Path,
    scenario_name: str | None = None,
    repo_root: Path | None = None,
    max_runs: int = 3,
    gateway_base: str = run_module.GATEWAY_BASE,
    hooks_token: str | None = None,
    slack_channel: str = "#lumina-bot",
    slack_token: str | None = None,
) -> dict[str, Any]:
    root = repo_root or _repo_root()
    contract, scenarios = _scenario_lookup(scenario_file)
    chosen_name = scenario_name or next(iter(scenarios.keys()))
    scenario = scenarios[chosen_name]
    entry = {
        "target_type": contract["target"]["type"],
        "target_path": contract["target"]["path"],
        "trigger": contract["target"].get("trigger"),
    }
    workflow = Path(entry["target_path"]).name

    report_paths: list[str] = []
    previous_signature: set[tuple[str, str]] | None = None
    resolved_reason: str | None = None
    action = "IDLE"

    for run_number in range(1, max_runs + 1):
        reports = evaluate_contract(
            scenario_file,
            run_number=run_number,
            scenario_name=chosen_name,
        )
        report = reports[0]
        report_paths.append(str(report.get("report_path")))

        status = report.get("status")
        if status in {"PASS", "WARN"} and not report.get("infrastructure_failure"):
            action = "PASSING"
            _write_state(
                workflow=workflow,
                scenario=chosen_name,
                report_paths=report_paths,
                run_count=run_number,
                action=action,
                reason=None,
            )
            return {
                "workflow": workflow,
                "scenario": chosen_name,
                "action": action,
                "reason": None,
                "run_count": run_number,
                "report_paths": report_paths,
            }

        if report.get("infrastructure_failure") or status == "ERROR":
            resolved_reason = "infrastructure"
            action = "ESCALATING"
            _send_escalation(
                workflow=workflow,
                scenario=chosen_name,
                reason=resolved_reason,
                report_paths=report_paths,
                slack_channel=slack_channel,
                slack_token=slack_token,
            )
            break

        if run_number >= max_runs:
            resolved_reason = "max-runs"
            action = "ESCALATING"
            _send_escalation(
                workflow=workflow,
                scenario=chosen_name,
                reason=resolved_reason,
                report_paths=report_paths,
                slack_channel=slack_channel,
                slack_token=slack_token,
            )
            break

        signature = _failed_assertions_signature(report)
        if previous_signature is not None and signature == previous_signature and signature:
            resolved_reason = "identical-failure"
            action = "ESCALATING"
            _send_escalation(
                workflow=workflow,
                scenario=chosen_name,
                reason=resolved_reason,
                report_paths=report_paths,
                slack_channel=slack_channel,
                slack_token=slack_token,
            )
            break

        _reinvoke_with_feedback(
            entry=entry,
            scenario=scenario,
            report=report,
            next_run_number=run_number + 1,
            repo_root=root,
            gateway_base=gateway_base,
            hooks_token=hooks_token,
        )
        previous_signature = signature
        action = "RE-INVOKING"

    _write_state(
        workflow=workflow,
        scenario=chosen_name,
        report_paths=report_paths,
        run_count=len(report_paths),
        action=action,
        reason=resolved_reason,
    )
    return {
        "workflow": workflow,
        "scenario": chosen_name,
        "action": action,
        "reason": resolved_reason,
        "run_count": len(report_paths),
        "report_paths": report_paths,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Ralph QA feedback loop.")
    parser.add_argument("--scenario-file")
    parser.add_argument("--scenario-name")
    parser.add_argument("--watch-path", action="append", default=[])
    parser.add_argument("--max-runs", type=int, default=3)
    parser.add_argument("--repo-root", default=str(_repo_root()))
    parser.add_argument("--gateway-base", default=run_module.GATEWAY_BASE)
    parser.add_argument("--hooks-token", default=run_module._hooks_token())
    parser.add_argument("--slack-channel", default="#lumina-bot")
    parser.add_argument("--slack-token", default=os.environ.get("SLACK_BOT_TOKEN"))
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    results: list[dict[str, Any]] = []
    if args.scenario_file:
        results.append(
            run_candidate(
                scenario_file=args.scenario_file,
                scenario_name=args.scenario_name,
                repo_root=repo_root,
                max_runs=args.max_runs,
                gateway_base=args.gateway_base,
                hooks_token=args.hooks_token,
                slack_channel=args.slack_channel,
                slack_token=args.slack_token,
            )
        )
    else:
        candidates = scan_outputs(repo_root=repo_root, patterns=args.watch_path or None)
        for candidate in candidates:
            scenario_file = candidate["scenario_file"]
            if not Path(scenario_file).exists():
                continue
            results.append(
                run_candidate(
                    scenario_file=scenario_file,
                    repo_root=repo_root,
                    max_runs=args.max_runs,
                    gateway_base=args.gateway_base,
                    hooks_token=args.hooks_token,
                    slack_channel=args.slack_channel,
                    slack_token=args.slack_token,
                )
            )

    print(json.dumps(results, indent=2, sort_keys=True))
    if any(item["action"] == "ESCALATING" for item in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
