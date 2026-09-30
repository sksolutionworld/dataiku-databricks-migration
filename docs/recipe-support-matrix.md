# Recipe Support Matrix

| Dataiku type | Databricks equivalent | Initial status |
|---|---|---|
| shaker | chained SQL/PySpark expressions | Supported with processor registry |
| distinct | `SELECT DISTINCT` / `dropDuplicates` | Supported |
| split | filtered output branches | Supported |
| vstack | `UNION ALL` / `unionByName` | Supported |
| grouping | `GROUP BY` aggregations | Supported |
| pivot | Spark SQL/PySpark pivot | Supported |
| join | explicit SQL/PySpark join | Supported |
| window | SQL/PySpark window functions | Supported |
| SQL/Python | static assessment, then rewrite/reuse | Assess |
| R/Shell/unknown | manual decision | Requires review |
