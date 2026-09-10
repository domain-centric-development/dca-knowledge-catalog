---
type: Reference
title: "ELEMENTS — Domain Layer (Enterprise Business Rules)"
tags: [reference]
evidence_for: "/guide/readme/elements.md#domain-layer-enterprise-business-rules"
---

[Full node and context](/guide/readme/elements.md#domain-layer-enterprise-business-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Domain Layer (Enterprise Business Rules)

#### Tactical Building Blocks
- **Entity** - Object with identity and lifecycle
- **Value Object** - Immutable object without identity
- **Aggregate** - Transactional consistency boundary
- **Aggregate Root** - Entry point entity for aggregate access
- **Domain Service** - Stateless operation on domain objects
- **Domain Event** - Immutable record of domain occurrence (internal to bounded context)
- **Specification** - Encapsulated business rule
- **Factory** - Complex object creation logic

#### Strategic Building Blocks
- **Bounded Context** - Explicit boundary for unified model
- **Ubiquitous Language** - Shared vocabulary in code and conversation
- **Subdomain** - Logical domain partition (Core, Supporting, Generic)
