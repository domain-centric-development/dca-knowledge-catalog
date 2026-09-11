---
type: Section
title: High-Level Structure Overview
chapter: Java Package Structure
source: guide
resource: dca-guide/architecture/package-structure.md
tags: [guide, section]
---

```
com.company.project/
│
├── {boundedcontext}/
│   │
│   ├── domain/              [CORE LAYER]
│   │                        Pure business logic with zero dependencies
│   │                        Entities, Value Objects, Aggregates, Domain Services, Domain Events
│   │
│   ├── application/         [USE CASE LAYER]
│   │                        Orchestrates domain objects and defines boundaries
│   │                        Input Ports, Output Ports, Use Cases, Commands, Queries, DTOs
│   │
│   ├── adapter/             [INFRASTRUCTURE INTERFACE LAYER]
│   │                        Connects application to external world
│   │   ├── incoming/        Controllers, Event Consumers, CLI (call Input Ports)
│   │   └── outgoing/        Repository Impl, API Clients, Publishers (implement Output Ports)
│   │
│   └── infrastructure/      [FRAMEWORKS & DRIVERS LAYER]
│                            Framework-specific configuration and cross-cutting concerns
│                            Spring, JPA, Kafka config, Logging, Security
│
├── sharedkernel/            [SHARED ACROSS ALL CONTEXTS - Keep Minimal]
│   ├── application/shared/  Application-specific ports shared by several contexts (IdentityProvider)
│   ├── domain/model/        Universal value objects (Money, Address, etc.)
│   └── adapter/outgoing/    Shared adapters only where no library ships them (Spring: dca-spring does)
│
└── infrastructure/          [GLOBAL INFRASTRUCTURE]
                             Application-wide configuration and setup

Architectural markers (AggregateRoot, UseCase, Repository, @BoundedContext, …) are not part of
the application: they come from the dca-building-blocks dependency (see Shared Kernel Pattern).
```

## Related mentions (heuristic)

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
