---
type: Section
title: Allowed Dependencies
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

- ✅ Infrastructure → Adapter
- ✅ Adapter → Application
- ✅ Application → Domain
- ✅ Adapter → Port (interface)
- ✅ Outgoing adapter → global and own-module Infrastructure
- ✅ Use Case → Domain
- ✅ Use Case → Output Port (interface)
- ✅ Controller → Input Port (interface)
- ✅ Outer → Inner (always)
