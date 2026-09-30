# Validation Policy

Required checks are schema, row count, declared uniqueness, null profile, aggregate reconciliation, and
project-specific business rules. Every result records expected and actual values, tolerance, execution
method, artifact identity, and timestamp. Required failures produce `FAILED`; unavailable evidence or
unsupported semantics produce `REQUIRES_REVIEW`.
