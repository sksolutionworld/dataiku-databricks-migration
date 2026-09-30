---
name: convert-stack
description: Convert normalized Dataiku Stack recipes into union IR while preserving schema alignment and origin-column behavior.
---

# Convert Stack

Keep input order. Choose by-name versus positional union only from configuration, preserve duplicate rows,
and model missing columns explicitly. If types conflict, require a declared cast policy. Validate total row
count as the sum of inputs unless filters are part of the contract.
