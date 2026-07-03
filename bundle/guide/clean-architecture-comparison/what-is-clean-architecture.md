---
type: Section
title: What is Clean Architecture?
chapter: Domain-Centric Architecture vs Clean Architecture
source: guide
resource: implementing-domain-centric-architecture/clean-architecture-comparison.md
tags: [guide, section]
---

**Clean Architecture**, introduced by Robert C. Martin ("Uncle Bob"), is an architectural pattern that emphasizes:

1. **Independence** - Business logic independent of frameworks, UI, database
2. **Testability** - Core logic testable without external dependencies
3. **Flexibility** - Easy to change UI, database, or framework
4. **Separation of Concerns** - Clear boundaries between layers

### Clean Architecture Layers

```
┌─────────────────────────────────────────────┐
│  Frameworks & Drivers (outermost)           │
│  - Web, UI, Database, External Interfaces   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Interface Adapters                         │
│  - Controllers, Gateways, Presenters        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Application Business Rules                 │
│  - Use Cases, Interactors                   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Enterprise Business Rules (innermost)      │
│  - Entities                                 │
└─────────────────────────────────────────────┘
```

**Key Principle:** Dependencies point inward. Inner layers know nothing about outer layers.
