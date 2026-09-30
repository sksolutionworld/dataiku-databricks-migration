---
name: convert-prepare
description: Convert normalized Dataiku Prepare processors into deterministic transformation IR for Databricks.
---

# Convert Prepare

Consume `RecipeContract.processors` in source order. Map each known processor through the processor
registry and preserve column types, null semantics, and error behavior. For GREL expressions, translate
only recognized constructs and send unknown functions to `REQUIRES_REVIEW`. Emit IR, never raw notebook
code. Verify the operation count and output column lineage against the contract.
