---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Best Practices
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#best-practices"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#best-practices). This is an evidence excerpt; retain the parent selection and caveats.

### Best Practices

**When to Use Domain Events:**
- Communication within the same module
- Eventual consistency between aggregates in same bounded context
- Triggering side effects in same transaction

**When to Use Integration Events:**
- Communication between different modules (bounded contexts)
- Cross-team integration points
- Events that may be externalized to message broker later
- When guaranteed delivery and retry are needed

**Naming Conventions:**
- Domain Events: Past tense, no suffix (e.g., `OrderCreated`, `PaymentProcessed`)
- Integration Events: Past tense + "Event" suffix (e.g., `OrderCreatedEvent`, `PaymentProcessedEvent`)
