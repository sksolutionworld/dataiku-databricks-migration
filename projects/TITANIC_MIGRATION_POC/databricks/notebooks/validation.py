# Databricks notebook source
# MAGIC %md
# MAGIC # Titanic migration validation

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
from lib.quality import assert_titanic_output

dbutils.widgets.text("catalog", "slmt_uat")
dbutils.widgets.text("schema", "exp_seif")
dbutils.widgets.text("table_suffix", "__migration_candidate")
config = MigrationConfig(
    catalog=dbutils.widgets.get("catalog"),
    schema=dbutils.widgets.get("schema"),
    table_suffix=dbutils.widgets.get("table_suffix"),
)

output = spark.table(config.target_table(TABLES["output"]))
assert_titanic_output(output)
display(output.limit(20))
