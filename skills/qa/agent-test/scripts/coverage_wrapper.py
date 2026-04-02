from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from skills.qa.agent_test.scripts.coverage_wrapper import main


if __name__ == "__main__":
    raise SystemExit(main())
