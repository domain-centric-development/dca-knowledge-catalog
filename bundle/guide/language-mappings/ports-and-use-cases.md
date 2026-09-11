---
type: Section
title: Ports and Use Cases
chapter: "Language Mappings: Java/Spring ↔ C#/.NET"
source: guide
resource: dca-guide/topics/language-mappings.md
tags: [guide, section]
---

Java package `hexagonal.port.in` / `.out`, .NET namespace `Hexagonal.Ports.In` / `.Out`. **.NET ports are
async only** — there is no synchronous twin — while the domain layer stays synchronous (a `DCA-NET` rule
enforces both).

| Concept | Java | C# |
|---|---|---|
| Input port marker | `InputPort` | `IInputPort` |
| Use case contract | `UseCase<INPUT, OUTPUT>` — `OUTPUT execute(INPUT)` | `IUseCase<TInput, TOutput>` — `Task<TOutput> ExecuteAsync(TInput, CancellationToken)` |
| Use case input port | `PlaceOrderInputPort extends UseCase<PlaceOrderCommand, PlaceOrderResult>` | `IPlaceOrderInputPort : IUseCase<PlaceOrderCommand, PlaceOrderResult>` |
| Use case implementation | `PlaceOrderUseCase implements PlaceOrderInputPort` (`@Service`) | `PlaceOrderUseCase : IPlaceOrderInputPort` (plain class, registered in DI) |
| Command / Query / Result | `record` | `sealed record` |
| Output port marker | `OutputPort` | `IOutputPort` |
| Repository | `Repository<T, ID>` — `findById`, `save`, `deleteById` | `IRepository<TAggregate, TId>` — `FindByIdAsync`, `SaveAsync`, `DeleteByIdAsync` |
| Store | `Store` | `IStore` |
| Domain event publisher | `DomainEventPublisher` — `publish`, `publishAndClearEvents` | `IDomainEventPublisher` — `PublishAsync`, `PublishAndClearEventsAsync` |
| Integration event publisher | `IntegrationEventPublisher` | `IIntegrationEventPublisher` — `PublishAsync` |
| Transaction boundary | `application.TransactionBoundary` — `inTransaction(Supplier<T>)` | `Application.Transactions.ITransactionBoundary` — `InTransactionAsync<T>(Func<Task<T>>)` |
| Context-specific output port | `OrderRepository extends Repository<Order, OrderId>` in `application/shared/` | `IOrderRepository : IRepository<Order, OrderId>` in `Application/Shared/` |

```java
// order/application/placeorder/
public interface PlaceOrderInputPort extends UseCase<PlaceOrderCommand, PlaceOrderResult> {}
public record PlaceOrderCommand(CustomerId customerId, List<LineItemData> items) {}
public record PlaceOrderResult(OrderId orderId, OrderStatus status) {}
```

```csharp
// Order/Application/PlaceOrder/
public interface IPlaceOrderInputPort : IUseCase<PlaceOrderCommand, PlaceOrderResult> { }
public sealed record PlaceOrderCommand(CustomerId CustomerId, IReadOnlyList<LineItemData> Items);
public sealed record PlaceOrderResult(OrderId OrderId, OrderStatus Status);
```

## Related mentions (heuristic)

- [TransactionBoundary](/marker/application/transactionboundary.md)
- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [IntegrationEventPublisher](/marker/port-out/integrationeventpublisher.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
