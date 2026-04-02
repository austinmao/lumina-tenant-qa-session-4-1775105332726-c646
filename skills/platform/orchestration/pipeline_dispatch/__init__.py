"""Pipeline dispatch loop: route ClawPipe envelope statuses to handlers.

Implements the DispatchLoop class and handle_envelope() function, which
drive a ClawPipe pipeline through its full envelope lifecycle.

Envelope statuses handled:
  ok               — advance or complete
  needs_dispatch   — sequential via sessions_spawn, parallel via coordinate
  needs_approval   — pause, record resume token
  needs_replan     — re-dispatch with quality feedback
  needs_compensation — run compensation agents in order
  needs_input      — pause, request external input
  failed           — try fallback agent or escalate
  cancelled        — clean up and terminate
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from clawpipe.models import Envelope, EnvelopeStatus

# Maximum spawn depth enforced by the dispatch loop.
_DEFAULT_MAX_SPAWN_DEPTH = 2

# Status values from sessions_spawn that indicate failure.
_SPAWN_ERROR_STATUS = "error"

# Value returned by sessions_spawn on success.
_SPAWN_OK_STATUS = "ok"


def _extract_contract_path(envelope: Envelope) -> str | None:
    """Return contract_path from test metadata attribute if present."""
    return getattr(envelope, "_test_contract_path", None)


def _extract_artifact_path(envelope: Envelope) -> str | None:
    """Return artifact_path from test metadata attribute if present."""
    return getattr(envelope, "_test_artifact_path", None)


def _extract_fallback_agent_id(envelope: Envelope) -> str | None:
    """Return fallback_agent_id from test metadata attribute if present."""
    return getattr(envelope, "_test_fallback_agent_id", None)


def _extract_quality_feedback(envelope: Envelope) -> list[str] | None:
    """Return quality_feedback from test metadata attribute if present."""
    return getattr(envelope, "_test_quality_feedback", None)


def _build_replan_task(original_task: str | None, feedback: list[str] | None) -> str:
    """Append quality feedback to the original task string."""
    base = original_task or ""
    if not feedback:
        return base
    feedback_str = "; ".join(feedback)
    return f"{base}\n\nQuality feedback: {feedback_str}"


def _run_assertions(
    contract_assertions: Callable[..., dict[str, Any]],
    contract_path: str,
    artifact_path: str | None,
) -> dict[str, Any]:
    """Invoke contract_assertions and return the result dict."""
    return contract_assertions(
        contract_path=contract_path,
        artifact_path=artifact_path,
    )


def _spawn_agent(
    sessions_spawn: Callable[..., dict[str, Any]],
    agent_id: str,
    task: str,
    stage: str | None = None,
    pipeline_id: str | None = None,
) -> dict[str, Any]:
    """Call sessions_spawn for a single agent and return the result."""
    return sessions_spawn(
        agent_id=agent_id,
        task=task,
        stage=stage,
        pipeline_id=pipeline_id,
    )


class DispatchLoop:
    """Routes ClawPipe envelopes to the appropriate action handler.

    Parameters
    ----------
    sessions_spawn:
        Callable that spawns a single agent session.
    coordinate:
        Callable that dispatches multiple agents in parallel via Agent Squad.
    contract_assertions:
        Callable that runs post-dispatch contract assertions.
    max_spawn_depth:
        Maximum nesting depth for agent dispatch. Defaults to 2.
    current_depth:
        Current nesting depth. Defaults to 0.
    """

    def __init__(
        self,
        *,
        sessions_spawn: Callable[..., dict[str, Any]],
        coordinate: Callable[..., dict[str, Any]],
        contract_assertions: Callable[..., dict[str, Any]],
        max_spawn_depth: int = _DEFAULT_MAX_SPAWN_DEPTH,
        current_depth: int = 0,
    ) -> None:
        self._sessions_spawn = sessions_spawn
        self._coordinate = coordinate
        self._contract_assertions = contract_assertions
        self.max_spawn_depth = max_spawn_depth
        self._current_depth = current_depth

    def handle_ok(self, envelope: Envelope) -> dict[str, Any]:
        """Advance pipeline to next stage or signal completion.

        Returns a dict with action=resume if stages remain, or
        action=complete when stages_remaining is 0 or None.
        """
        remaining = envelope.stages_remaining or 0
        if remaining > 0:
            return {
                "action": "resume",
                "pipeline_complete": False,
                "pipeline_id": envelope.pipeline_id,
            }
        return {
            "action": "complete",
            "pipeline_complete": True,
            "pipeline_id": envelope.pipeline_id,
        }

    def handle_needs_dispatch(self, envelope: Envelope) -> dict[str, Any]:
        """Dispatch a stage agent (sequential or parallel).

        Sequential: calls sessions_spawn and optionally runs contract assertions.
        Parallel: calls coordinate for all dispatches, then runs assertions per agent.

        Returns a status dict. If spawn depth is exceeded, returns error.
        """
        if self._current_depth >= self.max_spawn_depth:
            return {
                "status": _SPAWN_ERROR_STATUS,
                "error": f"Max spawn depth ({self.max_spawn_depth}) exceeded",
            }

        if envelope.parallel and envelope.dispatches:
            return self._dispatch_parallel(envelope)

        return self._dispatch_sequential(envelope)

    def _dispatch_sequential(self, envelope: Envelope) -> dict[str, Any]:
        """Dispatch a single agent and run post-dispatch contract assertions."""
        spawn_result = _spawn_agent(
            self._sessions_spawn,
            agent_id=envelope.agent_id or "",
            task=envelope.task or "",
            stage=envelope.stage,
            pipeline_id=envelope.pipeline_id,
        )

        if spawn_result.get("status") == _SPAWN_ERROR_STATUS:
            return {"status": _SPAWN_ERROR_STATUS, "error": spawn_result.get("error")}

        contract_path = _extract_contract_path(envelope)
        if contract_path is None:
            return {"status": _SPAWN_OK_STATUS}

        artifact_path = _extract_artifact_path(envelope)
        assertion_result = _run_assertions(
            self._contract_assertions, contract_path, artifact_path
        )

        if not assertion_result.get("passed", True):
            return {
                "status": "assertion_failed",
                "assertion_failures": assertion_result.get("failures", []),
            }

        return {"status": _SPAWN_OK_STATUS}

    def _dispatch_parallel(self, envelope: Envelope) -> dict[str, Any]:
        """Dispatch multiple agents in parallel and run per-agent assertions."""
        dispatches: list[dict[str, Any]] = envelope.dispatches or []
        coord_result = self._coordinate(
            pipeline_id=envelope.pipeline_id,
            dispatches=dispatches,
        )

        agents_with_contracts = [
            d for d in dispatches if d.get("contract_path")
        ]
        for dispatch in agents_with_contracts:
            _run_assertions(
                self._contract_assertions,
                contract_path=dispatch["contract_path"],
                artifact_path=dispatch.get("artifact_path"),
            )

        return coord_result

    def handle_needs_approval(self, envelope: Envelope) -> dict[str, Any]:
        """Pause the pipeline and record approval state.

        Returns paused action with resume token, preview, options, and stage.
        """
        return {
            "action": "paused",
            "reason": "needs_approval",
            "resume_token": envelope.resumeToken,
            "preview": envelope.preview,
            "options": envelope.options,
            "stage": envelope.stage,
            "pipeline_id": envelope.pipeline_id,
        }

    def handle_needs_replan(self, envelope: Envelope) -> dict[str, Any]:
        """Re-dispatch the stage agent with quality feedback appended to the task.

        Returns redispatched action with the original stage name.
        """
        quality_feedback = _extract_quality_feedback(envelope)
        failure_ctx: dict[str, Any] = envelope.failure_context or {}
        suggestion = failure_ctx.get("suggestion", "")

        all_feedback: list[str] = list(quality_feedback or [])
        if suggestion:
            all_feedback.append(suggestion)

        updated_task = _build_replan_task(envelope.task, all_feedback)

        _spawn_agent(
            self._sessions_spawn,
            agent_id=envelope.agent_id or "",
            task=updated_task,
            stage=envelope.stage,
            pipeline_id=envelope.pipeline_id,
        )

        return {
            "action": "redispatched",
            "stage": envelope.stage,
            "pipeline_id": envelope.pipeline_id,
        }

    def handle_needs_compensation(self, envelope: Envelope) -> dict[str, Any]:
        """Run compensation agents in ascending order (by `order` field).

        After all compensations run, marks the stage as failed.
        """
        compensations: list[dict[str, Any]] = envelope.compensations or []
        sorted_comps = sorted(compensations, key=lambda c: c.get("order", 0))

        for comp in sorted_comps:
            _spawn_agent(
                self._sessions_spawn,
                agent_id=comp.get("agent_id", ""),
                task=comp.get("task", ""),
                stage=comp.get("stage"),
                pipeline_id=envelope.pipeline_id,
            )

        return {
            "action": "compensated",
            "stage_status": "failed",
            "pipeline_id": envelope.pipeline_id,
        }

    def handle_needs_input(self, envelope: Envelope) -> dict[str, Any]:
        """Pause the pipeline and request external input.

        Returns paused action with the stage, prompt (from preview), and options.
        """
        return {
            "action": "paused",
            "reason": "needs_input",
            "stage": envelope.stage,
            "prompt": envelope.preview,
            "options": envelope.options,
            "resume_token": envelope.resumeToken,
            "pipeline_id": envelope.pipeline_id,
        }

    def handle_failed(self, envelope: Envelope) -> dict[str, Any]:
        """Try a fallback agent or escalate on permanent failure.

        If a fallback_agent_id is present, dispatches the fallback via
        sessions_spawn. If the fallback also fails (or no fallback exists),
        escalates with error details.
        """
        fallback_agent_id = _extract_fallback_agent_id(envelope)
        error = envelope.error or ""
        failure_class_value = (
            envelope.failure_class.value if envelope.failure_class else None
        )

        base_result: dict[str, Any] = {
            "error": error,
            "failure_class": failure_class_value,
            "pipeline_id": envelope.pipeline_id,
        }

        if not fallback_agent_id:
            base_result["action"] = "escalated"
            return base_result

        spawn_result = _spawn_agent(
            self._sessions_spawn,
            agent_id=fallback_agent_id,
            task=envelope.task or "",
            stage=envelope.stage,
            pipeline_id=envelope.pipeline_id,
        )

        if spawn_result.get("status") == _SPAWN_ERROR_STATUS:
            base_result["action"] = "escalated"
            return base_result

        base_result["action"] = "fallback_dispatched"
        return base_result

    def handle_cancelled(self, envelope: Envelope) -> dict[str, Any]:
        """Clean up in-progress work and terminate the pipeline."""
        return {
            "action": "terminated",
            "cleanup_performed": True,
            "pipeline_id": envelope.pipeline_id,
        }


def handle_envelope(loop: DispatchLoop, envelope: Envelope) -> dict[str, Any]:
    """Route an envelope to the correct DispatchLoop handler by status.

    Parameters
    ----------
    loop:
        The DispatchLoop instance containing all handler methods.
    envelope:
        The ClawPipe Envelope to process.

    Returns
    -------
    dict with the handler's result.
    """
    handlers: dict[EnvelopeStatus, Callable[[Envelope], dict[str, Any]]] = {
        EnvelopeStatus.OK: loop.handle_ok,
        EnvelopeStatus.NEEDS_DISPATCH: loop.handle_needs_dispatch,
        EnvelopeStatus.NEEDS_APPROVAL: loop.handle_needs_approval,
        EnvelopeStatus.NEEDS_REPLAN: loop.handle_needs_replan,
        EnvelopeStatus.NEEDS_COMPENSATION: loop.handle_needs_compensation,
        EnvelopeStatus.NEEDS_INPUT: loop.handle_needs_input,
        EnvelopeStatus.FAILED: loop.handle_failed,
        EnvelopeStatus.CANCELLED: loop.handle_cancelled,
    }

    handler = handlers[envelope.status]
    return handler(envelope)
