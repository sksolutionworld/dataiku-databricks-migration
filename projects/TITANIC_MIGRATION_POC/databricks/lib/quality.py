"""Reusable data-quality checks for the migrated pipeline."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def row_count(df: DataFrame) -> int:
    return df.count()


def null_count(df: DataFrame, column: str) -> int:
    return df.filter(F.col(column).isNull()).count()


def duplicate_count(df: DataFrame, keys: list[str]) -> int:
    return df.groupBy(*keys).count().filter(F.col("count") > 1).count()


def assert_titanic_output(df: DataFrame) -> None:
    checks = {
        "row count": row_count(df) == 891,
        "PassengerId null count": null_count(df, "PassengerId") == 0,
        "PassengerId duplicate count": duplicate_count(df, ["PassengerId"]) == 0,
        "survivor count": df.filter(F.col("Survived") == 1).count() == 342,
        "non-survivor count": df.filter(F.col("Survived") == 0).count() == 549,
    }
    failures = [name for name, passed in checks.items() if not passed]
    if failures:
        raise ValueError("Titanic validation failed: " + ", ".join(failures))
