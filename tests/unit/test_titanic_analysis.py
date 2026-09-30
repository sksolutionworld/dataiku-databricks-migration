from pathlib import Path

from migration_framework.orchestration import analyze_project


def test_titanic_project_has_expected_recipe_order(titanic_project_root: Path):
    plan = analyze_project(titanic_project_root)
    assert len(plan.ordered_recipe_ids) == 9
    assert plan.ordered_recipe_ids[0] == "compute_titanic_raw_prepared"
    assert plan.ordered_recipe_ids[-1] in {
        "compute_titanic_migration_output",
        "compute_titanic_survived_stacked_recombined_by_Sex",
    }
    assert all(item.disposition == "SUPPORTED" for item in plan.capabilities)
