---
type: Reference
title: RULES — PACKAGING RULES
tags: [reference]
evidence_for: "/guide/readme/rules.md#packaging-rules"
---

[Full node and context](/guide/readme/rules.md#packaging-rules). This is an evidence excerpt; retain the parent selection and caveats.

### PACKAGING RULES

- Package by bounded context, then by layer; inside the application layer by use case — optionally grouped into
  features (see [Grouping use cases into features](#grouping-use-cases-into-features))
- Layer separation enforced by module structure
- Domain module has zero external dependencies
- Application module depends only on domain
- Adapter modules depend on application
- Infrastructure module depends on adapters
- Modules can be independently deployed

> **Note:** For Spring Modulith module organization, see [Spring Modulith Implementation](/guide/spring-modulith.md)
