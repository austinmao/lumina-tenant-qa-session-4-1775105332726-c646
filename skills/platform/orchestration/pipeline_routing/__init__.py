"""Pipeline routing skill: classify an issue dict to the correct pipeline route.

Route classification logic:
1. Load the pipeline registry YAML from registry_path.
2. For each route, score keyword and label matches against the issue.
3. Select the highest-scoring route. If no route scores above zero, return
   needs_input.
4. Assess priority from priority_signals defined in the route config.
5. Compute confidence (0.0–1.0). If below threshold (0.7), set needs_review.
6. Detect missing required_input_fields and include them in the response.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

# Priority levels in ascending severity order.
_PRIORITY_ORDER = ["normal", "high", "critical"]

# Score divisor used to normalise raw match score into a 0.0–1.0 confidence.
# A score of 5 or above is capped at 1.0.
_SCORE_DIVISOR = 5.0

# Points awarded per unique keyword found in the combined issue text.
_KEYWORD_WEIGHT = 1

# Points awarded per label that matches a route label.
_LABEL_WEIGHT = 2

# Confidence threshold below which needs_review is set.
_CONFIDENCE_THRESHOLD = 0.7


def _load_registry(registry_path: str) -> dict[str, Any]:
    """Load and return the pipeline registry YAML."""
    path = Path(registry_path)
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)  # type: ignore[return-value]


def _normalise_text(value: str | None) -> str:
    """Return lower-cased text or empty string for None/empty values."""
    if not value:
        return ""
    return value.lower()


def _score_route(
    route: dict[str, Any],
    combined_text: str,
    issue_labels: list[str],
) -> float:
    """Return a raw match score for *route* against the issue data."""
    score = 0.0

    # Count unique keyword phrases found in the combined text.
    keywords: list[str] = route.get("keywords", [])
    for keyword in keywords:
        if keyword.lower() in combined_text:
            score += _KEYWORD_WEIGHT

    # Count matching labels.
    route_labels: list[str] = route.get("labels", [])
    for label in issue_labels:
        if label.lower() in [rl.lower() for rl in route_labels]:
            score += _LABEL_WEIGHT

    return score


def _compute_confidence(score: float) -> float:
    """Map a raw score to a confidence value in [0.0, 1.0]."""
    return min(1.0, score / _SCORE_DIVISOR)


def _assess_priority(
    route: dict[str, Any],
    combined_text: str,
    issue_labels: list[str],
    default_priority: str,
) -> str:
    """Return the highest-priority level triggered by priority_signals."""
    priority = default_priority
    signals: list[dict[str, Any]] = route.get("priority_signals", [])

    for signal in signals:
        pattern: str = signal.get("pattern", "")
        source: str = signal.get("source", "description")
        boost: str = signal.get("boost", "normal")

        matched = False
        if source == "labels":
            matched = any(
                re.search(pattern, label, re.IGNORECASE)
                for label in issue_labels
            )
        else:
            matched = bool(re.search(pattern, combined_text, re.IGNORECASE))

        if matched and _higher_priority(boost, priority):
            priority = boost

    return priority


def _higher_priority(candidate: str, current: str) -> bool:
    """Return True if *candidate* has strictly higher severity than *current*."""
    candidate_idx = _PRIORITY_ORDER.index(candidate) if candidate in _PRIORITY_ORDER else 0
    current_idx = _PRIORITY_ORDER.index(current) if current in _PRIORITY_ORDER else 0
    return candidate_idx > current_idx


def _detect_missing_fields(
    issue: dict[str, Any],
    required_fields: list[str],
) -> list[str]:
    """Return field names from *required_fields* that are absent or empty."""
    missing: list[str] = []
    for field in required_fields:
        value = issue.get(field)
        if value is None or value == "":
            missing.append(field)
    return missing


def route_work(issue: dict[str, Any], *, registry_path: str) -> dict[str, Any]:
    """Classify *issue* to a pipeline route and return a routing decision.

    Parameters
    ----------
    issue:
        Dict with optional keys: title (str), description (str), labels (list[str]).
    registry_path:
        File path to the pipeline registry YAML.

    Returns
    -------
    dict with keys:
        route_classification (str)
        config_path (str | None)
        priority (str)
        confidence (float)
        pipeline_input (dict)
        needs_review (bool)  — present when confidence < threshold
        missing_fields (list[str])  — present when required fields are absent
    """
    registry = _load_registry(registry_path)
    defaults: dict[str, Any] = registry.get("defaults", {})
    default_priority: str = defaults.get("priority", "normal")
    confidence_threshold: float = float(defaults.get("confidence_threshold", _CONFIDENCE_THRESHOLD))

    # Normalise issue fields, treating None as empty.
    title: str = _normalise_text(issue.get("title"))
    description: str = _normalise_text(issue.get("description"))
    raw_labels = issue.get("labels") or []
    issue_labels: list[str] = [str(lbl).lower() for lbl in raw_labels]

    combined_text = f"{title} {description}".strip()

    routes: list[dict[str, Any]] = registry.get("routes", [])

    best_route: dict[str, Any] | None = None
    best_score = 0.0

    for route in routes:
        score = _score_route(route, combined_text, issue_labels)
        if score > best_score:
            best_score = score
            best_route = route

    # Build the pipeline_input from the original (non-normalised) issue data.
    pipeline_input: dict[str, Any] = {
        "title": issue.get("title"),
        "description": issue.get("description"),
        "labels": issue.get("labels") or [],
    }

    # No route matched — return needs_input.
    if best_route is None or best_score == 0.0:
        result: dict[str, Any] = {
            "route_classification": "needs_input",
            "config_path": None,
            "priority": default_priority,
            "confidence": 0.0,
            "pipeline_input": pipeline_input,
            "needs_review": True,
        }
        return result

    confidence = _compute_confidence(best_score)
    priority = _assess_priority(
        best_route, combined_text, issue_labels, default_priority
    )

    result = {
        "route_classification": best_route["classification"],
        "config_path": best_route.get("pipeline_config"),
        "priority": priority,
        "confidence": confidence,
        "pipeline_input": pipeline_input,
    }

    if confidence < confidence_threshold:
        result["needs_review"] = True

    missing = _detect_missing_fields(issue, best_route.get("required_input_fields", []))
    if missing:
        result["missing_fields"] = missing

    return result
