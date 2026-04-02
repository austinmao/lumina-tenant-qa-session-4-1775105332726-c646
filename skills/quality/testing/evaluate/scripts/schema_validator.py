from __future__ import annotations

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from skills.qa._clawspec_bootstrap import bootstrap_clawspec
else:
    from ..._clawspec_bootstrap import bootstrap_clawspec

bootstrap_clawspec()

from clawspec import schema_validator as clawspec_schema_validator

ValidationIssue = clawspec_schema_validator.ValidationIssue
ValidationResult = clawspec_schema_validator.ValidationResult
detect_contract_kind = clawspec_schema_validator.detect_contract_kind
validate_contract_data = clawspec_schema_validator.validate_contract_data
validate_contract_file = clawspec_schema_validator.validate_contract_file


def main(argv: list[str] | None = None) -> int:
    return clawspec_schema_validator.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
