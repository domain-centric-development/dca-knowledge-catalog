---
type: Section
title: THE FUNDAMENTAL DEPENDENCY RULE
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

- **All dependencies point inward toward domain**
- Domain has zero outward dependencies
- Domain knows nothing about outer layers
- Application depends only on domain
- Adapters depend on application and domain (through interfaces)
- Infrastructure depends on adapters
- Outer layers know inner layers, never reverse
- Inner layers define interfaces, outer layers implement them
