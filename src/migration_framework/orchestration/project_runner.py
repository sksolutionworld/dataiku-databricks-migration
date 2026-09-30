from __future__ import annotations

import json
from pathlib import Path

from migration_framework.acquisition import ProjectExportAdapter, RecipeDetailsAdapter
from migration_framework.analysis import reconcile, scan_capabilities, topological_recipe_order
from migration_framework.contracts import MigrationPlan
from migration_framework.normalization import normalize_project


def analyze_project(project_root: Path) -> MigrationPlan:
    raw = project_root / "dataiku" / "raw"
    details = RecipeDetailsAdapter(raw / "recipe_details")
    exports = ProjectExportAdapter(raw / "project_export")
    index = details.index()
    raw_recipes = details.recipes()
    conflicts = reconcile(exports.recipe_configs(), raw_recipes)
    if conflicts:
        raise ValueError("Evidence reconciliation failed: " + "; ".join(conflicts))
    project = normalize_project(index["project_key"], raw_recipes)
    plan = MigrationPlan(
        project_key=project.project_key,
        ordered_recipe_ids=topological_recipe_order(project),
        capabilities=scan_capabilities(project),
    )
    analysis = project_root / "analysis"
    analysis.mkdir(parents=True, exist_ok=True)
    (analysis / "normalized-project.json").write_text(project.model_dump_json(indent=2), encoding="utf-8")
    (analysis / "migration-plan.json").write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    return plan
