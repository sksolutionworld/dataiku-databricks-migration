"""Normalize recipe-detail payloads into stable RecipeContract objects."""

from __future__ import annotations

from typing import Any

from migration_framework.contracts import ProcessorContract, RecipeContract


def _refs(groups: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for group in groups.values():
        refs.extend(item["ref"] for item in group.get("items", []) if item.get("ref"))
    return refs


def normalize_recipe(raw: dict[str, Any]) -> RecipeContract:
    metadata = raw.get("list_metadata", {})
    settings = raw.get("settings", {})
    processors = [
        ProcessorContract(
            processor_type=step.get("type", "unknown"),
            parameters=step.get("params", {}),
            disabled=step.get("disabled", False),
        )
        for step in settings.get("steps", [])
        if step.get("metaType") == "PROCESSOR"
    ]
    name = raw["recipe_name"]
    return RecipeContract(
        recipe_id=name,
        recipe_name=name,
        recipe_type=raw["recipe_type"],
        inputs=_refs(metadata.get("inputs", {})),
        outputs=_refs(metadata.get("outputs", {})),
        configuration=settings,
        processors=processors,
        metadata={"project_key": metadata.get("projectKey")},
    )
