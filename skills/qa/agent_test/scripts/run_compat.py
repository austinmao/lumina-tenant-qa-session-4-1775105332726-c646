from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec, seed_hooks_token
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec, seed_hooks_token

bootstrap_clawspec()

from clawspec.runner import run as runner


httpx = runner.httpx
subprocess = runner.subprocess
discover_scenarios = runner.discover_scenarios
evaluate_contract = runner.evaluate_contract
validate_target = runner.validate_target
validate_contract_file = runner.validate_contract_file
dispatch_assertion = runner.dispatch_assertion
_load_yaml = runner._load_yaml
_monitor_pipeline_stages = runner._monitor_pipeline_stages
_evaluate_pipeline_health = runner._evaluate_pipeline_health
_parse_json_payload = runner._parse_json_payload
_trigger_scenario = runner._trigger_scenario
_registered_agents = runner._registered_agents
_hooks_token = runner._hooks_token
_utc_now = runner._utc_now
GATEWAY_BASE = runner.GATEWAY_BASE


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _has_flag(args: list[str], flag: str) -> bool:
    return any(item == flag or item.startswith(f"{flag}=") for item in args)


def _with_defaults(argv: list[str] | None) -> list[str]:
    args = list(sys.argv[1:] if argv is None else argv)
    if not _has_flag(args, "--repo-root"):
        args.extend(["--repo-root", str(_repo_root())])
    return args


def _sync_runner_module() -> None:
    runner.httpx = httpx
    runner.subprocess = subprocess
    runner.discover_scenarios = discover_scenarios
    runner.evaluate_contract = evaluate_contract
    runner.validate_target = validate_target
    runner.validate_contract_file = validate_contract_file
    runner.dispatch_assertion = dispatch_assertion
    runner._load_yaml = _load_yaml
    runner._monitor_pipeline_stages = _monitor_pipeline_stages
    runner._evaluate_pipeline_health = _evaluate_pipeline_health
    runner._parse_json_payload = _parse_json_payload
    runner._trigger_scenario = _trigger_scenario
    runner._registered_agents = _registered_agents
    runner._hooks_token = _hooks_token
    runner._utc_now = _utc_now
    runner.GATEWAY_BASE = GATEWAY_BASE


def main(argv: list[str] | None = None) -> int:
    seed_hooks_token()
    _sync_runner_module()
    return runner.main(_with_defaults(argv))
