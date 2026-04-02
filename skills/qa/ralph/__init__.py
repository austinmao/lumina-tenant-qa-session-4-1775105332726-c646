from __future__ import annotations

from importlib import import_module

# Preserve the legacy `skills.qa.ralph` import path after the skill tree moved
# under `skills/quality/testing/ralph/`.
_TARGET_PACKAGE = import_module("skills.quality.testing.ralph")

__path__ = _TARGET_PACKAGE.__path__

