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
| Domain exceptions | Domain — beside the model, no `exception/` package | `InsufficientStockException` |
| Input Ports | Application — the use-case package | `CreateOrderInputPort` |
| Use-case implementations | Application — the use-case package | `CreateOrderUseCase` |
| Commands, Queries, Results | Application — the use-case package | `CreateOrderCommand`, `CreateOrderResult` |
| Output Ports | Application — the use-case package, or `application/shared` when reused | `OrderRepository`, `LoginProtectionStore` |
| Expected refusals | Application — cases nested in the use case's sealed `*Result`, or use-case exceptions beside the use case; one way per context | `CancelOrderResult.OrderNotFound`, `OrderNotFoundException` |
| Use-case exceptions (extend `UseCaseException`) | Application — beside the use case, or `application/shared` when reused | `PaymentProviderUnavailableException` |
| Output-port exceptions (extend `OutputPortException`) | Application — beside the port whose contract declares them | `DuplicateOrderNumberException`, `PaymentGatewayUnavailableException` |
| Answers to result cases | `adapter/incoming` — written once per context, called from each switch (a returning context) | `OrderProblems` |
| Exception handlers | `adapter/incoming` — one per context, for what is thrown | `OrderApiExceptionHandler` |
| REST controllers | `adapter/incoming` | `OrderRestController` |
| Message listeners | `adapter/incoming` | `OrderCommandListener` |
| Persistence adapters, ORM entities | `adapter/outgoing` | `JpaOrderRepository`, `OrderEntity` |
| Event publishers, API clients | `adapter/outgoing` | `KafkaEventPublisher`, `PaymentGatewayClient` |
| Framework configuration | Infrastructure | `BeansConfiguration` |
| Composition root — wiring, a port implemented by another use case | Infrastructure — `{context}/infrastructure/` | `PricingConfiguration` |
| Process manager — executive and tracker | Application (use case) and Domain (tracker aggregate) | `BookTripUseCase`, `TripBooking` |
| Universal value objects | `sharedkernel/domain/model` | `Money`, `Address` |
| Shared application ports | `sharedkernel/application/shared` | `IdentityProvider` |

## Related mentions (heuristic)

- [OutputPortException](/marker/application/outputportexception.md)
- [UseCaseException](/marker/application/usecaseexception.md)
