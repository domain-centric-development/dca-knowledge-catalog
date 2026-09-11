---
type: Section
title: Forbidden Dependencies
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

- ❌ Domain → Application
- ❌ Domain → Adapter
- ❌ Domain → Infrastructure
- ❌ Application → Adapter
- ❌ Application → Infrastructure
- ❌ Incoming adapter → Infrastructure (`DCA-HEX-004`)
- ❌ Outgoing adapter → *another module's* Infrastructure (`DCA-HEX-005`)
- ❌ Use Case → Controller
- ❌ Use Case → Repository Implementation
- ❌ Port → Adapter (implementation)
- ❌ Inner → Outer (never)

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
