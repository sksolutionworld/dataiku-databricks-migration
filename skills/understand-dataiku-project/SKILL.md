---
name: understand-dataiku-project
description: Inspect and normalize an already-acquired Dataiku project export and recipe-detail evidence before migration planning.
---

# Understand a Dataiku Project

Use local evidence only unless external access is explicitly authorized. Verify `project_export/` and
`recipe_details/index.json`, normalize recipes into canonical contracts, reconcile recipe identity,
type, inputs, and outputs, and build a dependency DAG. Preserve raw files unchanged. Stop on missing
evidence, conflicts, cycles, or suspected secrets; report exact files and fields involved.
