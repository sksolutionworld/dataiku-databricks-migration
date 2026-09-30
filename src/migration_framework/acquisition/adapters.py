"""Read-only adapters for already-acquired Dataiku evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProjectExportAdapter:
    def __init__(self, project_export: Path):
        self.project_export = project_export

    def recipe_configs(self) -> dict[str, dict[str, Any]]:
        folder = self.project_export / "project_config" / "recipes"
        return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in folder.glob("*.json")}


class RecipeDetailsAdapter:
    def __init__(self, recipe_details: Path):
        self.recipe_details = recipe_details

    def index(self) -> dict[str, Any]:
        return json.loads((self.recipe_details / "index.json").read_text(encoding="utf-8"))

    def recipes(self) -> list[dict[str, Any]]:
        index = self.index()
        return [
            json.loads((self.recipe_details / item["details_file"]).read_text(encoding="utf-8"))
            for item in index["recipes"]
        ]
