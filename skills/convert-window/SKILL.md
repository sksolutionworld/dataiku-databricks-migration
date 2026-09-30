---
name: convert-window
description: Convert normalized Dataiku Window recipes into deterministic window IR, including partitions, ordering, frames, and ranks.
---

# Convert Window

Preserve partition keys, ordered columns and directions, null ordering, frame bounds, and operation type.
Ranking must have a deterministic tie-breaker; otherwise mark the recipe `REQUIRES_REVIEW`. Distinguish
`row_number`, `rank`, and `dense_rank` exactly.
