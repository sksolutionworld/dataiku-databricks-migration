from __future__ import annotations

from migration_framework.contracts import DependencyContract, ProjectContract


def build_dependencies(project: ProjectContract) -> list[DependencyContract]:
    return [
        DependencyContract(upstream_dataset=input_name, recipe_id=recipe.recipe_id, downstream_dataset=output_name)
        for recipe in project.recipes
        for input_name in recipe.inputs
        for output_name in recipe.outputs
    ]


def topological_recipe_order(project: ProjectContract) -> list[str]:
    producer = {output: recipe.recipe_id for recipe in project.recipes for output in recipe.outputs}
    dependencies = {
        recipe.recipe_id: {producer[i] for i in recipe.inputs if i in producer}
        for recipe in project.recipes
    }
    order: list[str] = []
    remaining = dict(dependencies)
    while remaining:
        ready = sorted(key for key, deps in remaining.items() if deps.issubset(order))
        if not ready:
            raise ValueError("Recipe dependency graph contains a cycle or unresolved dependency")
        order.extend(ready)
        for key in ready:
            remaining.pop(key)
    return order
