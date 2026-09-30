# Dataiku to Databricks Migration Framework

An auditable, deterministic framework for translating Dataiku projects into Databricks assets.

The framework keeps source evidence immutable and separates acquisition, normalization, analysis,
conversion, rendering, validation, and reporting. The Codex agent coordinates these stages but does
not invent transformations or execute external calls without explicit authorization.

## Local proof of concept

The bundled `TITANIC_MIGRATION_POC` fixture contains nine Dataiku recipes: Prepare, Distinct, Split,
Stack, Group, Pivot, Join, Window, and final Prepare. Run the local analysis without any API calls:

```powershell
python -m migration_framework.cli analyze --project-root projects/TITANIC_MIGRATION_POC
```

See `docs/architecture.md` for the locked design and `agents/dataiku-databricks-migration-orchestrator.md`
for the orchestration contract.

The bundled Titanic migration has been validated in Databricks. See `HANDOFF.md` for execution,
security, packaging, and validation details.
