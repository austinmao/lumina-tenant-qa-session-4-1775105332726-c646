from __future__ import annotations

import os
import sys
from pathlib import Path


def bootstrap_clawspec(*, marker: str = "__init__.py") -> None:
    try:
        import clawspec  # noqa: F401
        return
    except ModuleNotFoundError:
        pass

    candidates: list[Path] = []
    explicit = os.environ.get("CLAWSPEC_REPO")
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())

    repo_root = Path(__file__).resolve().parents[2]
    candidates.append(repo_root.parent / "clawspec")

    for candidate in candidates:
        package_file = candidate / "clawspec" / marker
        if package_file.exists():
            sys.path.insert(0, str(candidate))
            return

    raise ModuleNotFoundError(
        "clawspec is not importable. Install it with `python3 -m pip install -e ../clawspec`, "
        "or set CLAWSPEC_REPO to the standalone repo path."
    )


def seed_hooks_token(*, env_path: Path | None = None) -> None:
    if os.environ.get("HOOKS_TOKEN") or os.environ.get("OPENCLAW_HOOKS_TOKEN"):
        return

    target = env_path or (Path.home() / ".openclaw" / ".env")
    if not target.exists():
        return

    for line in target.read_text(encoding="utf-8").splitlines():
        if line.startswith("HOOKS_TOKEN="):
            value = line.split("=", 1)[1].strip().strip("'").strip('"')
            if value:
                os.environ["HOOKS_TOKEN"] = value
            return
