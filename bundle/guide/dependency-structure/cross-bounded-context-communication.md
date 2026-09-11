---
type: Section
title: Cross-Bounded Context Communication
chapter: Dependency Structure
source: guide
resource: dca-guide/architecture/dependency-structure.md
tags: [guide, section]
---

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

## Related mentions (heuristic)

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
