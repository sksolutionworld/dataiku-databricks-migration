---
name: validate-migration
description: Validate migrated Databricks outputs against Dataiku evidence using policy-driven structural and data checks.
---

# Validate a Migration

Build checks from the persisted migration plan. Compare schema, row count, nulls, duplicates, aggregates,
and declared business rules with configured tolerances. Store expected, actual, status, query or method,
timestamp, and artifact identity as evidence. A failed required check prevents `VALIDATED` status.
