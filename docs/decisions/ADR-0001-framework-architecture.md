# ADR-0001: Evidence-first migration architecture

## Status

Accepted

## Decision

Use immutable acquisition evidence, canonical Pydantic contracts, deterministic converters producing an
intermediate representation, replaceable renderers, policy-driven validation, and mandatory traceability.
The orchestrator agent coordinates stages but cannot bypass framework controls.

## Consequences

Raw Dataiku format changes are isolated to adapters and normalizers. Conversion tests do not require API
access. Unsupported behavior is visible instead of silently approximated.
