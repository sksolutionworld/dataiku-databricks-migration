import unittest

from lib.config import MigrationConfig


class ConfigTests(unittest.TestCase):
    def test_source_table_is_unsuffixed(self):
        config = MigrationConfig("slmt_uat", "exp_seif")
        self.assertEqual(config.source_table("titanic_raw"), "`slmt_uat`.`exp_seif`.`titanic_raw`")

    def test_target_table_uses_candidate_suffix(self):
        config = MigrationConfig("slmt_uat", "exp_seif")
        self.assertEqual(
            config.target_table("titanic_migration_output"),
            "`slmt_uat`.`exp_seif`.`titanic_migration_output__migration_candidate`",
        )

    def test_empty_suffix_is_rejected_for_writes(self):
        config = MigrationConfig("slmt_uat", "exp_seif", table_suffix="")
        with self.assertRaises(ValueError):
            config.target_table("titanic_migration_output")


if __name__ == "__main__":
    unittest.main()
