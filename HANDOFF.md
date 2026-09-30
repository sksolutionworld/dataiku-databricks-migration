# Delivery handoff

## Status

`TITANIC_MIGRATION_POC` is implemented and validated in Databricks.

- Workspace: `https://adb-7405606041874672.12.azuredatabricks.net/`
- Catalog: `slmt_uat`
- Schema: `exp_seif`
- Source table: `slmt_uat.exp_seif.titanic_raw`
- Candidate suffix: `__migration_candidate`
- Final candidate table: `slmt_uat.exp_seif.titanic_migration_output__migration_candidate`

The candidate suffix is intentional. It prevents the migration test from overwriting source or
existing Dataiku-managed tables.

## What is included

- A reusable migration framework under `src/migration_framework/`.
- The migration orchestrator definition under `agents/`.
- Recipe-specific migration skills under `skills/`.
- Immutable Dataiku project export and recipe evidence under the Titanic project.
- Generated analysis artifacts and the Databricks implementation.
- Unit, baseline, traceability, and Databricks validation assets.
- Formal validation evidence under `projects/TITANIC_MIGRATION_POC/evidence/`.

## Run locally

From the repository root:

```powershell
py -m pip install -e .
py -m unittest discover -s projects/TITANIC_MIGRATION_POC/databricks/tests -p "test_*.py"
```

Analyze the captured Dataiku project without making API calls:

```powershell
python -m migration_framework.cli analyze --project-root projects/TITANIC_MIGRATION_POC
```

## Run in Databricks

1. Upload `projects/TITANIC_MIGRATION_POC/databricks` to a Databricks workspace folder.
2. Confirm `slmt_uat.exp_seif.titanic_raw` exists.
3. Open `notebooks/pipeline.py` and run every cell using Python-capable compute.
4. Open `notebooks/validation.py` and run every cell.
5. Confirm all validation results are `PASS` and all comparison differences are zero.
6. Use `resources/titanic_migration_job.yml` as the job definition when scheduling the flow.

If a notebook cannot import `lib`, run it from the uploaded project folder or add that folder to
`sys.path` before importing. The notebook already contains the supported workspace-path bootstrap.

## Validation interpretation

Validation compares rows by named business columns rather than `SELECT *`. Physical column order
and compatible numeric types can differ between Dataiku and Databricks without changing the data.
Floating-point fields use a tolerance of `1e-6`.

The two source names with trailing spaces are normalized with the same behavior observed in the
Dataiku output. This produced zero remaining name differences.

## Security

No Databricks token, Dataiku API key, username, password, or Azure Key Vault secret is included in
this package. Runtime credentials must be supplied using environment variables or an approved
secret store.

## Scope boundary

The Titanic vertical slice is complete and validated. The framework is reusable, but another
Dataiku project may contain recipe types or processor semantics that require an additional
converter and associated golden tests before it can be declared validated.
