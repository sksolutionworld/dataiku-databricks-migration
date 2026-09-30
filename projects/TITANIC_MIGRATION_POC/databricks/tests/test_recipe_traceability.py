import ast
import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).parents[2]
RAW_DETAILS = PROJECT / "dataiku" / "raw" / "recipe_details"
TRANSFORMATIONS = PROJECT / "databricks" / "lib" / "transformations.py"
TRACEABILITY = PROJECT / "databricks" / "tests" / "expected" / "recipe-traceability.json"


class RecipeTraceabilityTests(unittest.TestCase):
    def test_every_exported_recipe_has_a_mapping(self):
        index = json.loads((RAW_DETAILS / "index.json").read_text(encoding="utf-8"))
        mapping = json.loads(TRACEABILITY.read_text(encoding="utf-8"))
        recipe_names = {item["recipe_name"] for item in index["recipes"]}
        self.assertEqual(recipe_names, set(mapping["recipes"]))

    def test_every_mapped_function_exists(self):
        module = ast.parse(TRANSFORMATIONS.read_text(encoding="utf-8"))
        functions = {node.name for node in module.body if isinstance(node, ast.FunctionDef)}
        mapping = json.loads(TRACEABILITY.read_text(encoding="utf-8"))
        for recipe in mapping["recipes"].values():
            self.assertTrue(set(recipe["functions"]).issubset(functions))

    def test_pivot_contract_matches_export(self):
        raw = json.loads(
            (RAW_DETAILS / "compute_titanic_survived_stacked_recombined_by_Sex.json").read_text(encoding="utf-8")
        )
        settings = raw["settings"]
        self.assertEqual(settings["explicitIdentifiers"], ["Sex"])
        self.assertEqual(settings["pivots"][0]["keyColumns"], ["Pclass"])
        value = settings["pivots"][0]["valueColumns"][0]
        self.assertEqual((value["column"], value["$agg"]), ("Survived", "avg"))

    def test_source_compatibility_normalization_is_traceable(self):
        mapping = json.loads(TRACEABILITY.read_text(encoding="utf-8"))
        prepared = mapping["recipes"]["compute_titanic_raw_prepared"]
        self.assertEqual(prepared["status"], "VERIFIED_WITH_SOURCE_COMPATIBILITY_NORMALIZATION")
        self.assertTrue(any("trailing ASCII spaces" in note for note in prepared["compatibility_notes"]))

    def test_window_contract_matches_export(self):
        raw = json.loads(
            (RAW_DETAILS / "compute_titanic_survived_stacked_recombined_joined_enriched_windows.json").read_text(
                encoding="utf-8"
            )
        )
        window = raw["settings"]["windows"][0]
        self.assertEqual(window["partitioningColumns"], ["Pclass"])
        self.assertEqual(window["orders"], [{"column": "Fare", "desc": True}, {"column": "PassengerId", "desc": False}])
        self.assertTrue(raw["settings"]["rowNumber"])


if __name__ == "__main__":
    unittest.main()
