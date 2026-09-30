# Locked Architecture

```text
Dataiku ZIP + recipe details
            |
       acquisition
            |
   immutable raw evidence
            |
      normalization
            |
     typed contracts
            |
 reconciliation -> dependency DAG -> capability scan -> migration plan
            |
       converters
            |
            IR
            |
        renderers
            |
 Databricks project assets
            |
 validation -> evidence -> migration report
```

The agent is the control plane. Python framework components are the execution plane. Skills hold bounded
decision guidance; they do not duplicate converter business logic. Structural changes require an ADR.
