---
type: Section
title: "Domain Layer (Enterprise Business Rules)"
chapter: Elements
source: guide
resource: dca-guide/architecture/elements.md
tags: [guide, section]
---

### Tactical Building Blocks
- **Entity** - Object with identity and lifecycle
- **Value Object** - Immutable object without identity
- **Aggregate** - Transactional consistency boundary
- **Aggregate Root** - Entry point entity for aggregate access
- **Domain Service** - Stateless operation on domain objects
- **Domain Event** - Immutable record of domain occurrence (internal to bounded context)
- **Specification** - Encapsulated business rule
- **Factory** - Complex object creation logic
- **Domain Exception** - A broken business rule, named in the ubiquitous language

### Strategic Building Blocks
- **Bounded Context** - Explicit boundary for unified model
- **Ubiquitous Language** - Shared vocabulary in code and conversation
- **Subdomain** - Logical domain partition (Core, Supporting, Generic)

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)
- [Specification<T>](/marker/tactical/specification.md)
