from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa.validate.scripts.validate import main, validate_target
else:
    from .validate import main, validate_target


if __name__ == "__main__":
    raise SystemExit(main())
