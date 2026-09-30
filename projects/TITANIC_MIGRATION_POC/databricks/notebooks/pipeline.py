# Databricks notebook source
# MAGIC %md
# MAGIC # Titanic migration pipeline

# COMMAND ----------

import sys
from pathlib import Path


def _add_project_root_to_path() -> Path:
    notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
    current_folder = (Path("/Workspace") / notebook_path.lstrip("/")).parent
    for candidate in (current_folder, *current_folder.parents):
        if (candidate / "lib" / "config.py").is_file():
            project_root = str(candidate)
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            return candidate
    raise FileNotFoundError(
        f"Could not find lib/config.py above {current_folder}. "
        "Upload the lib folder and this notebook under the same project folder."
    )


PROJECT_ROOT = _add_project_root_to_path()

from lib.config import MigrationConfig, TABLES
from lib.transformations import (
    add_fare_rank,
    distinct_rows,
    join_summary,
    pivot_survival_by_class,
    prepare_titanic,
    select_final_columns,
    split_survival,
    stack_survival,
    summarize_by_sex_and_class,
)

dbutils.widgets.text("catalog", "slmt_uat")
dbutils.widgets.text("schema", "exp_seif")
dbutils.widgets.text("table_suffix", "__migration_candidate")
config = MigrationConfig(
    catalog=dbutils.widgets.get("catalog"),
    schema=dbutils.widgets.get("schema"),
    table_suffix=dbutils.widgets.get("table_suffix"),
)

# COMMAND ----------

raw = spark.table(config.source_table(TABLES["raw"]))
prepared = prepare_titanic(raw)
deduplicated = distinct_rows(prepared)
survived, not_survived = split_survival(deduplicated)
stacked = stack_survival(survived, not_survived)
summary = summarize_by_sex_and_class(stacked)
pivot = pivot_survival_by_class(stacked)
enriched = join_summary(stacked, summary)
windowed = add_fare_rank(enriched)
output = select_final_columns(windowed)

datasets = {
    "prepared": prepared,
    "distinct": deduplicated,
    "survived": survived,
    "not_survived": not_survived,
    "stacked": stacked,
    "summary": summary,
    "pivot": pivot,
    "enriched": enriched,
    "windowed": windowed,
    "output": output,
}

for logical_name, dataframe in datasets.items():
    dataframe.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(
        config.target_table(TABLES[logical_name])
    )
