"""Environment-driven table configuration for the Titanic migration."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MigrationConfig:
    catalog: str
    schema: str
    table_suffix: str = "__migration_candidate"

    def source_table(self, logical_name: str) -> str:
        """Fully qualified existing source; source names are never suffixed."""
        return self._qualified(logical_name)

    def target_table(self, logical_name: str) -> str:
        """Fully qualified migration output protected by the candidate suffix."""
        if not self.table_suffix:
            raise ValueError("table_suffix must not be empty for migration writes")
        return self._qualified(f"{logical_name}{self.table_suffix}")

    def _qualified(self, table_name: str) -> str:
        return f"`{self.catalog}`.`{self.schema}`.`{table_name}`"


TABLES = {
    "raw": "titanic_raw",
    "prepared": "titanic_raw_prepared",
    "distinct": "titanic_raw_prepared_distinct",
    "survived": "titanic_survived",
    "not_survived": "titanic_not_survived",
    "stacked": "titanic_survived_stacked",
    "summary": "titanic_survived_stacked_summary",
    "pivot": "titanic_survived_stacked_recombined_by_Sex",
    "enriched": "titanic_survived_stacked_recombined_joined_enriched",
    "windowed": "titanic_survived_stacked_recombined_joined_enriched_ranked",
    "output": "titanic_migration_output",
}
