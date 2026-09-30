from __future__ import annotations

import json
from pathlib import Path

from migration_framework.contracts import MigrationPlan, MigrationReport, ProjectContract, RecipeContract


def main() -> None:
    output = Path(__file__).parents[1] / "config" / "schemas"
    output.mkdir(parents=True, exist_ok=True)
    models = {
        "project-contract.schema.json": ProjectContract,
        "recipe-contract.schema.json": RecipeContract,
        "migration-plan.schema.json": MigrationPlan,
        "migration-report.schema.json": MigrationReport,
    }
    for name, model in models.items():
        (output / name).write_text(json.dumps(model.model_json_schema(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
