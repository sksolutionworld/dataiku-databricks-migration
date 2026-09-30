from __future__ import annotations

from migration_framework.contracts import DatasetContract, ProjectContract
from migration_framework.normalization.recipe_normalizer import normalize_recipe


def normalize_project(project_key: str, raw_recipes: list[dict]) -> ProjectContract:
    recipes = [normalize_recipe(recipe) for recipe in raw_recipes]
    produced = {name for recipe in recipes for name in recipe.outputs}
    consumed = {name for recipe in recipes for name in recipe.inputs}
    datasets = [
        DatasetContract(
            name=name,
            role="source" if name not in produced else "output" if name not in consumed else "intermediate",
        )
        for name in sorted(produced | consumed)
    ]
    return ProjectContract(project_key=project_key, datasets=datasets, recipes=recipes)
