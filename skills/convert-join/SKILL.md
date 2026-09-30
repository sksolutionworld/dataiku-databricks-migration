---
name: convert-join
description: Convert normalized Dataiku Join recipes into explicit join IR while preserving keys, join type, and selected columns.
---

# Convert Join

Preserve input order, join type, all key pairs, null/case behavior, match limits, selected columns, and
aliases. Reject ambiguous duplicate names unless the contract defines resolution. Verify expected join
cardinality during validation; do not infer business keys.
