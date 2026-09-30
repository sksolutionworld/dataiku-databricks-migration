from __future__ import annotations

from typing import Any


def reconcile(export_recipes: dict[str, dict[str, Any]], detail_recipes: list[dict[str, Any]]) -> list[str]:
    """Return evidence conflicts; recipe details own settings, export owns structure."""
    conflicts: list[str] = []
    for raw in detail_recipes:
        name = raw["recipe_name"]
        exported = export_recipes.get(name)
        if exported is None:
            conflicts.append(f"{name}: missing from project export")
        elif exported.get("type") != raw.get("recipe_type"):
            conflicts.append(f"{name}: recipe type differs between sources")
    for name in export_recipes.keys() - {r["recipe_name"] for r in detail_recipes}:
        conflicts.append(f"{name}: missing recipe-detail evidence")
    return sorted(conflicts)
