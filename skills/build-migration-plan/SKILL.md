---
name: build-migration-plan
description: Build an ordered, reviewable Dataiku-to-Databricks migration plan from normalized contracts and capability results.
---

# Build a Migration Plan

Require reconciled contracts and an acyclic DAG. Classify every recipe as `SUPPORTED`, `ASSESS`, or
`REQUIRES_REVIEW`; never silently omit one. Persist recipe order, inputs, outputs, selected converter,
target renderer, validation checks, and unresolved decisions. Planning does not authorize deployment.
