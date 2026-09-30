"""Extract complete recipe metadata from a Dataiku project as JSON evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from dataikuapi import DSSClient
except ImportError as exc:
    raise SystemExit(
        "Missing dependency 'dataikuapi'. Install it with: "
        "python -m pip install -r requirements.txt"
    ) from exc


DEFAULT_PROJECT_KEY = "TITANIC_MIGRATION_POC"
BASE_DIR = Path(__file__).resolve().parent
SENSITIVE_KEY = re.compile(
    r"password|secret|token|api[_-]?key|credential|authorization|cookie|private[_-]?key",
    re.IGNORECASE,
)


def required_environment(name: str) -> str:
    """Return a required non-empty environment variable."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Set {name} in the current PowerShell session.")
    return value


def redact_sensitive_values(value: Any, key: str = "") -> Any:
    """Redact likely credentials before recipe evidence is written to disk."""
    if SENSITIVE_KEY.search(key):
        return "<REDACTED>"
    if isinstance(value, dict):
        return {
            str(item_key): redact_sensitive_values(item_value, str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive_values(item) for item in value]
    return value


def safe_file_name(value: str) -> str:
    """Convert a Dataiku object name into a safe JSON filename."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return cleaned or "unnamed_recipe"


def json_ready(value: Any) -> Any:
    """Convert SDK payloads to plain JSON-compatible objects."""
    return json.loads(json.dumps(value, default=str))


def recipe_payload(project: Any, recipe_info: dict[str, Any]) -> dict[str, Any]:
    """Collect list metadata and the full settings payload for one recipe."""
    recipe_name = recipe_info["name"]
    recipe = project.get_recipe(recipe_name)
    settings = recipe.get_settings()
    settings_payload = getattr(settings, "obj_payload", None)

    return {
        "recipe_name": recipe_name,
        "recipe_type": recipe_info.get("type", "unknown"),
        "list_metadata": redact_sensitive_values(json_ready(recipe_info)),
        "settings": redact_sensitive_values(json_ready(settings_payload)),
    }


def write_json(path: Path, payload: Any) -> None:
    """Write formatted UTF-8 JSON."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract raw recipe details from a Dataiku project."
    )
    parser.add_argument(
        "--project-key",
        default=os.environ.get("DATAIKU_PROJECT_KEY", DEFAULT_PROJECT_KEY),
        help="Dataiku project key (default: DATAIKU_PROJECT_KEY or Titanic POC)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    dataiku_url = required_environment("DATAIKU_URL").rstrip("/")
    dataiku_api_key = required_environment("DATAIKU_API_KEY")

    output_dir = (
        BASE_DIR
        / "projects"
        / args.project_key
        / "dataiku"
        / "raw"
        / "recipe_details"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    client = DSSClient(dataiku_url, api_key=dataiku_api_key)
    project = client.get_project(args.project_key)
    recipes = project.list_recipes()

    extracted_at = datetime.now(timezone.utc).isoformat()
    index_entries: list[dict[str, Any]] = []

    print(f"Project: {args.project_key}")
    print(f"Recipes: {len(recipes)}")

    for recipe_info in recipes:
        details = recipe_payload(project, recipe_info)
        recipe_name = details["recipe_name"]
        file_name = f"{safe_file_name(recipe_name)}.json"
        write_json(output_dir / file_name, details)
        index_entries.append(
            {
                "recipe_name": recipe_name,
                "recipe_type": details["recipe_type"],
                "details_file": file_name,
            }
        )
        print(f"Extracted: {recipe_name} [{details['recipe_type']}]")

    index = {
        "schema_version": "1.0",
        "project_key": args.project_key,
        "extracted_at_utc": extracted_at,
        "recipe_count": len(index_entries),
        "recipes": index_entries,
    }
    write_json(output_dir / "index.json", index)

    print()
    print("Recipe-details extraction completed successfully.")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()
