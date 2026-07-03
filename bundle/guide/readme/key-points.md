---
type: Section
title: Key Points
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

**Domain-Centric Architecture** is an architectural approach that puts **domain logic at the center** and protects it from infrastructure concerns. It synthesizes proven patterns from Domain-Driven Design, Hexagonal Architecture, and Clean Architecture.

### Core Principles

1. **Dependencies Point Inward** - All code dependencies point toward the domain layer. The domain has zero outward dependencies.

2. **Domain is King** - Business logic lives in a rich domain model using tactical DDD patterns (Entities, Value Objects, Aggregates, Domain Services, Domain Events).

3. **Ports & Adapters** - Application layer defines interfaces (ports), infrastructure implements them (adapters). This inverts dependencies.

4. **Bounded Contexts** - Large systems are partitioned into bounded contexts, each with its own ubiquitous language and model.

5. **Event-Driven Integration** - Bounded contexts communicate asynchronously via domain events (internal) and integration events (external).

6. **Progressive Complexity** - Start simple with flat structures, add complexity only when needed based on actual pain points.

### Four Layers

```
Infrastructure  ─→  Frameworks, Database, Message Broker
     ↓ depends on
Adapters       ─→  Controllers, Repositories, API Clients
     ↓ depends on
Application    ─→  Use Cases, Input Ports, Output Ports
     ↓ depends on
Domain         ─→  Entities, Value Objects, Aggregates, Events
(ZERO DEPENDENCIES)
```

### Key Benefits

- ✅ **Business Logic Protection** - Domain isolated from technical concerns
- ✅ **Testability** - Domain and application layers testable without infrastructure
- ✅ **Flexibility** - Easy to swap frameworks, databases, or external services
- ✅ **Team Scaling** - Bounded contexts enable independent teams
- ✅ **Evolution** - Clear path from monolith to microservices
- ✅ **Maintainability** - Clear separation of concerns and explicit boundaries

### When to Use

**Ideal for:**
- Complex business domains with rich logic
- Systems that will evolve and scale over time
- Multiple teams working on different parts
- Event-driven or microservices architectures

**Consider alternatives for:**
- Simple CRUD applications
- Very small systems with minimal business logic
- Short-lived projects or prototypes

### Quick Start

1. **Identify bounded contexts** - Partition your domain by language and model boundaries
2. **Start with 4 layers** - domain, application, adapter, infrastructure (keep it flat initially)
3. **Apply tactical DDD** - Use Entities, Value Objects, Aggregates in domain layer
4. **Define ports** - Input Ports for use cases, Output Ports for infrastructure needs
5. **Implement adapters** - Web controllers, persistence, messaging as adapters
6. **Add complexity progressively** - Subdivide packages only when you feel pain

For detailed patterns and rules, continue reading below. For specific topics, see [Related Documentation](#related-documentation).
