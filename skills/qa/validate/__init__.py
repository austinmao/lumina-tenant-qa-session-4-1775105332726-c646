from __future__ import annotations

from importlib import import_module

# Preserve the legacy `skills.qa.validate` import path after the skill tree
# moved under `skills/quality/compliance/validate/`.
_TARGET_PACKAGE = import_module("skills.quality.compliance.validate")

__path__ = _TARGET_PACKAGE.__path__

