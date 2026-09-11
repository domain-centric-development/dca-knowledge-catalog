---
type: Section
title: Layer Dependency Flow
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

```
┌─────────────────────────────────────────────────────┐
│  INFRASTRUCTURE                                     │
│  - Spring Boot, JPA, Kafka, Configuration           │
│  - Glue code only, no business logic                │
└────────────────────┬────────────────────────────────┘
                     │ depends on
                     ↓
┌─────────────────────────────────────────────────────┐
│  ADAPTER                                            │
│                                                     │
│  Input Adapters          Output Adapters            │
│  - Controllers           - Repository Impl          │
│  - Event Consumers       - API Clients              │
│  - CLI Handlers          - Event Publishers         │
│                          - Presenters               │
└────────────────────┬────────────────────────────────┘
                     │ depends on
                     ↓
┌─────────────────────────────────────────────────────┐
│  APPLICATION                                        │
│                                                     │
│  Input Ports ← Use Cases → Output Ports             │
│  (interfaces)  (implementations)  (interfaces)      │
│                                                     │
│  - CreateOrderInputPort  - OrderRepository          │
│  - CreateOrderUseCase    - PaymentGateway           │
│  - DTOs                  - EventPublisher           │
└────────────────────┬────────────────────────────────┘
                     │ depends on
                     ↓
┌─────────────────────────────────────────────────────┐
│  DOMAIN                                             │
│                                                     │
│  - Entities (Order, OrderLine)                      │
│  - Value Objects (Money, OrderId)                   │
│  - Aggregates (Order = Aggregate Root)              │
│  - Domain Services (PricingService)                 │
│  - Domain Events (OrderCreated)                     │
│  - Specifications                                   │
│                                                     │
│  ZERO DEPENDENCIES                                  │
└─────────────────────────────────────────────────────┘
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
