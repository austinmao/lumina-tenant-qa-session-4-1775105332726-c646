from __future__ import annotations

from importlib import import_module

# Preserve the legacy `skills.qa.evaluate` import path after the skill tree
# moved under `skills/quality/testing/evaluate/`.
_TARGET_PACKAGE = import_module("skills.quality.testing.evaluate")

__path__ = _TARGET_PACKAGE.__path__

