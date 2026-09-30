import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).parents[2]
BASELINE = PROJECT / "evidence" / "baselines" / "dataiku-row-counts.json"


class BaselineTests(unittest.TestCase):
    def test_confirmed_counts_are_complete(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        counts = baseline["row_counts"]
        self.assertEqual(len(counts), 10)
        self.assertEqual(counts["titanic_survived"], 342)
        self.assertEqual(counts["titanic_not_survived"], 549)
        self.assertEqual(counts["titanic_migration_output"], 891)
        self.assertEqual(counts["titanic_survived"] + counts["titanic_not_survived"], counts["titanic_survived_stacked"])


if __name__ == "__main__":
    unittest.main()
