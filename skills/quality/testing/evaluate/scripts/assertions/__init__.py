from __future__ import annotations

from typing import Any, Callable


AssertionHandler = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
_REGISTRY: dict[str, AssertionHandler] = {}


class AssertionDispatchError(KeyError):
    """Raised when an assertion type has no registered handler."""


def register_assertion(assertion_type: str, handler: AssertionHandler) -> None:
    _REGISTRY[assertion_type] = handler


def get_registered_assertions() -> dict[str, AssertionHandler]:
    load_default_assertions()
    return dict(_REGISTRY)


def load_default_assertions() -> None:
    if _REGISTRY:
        return
    from .artifact import HANDLERS as artifact_handlers
    from .behavioral import HANDLERS as behavioral_handlers
    from .external import HANDLERS as external_handlers
    from .handoff import HANDLERS as handoff_handlers
    from .identity import HANDLERS as identity_handlers
    from .integration import HANDLERS as integration_handlers
    from .operational import HANDLERS as operational_handlers
    from .permission import HANDLERS as permission_handlers
    from .precondition import HANDLERS as precondition_handlers
    from .semantic import HANDLERS as semantic_handlers
    from .tool import HANDLERS as tool_handlers

    for mapping in (
        precondition_handlers,
        integration_handlers,
        artifact_handlers,
        behavioral_handlers,
        external_handlers,
        semantic_handlers,
        tool_handlers,
        handoff_handlers,
        identity_handlers,
        operational_handlers,
        permission_handlers,
    ):
        _REGISTRY.update(mapping)


def dispatch_assertion(assertion: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    load_default_assertions()
    assertion_type = assertion.get("type")
    if not assertion_type:
        raise AssertionDispatchError("Assertion is missing a type")
    try:
        handler = _REGISTRY[assertion_type]
    except KeyError as exc:
        raise AssertionDispatchError(f"Unknown assertion type: {assertion_type}") from exc

    result = handler(assertion, context)
    if "name" not in result:
        result["name"] = assertion_type
    return result
