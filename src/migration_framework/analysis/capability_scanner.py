from __future__ import annotations

from migration_framework.contracts import CapabilityResult, ProjectContract

SUPPORTED = {"shaker", "distinct", "split", "vstack", "grouping", "pivot", "join", "window"}
ASSESS = {"sql", "python"}


def scan_capabilities(project: ProjectContract) -> list[CapabilityResult]:
    results = []
    for recipe in project.recipes:
        if recipe.recipe_type in SUPPORTED:
            disposition, reason = "SUPPORTED", "Deterministic converter available"
        elif recipe.recipe_type in ASSESS:
            disposition, reason = "ASSESS", "Source code requires static assessment"
        else:
            disposition, reason = "REQUIRES_REVIEW", "No deterministic converter registered"
        results.append(CapabilityResult(recipe_id=recipe.recipe_id, recipe_type=recipe.recipe_type, disposition=disposition, reason=reason))
    return results
