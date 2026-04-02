"""GovernanceProjector — mirrors ClawPipe pipeline state to Paperclip issues.

Projects pipeline lifecycle events (started, dispatched, completed, etc.) as
Paperclip issue mutations. Resilient: failures are queued for later replay via
flush_pending(). Every event is audit-logged to a daily YAML file.

FR-016/SC-006: assigneeAgentId is ALWAYS the orchestrator, never the executor.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_QUEUE_SIZE = 100
DEFAULT_TIMEOUT_SECONDS = 10


# ---------------------------------------------------------------------------
# GovernanceProjector
# ---------------------------------------------------------------------------


class GovernanceProjector:
    """Projects ClawPipe pipeline state to Paperclip as a governance mirror."""

    def __init__(
        self,
        *,
        base_url: str = "http://localhost:3101/api",
        company_id: str,
        audit_dir: str = "memory/logs/governance",
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._company_id = company_id
        self._audit_dir = audit_dir
        # Composite key {pipeline_id}:{stage_id} -> child_issue_id
        self._dedup_index: dict[str, str] = {}
        self.pending_queue: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public projection methods
    # ------------------------------------------------------------------

    def project_started(
        self,
        *,
        parent_issue_id: str,
        pipeline_id: str,
    ) -> None:
        """PATCH parent issue to in_progress with pipeline metadata."""
        payload = {
            "status": "in_progress",
            "metadata": {
                "clawpipe_pipeline_id": pipeline_id,
                "clawpipe_status": "started",
            },
        }
        self._patch_issue(
            issue_id=parent_issue_id,
            payload=payload,
            event_type="started",
            pipeline_id=pipeline_id,
        )

    def project_dispatched(
        self,
        *,
        parent_issue_id: str,
        pipeline_id: str,
        pipeline_name: str,
        stage_id: str,
        stage_name: str,
        stage_task: str,
        orchestrator_agent_id: str,
        executor_agent_id: str,
    ) -> str | None:
        """POST child issue (or PATCH if already exists) for the stage.

        Returns the child issue ID or None on failure.
        FR-016/SC-006: assigneeAgentId is the orchestrator, not the executor.
        """
        dedup_key = f"{pipeline_id}:{stage_id}"
        existing_id = self._dedup_index.get(dedup_key)

        payload: dict[str, Any] = {
            "title": f"[{pipeline_name}] {stage_name}",
            "status": "in_progress",
            "assigneeAgentId": orchestrator_agent_id,
            "parentIssueId": parent_issue_id,
            "metadata": {
                "clawpipe_pipeline_id": pipeline_id,
                "clawpipe_stage": stage_id,
                "clawpipe_status": "dispatched",
                "executor_agent_id": executor_agent_id,
                "is_mirror_managed": True,
                "started_at": _utc_now(),
            },
        }

        if existing_id:
            result = self._patch_issue(
                issue_id=existing_id,
                payload=payload,
                event_type="dispatched",
                pipeline_id=pipeline_id,
                stage_id=stage_id,
                dedup_key=dedup_key,
            )
            if result is not None:
                return existing_id
            return existing_id  # still return existing_id even on patch error
        else:
            child_id = self._post_issue(
                payload=payload,
                event_type="dispatched",
                pipeline_id=pipeline_id,
                stage_id=stage_id,
                dedup_key=dedup_key,
            )
            if child_id:
                self._dedup_index[dedup_key] = child_id
            return child_id

    def project_completed(
        self,
        *,
        child_issue_id: str,
        pipeline_id: str,
        stage_id: str,
        artifact_paths: list[str],
    ) -> None:
        """PATCH child issue to done with artifact paths."""
        payload: dict[str, Any] = {
            "status": "done",
            "metadata": {
                "clawpipe_status": "ok",
                "completed_at": _utc_now(),
                "artifact_paths": artifact_paths,
            },
        }
        self._patch_issue(
            issue_id=child_issue_id,
            payload=payload,
            event_type="completed",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def project_approval_gate(
        self,
        *,
        child_issue_id: str,
        pipeline_id: str,
        stage_id: str,
        stage_name: str,
    ) -> None:
        """PATCH metadata status + POST approval-needed comment."""
        patch_payload: dict[str, Any] = {
            "metadata": {
                "clawpipe_status": "needs_approval",
            },
        }
        self._patch_issue(
            issue_id=child_issue_id,
            payload=patch_payload,
            event_type="approval_gate_patch",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )
        comment_payload = {
            "body": f"[APPROVAL NEEDED] Stage '{stage_name}' requires operator approval.",
        }
        self._post_comment(
            issue_id=child_issue_id,
            payload=comment_payload,
            event_type="approval_gate",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def project_failed(
        self,
        *,
        child_issue_id: str,
        pipeline_id: str,
        stage_id: str,
        error_message: str,
        retry_count: int = 0,
    ) -> None:
        """PATCH child issue to cancelled with error details."""
        payload: dict[str, Any] = {
            "status": "cancelled",
            "metadata": {
                "clawpipe_status": "failed",
                "error": error_message,
                "retry_count": retry_count,
            },
        }
        self._patch_issue(
            issue_id=child_issue_id,
            payload=payload,
            event_type="failed",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def project_cancelled(
        self,
        *,
        child_issue_id: str,
        pipeline_id: str,
        stage_id: str,
    ) -> None:
        """PATCH child issue to cancelled for operator-initiated cancellation."""
        payload: dict[str, Any] = {
            "status": "cancelled",
            "metadata": {
                "clawpipe_status": "cancelled",
                "cancelled_at": _utc_now(),
            },
        }
        self._patch_issue(
            issue_id=child_issue_id,
            payload=payload,
            event_type="cancelled",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def project_pipeline_completed(
        self,
        *,
        parent_issue_id: str,
        pipeline_id: str,
    ) -> None:
        """PATCH parent issue to done."""
        payload: dict[str, Any] = {
            "status": "done",
            "metadata": {
                "clawpipe_status": "completed",
                "completed_at": _utc_now(),
            },
        }
        self._patch_issue(
            issue_id=parent_issue_id,
            payload=payload,
            event_type="pipeline_completed",
            pipeline_id=pipeline_id,
        )

    def project_compensation(
        self,
        *,
        child_issue_id: str,
        pipeline_id: str,
        stage_id: str,
        stage_name: str,
    ) -> None:
        """POST compensation comment + PATCH metadata status."""
        comment_payload = {
            "body": f"[COMPENSATION IN PROGRESS] Stage '{stage_name}' is being compensated.",
        }
        self._post_comment(
            issue_id=child_issue_id,
            payload=comment_payload,
            event_type="compensation",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )
        patch_payload: dict[str, Any] = {
            "metadata": {
                "clawpipe_status": "needs_compensation",
            },
        }
        self._patch_issue(
            issue_id=child_issue_id,
            payload=patch_payload,
            event_type="compensation_patch",
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def flush_pending(self) -> int:
        """Replay queued events. Returns number of successfully flushed events."""
        if not self.pending_queue:
            return 0

        flushed_count = 0
        remaining: list[dict[str, Any]] = []

        for event in self.pending_queue:
            try:
                self._execute_http_request(
                    method=event["method"],
                    url=event["url"],
                    body=event.get("body"),
                )
                flushed_count += 1
            except Exception:
                remaining.append(event)

        self.pending_queue = remaining
        return flushed_count

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------

    def _patch_issue(
        self,
        *,
        issue_id: str,
        payload: dict[str, Any],
        event_type: str,
        pipeline_id: str,
        stage_id: str | None = None,
        dedup_key: str | None = None,
    ) -> dict[str, Any] | None:
        url = f"{self._base_url}/issues/{issue_id}"
        return self._send(
            method="PATCH",
            url=url,
            body=payload,
            event_type=event_type,
            pipeline_id=pipeline_id,
            stage_id=stage_id,
            dedup_key=dedup_key,
        )

    def _post_issue(
        self,
        *,
        payload: dict[str, Any],
        event_type: str,
        pipeline_id: str,
        stage_id: str | None = None,
        dedup_key: str | None = None,
    ) -> str | None:
        url = f"{self._base_url}/companies/{self._company_id}/issues"
        result = self._send(
            method="POST",
            url=url,
            body=payload,
            event_type=event_type,
            pipeline_id=pipeline_id,
            stage_id=stage_id,
            dedup_key=dedup_key,
        )
        if result is not None:
            return result.get("id")
        return None

    def _post_comment(
        self,
        *,
        issue_id: str,
        payload: dict[str, Any],
        event_type: str,
        pipeline_id: str,
        stage_id: str | None = None,
    ) -> dict[str, Any] | None:
        url = f"{self._base_url}/issues/{issue_id}/comments"
        return self._send(
            method="POST",
            url=url,
            body=payload,
            event_type=event_type,
            pipeline_id=pipeline_id,
            stage_id=stage_id,
        )

    def _send(
        self,
        *,
        method: str,
        url: str,
        body: dict[str, Any] | None,
        event_type: str,
        pipeline_id: str,
        stage_id: str | None = None,
        dedup_key: str | None = None,
    ) -> dict[str, Any] | None:
        """Execute HTTP request with resilience: queue on failure, always audit."""
        start_ms = time.monotonic() * 1000
        response_status: int | None = None
        error_msg: str | None = None
        result: dict[str, Any] | None = None

        try:
            response_body = self._execute_http_request(
                method=method,
                url=url,
                body=body,
            )
            response_status = response_body.get("_status", 200)
            result = response_body
        except Exception as exc:
            error_msg = str(exc)
            self._enqueue(
                method=method,
                url=url,
                body=body,
                event_type=event_type,
                pipeline_id=pipeline_id,
            )

        duration_ms = time.monotonic() * 1000 - start_ms
        self._audit_log(
            event_type=event_type,
            pipeline_id=pipeline_id,
            stage_id=stage_id,
            action=f"{method} {url}",
            response_status=response_status,
            success=error_msg is None,
            error=error_msg,
            dedup_key=dedup_key,
            duration_ms=duration_ms,
        )
        return result

    def _execute_http_request(
        self,
        *,
        method: str,
        url: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute an HTTP request using urllib. Returns parsed JSON body."""
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url=url,
            data=data,
            headers={"Content-Type": "application/json"},
            method=method,
        )
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT_SECONDS) as resp:
            raw = resp.read()
            status = resp.status
            parsed: dict[str, Any] = {}
            if raw:
                try:
                    parsed = json.loads(raw)
                except (json.JSONDecodeError, ValueError):
                    parsed = {}
            parsed["_status"] = status
            return parsed

    # ------------------------------------------------------------------
    # Resilience queue
    # ------------------------------------------------------------------

    def _enqueue(
        self,
        *,
        method: str,
        url: str,
        body: dict[str, Any] | None,
        event_type: str,
        pipeline_id: str,
    ) -> None:
        """Add a failed event to the pending queue (capped at MAX_QUEUE_SIZE)."""
        if len(self.pending_queue) >= MAX_QUEUE_SIZE:
            return
        self.pending_queue.append(
            {
                "event_type": event_type,
                "pipeline_id": pipeline_id,
                "method": method,
                "url": url,
                "body": body,
                "queued_at": _utc_now(),
            }
        )

    # ------------------------------------------------------------------
    # Audit logging
    # ------------------------------------------------------------------

    def _audit_log(
        self,
        *,
        event_type: str,
        pipeline_id: str,
        stage_id: str | None,
        action: str,
        response_status: int | None,
        success: bool,
        error: str | None,
        dedup_key: str | None,
        duration_ms: float,
    ) -> None:
        """Append an audit entry to today's YAML log file."""
        os.makedirs(self._audit_dir, exist_ok=True)
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        log_path = os.path.join(self._audit_dir, f"{today}.yaml")

        entry: dict[str, Any] = {
            "timestamp": _utc_now(),
            "event_type": event_type,
            "pipeline_id": pipeline_id,
            "action": action,
            "paperclip_response_status": response_status,
            "success": success,
            "duration_ms": round(duration_ms, 2),
        }
        if stage_id is not None:
            entry["stage_id"] = stage_id
        if dedup_key is not None:
            entry["dedup_key"] = dedup_key
        if error is not None:
            entry["error"] = error

        existing: list[dict[str, Any]] = []
        if os.path.exists(log_path):
            with open(log_path) as f:
                try:
                    loaded = yaml.safe_load(f)
                    if isinstance(loaded, list):
                        existing = loaded
                except yaml.YAMLError:
                    existing = []

        existing.append(entry)
        with open(log_path, "w") as f:
            yaml.dump(existing, f, allow_unicode=True, sort_keys=False)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def _utc_now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(tz=timezone.utc).isoformat()
