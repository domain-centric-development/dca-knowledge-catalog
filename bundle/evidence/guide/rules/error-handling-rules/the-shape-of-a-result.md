---
type: Reference
title: ERROR HANDLING RULES — The shape of a result
tags: [reference]
evidence_for: "/guide/rules/error-handling-rules.md#the-shape-of-a-result"
---

[Full node and context](/guide/rules/error-handling-rules.md#the-shape-of-a-result). This is an evidence excerpt; retain the parent selection and caveats.

### The shape of a result

This section and the next two show the returned form; the throwing form is the one the sections above describe,
and the differences are named where they arise.

The input port returns `<Operation>Result`. When the operation can end in more than one way, the result is sealed:
one case per outcome. A success case is named for what happened (`Cancelled`, `Placed`, `Found`), a refusal case
after the refusal (`OrderNotFound`, `OrderAlreadyShipped`). The cases are nested in the result and carry ids and
figures. Not every outcome is a refusal: a reminder that was `Sent` or `AlreadySent`, a merge that `Merged` or found
`NothingToMerge`, ends in two successes, and that alone is reason enough for a sealed result. An operation with one
outcome keeps a plain result record.

```java
// order/application/cancelorder/CancelOrderResult.java
public sealed interface CancelOrderResult
        permits CancelOrderResult.Cancelled, CancelOrderResult.OrderNotFound,
                CancelOrderResult.OrderAlreadyShipped {

    record Cancelled(OrderId orderId) implements CancelOrderResult {}

    record OrderNotFound(OrderId orderId) implements CancelOrderResult, Refusal {}

    record OrderAlreadyShipped(OrderId orderId, Instant shippedAt) implements CancelOrderResult, Refusal {}
}
```

The use case returns the case it finds and turns the model's refusal into its case:

```java
// order/application/cancelorder/CancelOrderUseCase.java
@Service
@Transactional
public class CancelOrderUseCase implements CancelOrderInputPort {

    private final OrderRepository orders;
    private final DomainEventPublisher eventPublisher;

    @Override
    public CancelOrderResult execute(CancelOrderCommand command) {
        Optional<Order> found = orders.findByIdForCustomer(command.orderId(), command.customerId());
        if (found.isEmpty()) {
            return new OrderNotFound(command.orderId());                  // the application's finding
        }
        Order order = found.get();
        try {
            order.cancel();
        } catch (OrderAlreadyShippedException shipped) {                  // the model's refusal, caught once
            return new OrderAlreadyShipped(shipped.orderId(), shipped.shippedAt());
        }
        orders.save(order);
        eventPublisher.publishAndClearEvents(order);
        return new Cancelled(order.id());
    }
}
```

Thrown, the same use case returns a plain `CancelOrderResult` record, raises `OrderNotFoundException` — a use-case
exception — where this one returns `OrderNotFound`, and lets `OrderAlreadyShippedException` pass without a `catch`.
The order of the steps is the same: every refusal comes before `save`.

The adapter switches over the result, **without a `default`**. A `default` would let a new case compile and fall
into whatever the branch does; without it the compiler refuses a switch that misses a case:

```java
@PostMapping("/{orderId}/cancellation")
public ResponseEntity<?> cancel(@PathVariable UUID orderId) {
    CancelOrderCommand command = new CancelOrderCommand(new OrderId(orderId), currentCustomer());
    return switch (cancelOrder.execute(command)) {
        case Cancelled cancelled -> ResponseEntity.ok(CancellationDto.from(cancelled));
        case OrderNotFound refusal -> OrderProblems.orderNotFound(refusal.orderId());
        case OrderAlreadyShipped refusal -> OrderProblems.alreadyShipped(refusal.orderId(), refusal.shippedAt());
    };
}
```

The same in the other languages:

- **C#** needs a closed union. Until C# `union` types are released (C# 15), a library gives one: OneOf's
  `[GenerateOneOf] public sealed partial class CancelOrderResult : OneOfBase<Cancelled, OrderNotFound,
  OrderAlreadyShipped>`, the cases nested `sealed record`s, each refusal case implementing `IRefusal`, a use case that simply `return`s a case (an implicit
  conversion), and an adapter that calls `result.Match(cancelled => …, notFound => …, shipped => …)`. `Match` is
  exhaustive by arity, not by name: its functions are positional, two of the same shape can be swapped and still
  compile, and the error for a missing one names a parameter, not the case. A C# `union` closes that gap: a
  `switch` over it warns about a case it does not handle. A closed class hierarchy without either gives no
  exhaustiveness at all.
- **Rust** spells the result as an `enum` with one variant per case and the adapter as a `match` without a `_`
  arm; the `Refusal` trait says which variants refuse. `#[must_use]` on the enum turns an ignored result into a warning.
