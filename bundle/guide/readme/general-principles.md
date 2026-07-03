---
type: Section
title: GENERAL PRINCIPLES
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

- **Domain First** - Domain is the heart, everything serves it
- **Dependency Inversion** - Depend on abstractions, not concretions
- **Separation of Concerns** - Each layer has single responsibility
- **Framework Independence** - Domain and application know no framework
- **Database Independence** - Domain knows no persistence
- **UI Independence** - Domain knows no presentation
- **Testability** - Test domain without infrastructure
- **Replaceability** - Swap adapters without changing domain
- **Screaming Architecture** - Use cases are visible
- **Ubiquitous Language** - Domain terms everywhere
- **Bounded Contexts** - Explicit boundaries
- **Small Aggregates** - Minimal transactional boundaries
- **Eventual Consistency** - Between aggregates and contexts
- **Interface Segregation** - Small, focused ports
- **Immutability** - Value objects and events are immutable
- **Protection** - Protect domain from external changes
- **Delay Decisions** - Defer infrastructure choices
- **Business Focus** - Code reflects business, not technology
