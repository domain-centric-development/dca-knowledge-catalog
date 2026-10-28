---
type: Section
title: INFRASTRUCTURE LAYER RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

- Framework code stays in infrastructure
- Infrastructure is a detail
- Database is a detail
- Web framework is a detail
- Infrastructure decisions can be delayed
- Infrastructure can be swapped
- No business logic in infrastructure
- The composition root wires and never decides: it creates the adapters, hands each use case its ports and holds no
  rule (see [The composition root](/guide/dependency-structure/the-composition-root.md))
