---
type: Reference
title: RULES — THE FUNDAMENTAL DEPENDENCY RULE
tags: [reference]
evidence_for: "/guide/readme/rules.md#the-fundamental-dependency-rule"
---

[Full node and context](/guide/readme/rules.md#the-fundamental-dependency-rule). This is an evidence excerpt; retain the parent selection and caveats.

### THE FUNDAMENTAL DEPENDENCY RULE

- **All dependencies point inward toward domain**
- Domain has zero outward dependencies
- Domain knows nothing about outer layers
- Application depends only on domain
- Adapters depend on application and domain (through interfaces)
- Infrastructure depends on adapters
- Outer layers know inner layers, never reverse
- Inner layers define interfaces, outer layers implement them
