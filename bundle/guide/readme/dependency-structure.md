---
type: Section
title: DEPENDENCY STRUCTURE
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

### Layer Dependency Flow

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

### Request Flow with Dependency Inversion

```
HTTP Request
    ↓
┌──────────────────────────────────────────┐
│ Spring Controller (infrastructure)       │
└──────────────────────────────────────────┘
    ↓ delegates to
┌──────────────────────────────────────────┐
│ OrderController (adapter)                │
│ - validates HTTP input                   │
│ - creates CreateOrderCommand (DTO)       │
└──────────────────────────────────────────┘
    ↓ calls (depends on interface)
┌──────────────────────────────────────────┐
│ CreateOrderInputPort (application)       │ ← Interface
└──────────────────────────────────────────┘
    ↑ implemented by
┌──────────────────────────────────────────┐
│ CreateOrderUseCase (application)         │
│ - converts DTO → Domain                  │
│ - calls Order.create()                   │
│ - validates business rules               │
│ - calls repository.save()                │
│ - publishes domain events                │
│ - converts Domain → DTO                  │
└──────────────────────────────────────────┘
    │                           │
    │ uses                      │ calls
    ↓                           ↓
┌─────────────────┐    ┌──────────────────┐
│ Order           │    │ OrderRepository  │ ← Interface (application)
│ (Aggregate)     │    │ (Output Port)    │
│ (domain)        │    └──────────────────┘
│                 │            ↑ implemented by
│ - OrderLine     │    ┌──────────────────────────┐
│ - Money         │    │ OrderRepositoryAdapter   │
│ - OrderId       │    │ (adapter)                │
└─────────────────┘    │ - maps Domain ↔ JPA      │
                       │ - uses Spring Data       │
                       └──────────────────────────┘
                               ↓ uses
                       ┌──────────────────────────┐
                       │ OrderJpaEntity           │
                       │ (adapter)                │
                       └──────────────────────────┘
                               ↓
                       ┌──────────────────────────┐
                       │ Spring Data JPA          │
                       │ (infrastructure)         │
                       └──────────────────────────┘
                               ↓
                           Database
```

### Cross-Bounded Context Communication

```
Order Context                                     Inventory Context
┌───────────────────────┐                        ┌─────────────────────┐
│ CreateOrderUseCase    │                        │ ReserveStockUseCase │
│ (application)         │                        │ (application)       │
└───────────┬───────────┘                        └──────────┬──────────┘
            │ publishes                                     ↑ calls
            ↓                                               │
┌───────────────────────┐                                   │
│ OrderCreated          │                                   │
│ (domain event)        │                                   │
└───────────┬───────────┘                                   │
            │ via DomainEventPublisher                      │
            ↓                                               │
┌───────────────────────┐                                   │
│ OrderEventMapper      │                                   │
│ (adapter/outgoing)    │                                   │
└───────────┬───────────┘                                   │
            │ converts to DTO                               │
            ↓                                               │
┌───────────────────────┐                                   │
│ OrderCreatedEvent     │                                   │
│ (integration event)   │                                   │
└───────────┬───────────┘                                   │
            │                                               │
            └────────→ Message Broker ─────────┐            │
                      (Kafka/RabbitMQ)         │            │
                                               │            │
                                               ↓            │
                          ┌─────────────────────────────────┐
                          │ OrderEventConsumer              │
                          │ (adapter/incoming)              │
                          └──────────┬──────────────────────┘
                                     │ via ACL
                                     ↓
                          ┌─────────────────────────────────┐
                          │ ExternalEventToCommandMapper    │
                          │ (Anti-Corruption Layer)         │
                          │ converts to ReserveStockCommand │
                          └─────────────────────────────────┘
                                     │
                          ┌──────────┘
                          │
                          ↓
                    ┌────────────────────┐
                    │ ReserveStockInput  │
                    │ Port (application) │
                    └────────────────────┘
```

### Complete Cross-Context Event Flow

(Event flow diagram included - see original document for full details)

### Allowed Dependencies

- ✅ Infrastructure → Adapter
- ✅ Adapter → Application
- ✅ Application → Domain
- ✅ Adapter → Port (interface)
- ✅ Use Case → Domain
- ✅ Use Case → Output Port (interface)
- ✅ Controller → Input Port (interface)
- ✅ Outer → Inner (always)

### Forbidden Dependencies

- ❌ Domain → Application
- ❌ Domain → Adapter
- ❌ Domain → Infrastructure
- ❌ Application → Adapter
- ❌ Application → Infrastructure
- ❌ Adapter → Infrastructure
- ❌ Use Case → Controller
- ❌ Use Case → Repository Implementation
- ❌ Port → Adapter (implementation)
- ❌ Inner → Outer (never)

## Related markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
