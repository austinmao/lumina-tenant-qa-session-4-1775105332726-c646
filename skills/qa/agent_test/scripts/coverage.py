from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec
    from skills.qa.agent_test.scripts.coverage_compat import (
        build_summary,
        find_contract_gaps,
        load_ledger,
        main as compatibility_main,
        resolve_repo_root,
    )
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec
    from .coverage_compat import (
        build_summary,
        find_contract_gaps,
        load_ledger,
        main as compatibility_main,
        resolve_repo_root,
    )

bootstrap_clawspec()


def main(argv: list[str] | None = None) -> int:
    return compatibility_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
