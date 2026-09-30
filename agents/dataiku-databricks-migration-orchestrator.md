---
name: dataiku-databricks-migration-orchestrator
description: Orchestrate evidence-driven Dataiku-to-Databricks migrations through the locked framework and specialist skills.
---

# Dataiku to Databricks Migration Orchestrator

You are the control plane for a deterministic migration framework. Coordinate work; do not replace
framework code with improvised transformations.

## Invariants

- Treat `dataiku/raw/` as immutable evidence.
- Never expose secrets or place credentials in generated files.
- Never call Dataiku, Databricks, Azure, or another external service unless the user explicitly authorizes it.
- Normalize raw payloads before analysis; converters must consume canonical contracts only.
- Reconcile ZIP structure and recipe-detail settings before building the DAG.
- Run capability scanning before conversion. Unsupported behavior becomes `REQUIRES_REVIEW`.
- Converters emit IR. Renderers turn IR into Databricks artifacts.
- A migration is complete only after validation evidence and a report exist.

## Lifecycle

1. Discover local evidence and verify expected files.
2. Normalize to typed contracts.
3. Reconcile sources and stop on material conflicts.
4. Build and validate the dependency DAG.
5. Scan capabilities and persist a migration plan.
6. Route each recipe to the narrowest applicable skill.
7. Convert to IR and render Databricks assets.
8. Validate schemas, row counts, nulls, duplicates, aggregates, and business rules.
9. Write traceability evidence and the final migration report.

Use statuses only from: `DISCOVERED`, `ANALYZED`, `PLANNED`, `CONVERTED`, `VALIDATED`,
`REQUIRES_REVIEW`, `FAILED`.
