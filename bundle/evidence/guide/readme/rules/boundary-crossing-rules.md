---
type: Reference
title: RULES — BOUNDARY CROSSING RULES
tags: [reference]
evidence_for: "/guide/readme/rules.md#boundary-crossing-rules"
---

[Full node and context](/guide/readme/rules.md#boundary-crossing-rules). This is an evidence excerpt; retain the parent selection and caveats.

### BOUNDARY CROSSING RULES

- Data crosses boundaries as simple DTOs
- DTOs have no business logic
- DTOs have no dependencies
- Never pass entities across boundaries
- Never pass value objects across boundaries (convert to DTOs)
- Domain events can cross boundaries (as DTOs)
- Dependencies point inward at boundaries
- Control flow can go any direction
- Use Dependency Inversion when control flow goes outward
