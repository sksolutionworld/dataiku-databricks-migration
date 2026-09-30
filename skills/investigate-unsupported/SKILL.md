---
name: investigate-unsupported
description: Investigate an unsupported Dataiku recipe or processor and produce a bounded migration decision without guessing.
---

# Investigate Unsupported Behavior

Use raw evidence and canonical contracts to isolate the unsupported feature. Document semantics, dependencies,
side effects, and candidate Databricks equivalents. Prefer adding a deterministic converter only when behavior
is proven by fixtures and tests. Otherwise retain `REQUIRES_REVIEW` with a concrete decision request.
