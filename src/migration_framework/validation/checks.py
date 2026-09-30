from __future__ import annotations

from migration_framework.contracts import ValidationResult


def compare_scalar(check: str, expected: int | float, actual: int | float, tolerance: float = 0) -> ValidationResult:
    passed = abs(actual - expected) <= tolerance
    return ValidationResult(
        check=check,
        status="PASSED" if passed else "FAILED",
        expected=expected,
        actual=actual,
        details={"tolerance": tolerance},
    )


def compare_schema(expected: list[tuple[str, str]], actual: list[tuple[str, str]]) -> ValidationResult:
    return ValidationResult(
        check="schema",
        status="PASSED" if expected == actual else "FAILED",
        expected=expected,
        actual=actual,
    )
