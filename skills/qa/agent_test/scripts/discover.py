from __future__ import annotations

import json
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec

bootstrap_clawspec()

from clawspec.runner import discover as clawspec_discover

discover_scenarios = clawspec_discover.discover_scenarios


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--repo-root" not in args and not any(item.startswith("--repo-root=") for item in args):
        args.extend(["--repo-root", str(_repo_root())])
    return clawspec_discover.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
