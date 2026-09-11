---
type: Section
title: Where things live
chapter: Quick Reference
source: guide
resource: dca-guide/architecture/quick-reference.md
tags: [guide, section]
---

| Component | Layer | Example |
|---|---|---|
| Entities, Value Objects | Domain | `Order`, `OrderId`, `Money` |
| Domain Events | Domain | `OrderPlaced`, `OrderCancelled` |
| Domain Services | Domain | `PricingService` |
| Input Ports | Application — the use-case package | `CreateOrderInputPort` |
| Use-case implementations | Application — the use-case package | `CreateOrderUseCase` |
| Commands, Queries, Results | Application — the use-case package | `CreateOrderCommand`, `CreateOrderResult` |
| Output Ports | Application — the use-case package, or `application/shared` when reused | `OrderRepository`, `LoginProtectionStore` |
| REST controllers | `adapter/incoming` | `OrderRestController` |
| Message listeners | `adapter/incoming` | `OrderCommandListener` |
| Persistence adapters, ORM entities | `adapter/outgoing` | `JpaOrderRepository`, `OrderEntity` |
| Event publishers, API clients | `adapter/outgoing` | `KafkaEventPublisher`, `PaymentGatewayClient` |
| Framework configuration | Infrastructure | `BeansConfiguration` |
| Universal value objects | `sharedkernel/domain/model` | `Money`, `Address` |
| Shared application ports | `sharedkernel/application/shared` | `IdentityProvider` |
