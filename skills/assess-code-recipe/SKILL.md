---
name: assess-code-recipe
description: Statically assess Dataiku SQL or Python recipe code for migration feasibility without executing it.
---

# Assess a Code Recipe

Perform static analysis only. Record language, inputs, outputs, imports, external I/O, secrets, dynamic SQL,
Dataiku-specific APIs, and side effects. Classify as directly portable, rewrite required, or unsupported.
Never execute source code or make network calls during assessment.
