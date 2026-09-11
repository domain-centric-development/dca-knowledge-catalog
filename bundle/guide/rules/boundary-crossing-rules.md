---
type: Section
title: BOUNDARY CROSSING RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

- Data crosses boundaries as simple DTOs
- DTOs have no business logic
- DTOs have no dependencies
- Never pass entities across boundaries
- Never pass value objects across boundaries (convert to DTOs)
- Domain events can cross boundaries (as DTOs)
- Dependencies point inward at boundaries
- Control flow can go any direction
- Use Dependency Inversion when control flow goes outward
