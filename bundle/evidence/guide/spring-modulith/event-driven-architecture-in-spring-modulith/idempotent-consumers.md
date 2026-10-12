---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Idempotent Consumers
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#idempotent-consumers"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#idempotent-consumers). This is an evidence excerpt; retain the parent selection and caveats.

### Idempotent Consumers

At-least-once delivery means every listener must expect duplicates and out-of-order arrival. A duplicate is
recognised **per effect**: two listeners of one module may react to the same event, and each has to do its work
exactly once — so the record of what was processed is keyed by the effect *and* the event id, never by the event id
alone. And the record is written **in the same transaction as the effect**: marked after it, a crash in between
replays the effect; marked before it, a crash loses it. The use case does both, the listener hands it the event id:

```java
@ApplicationModuleListener
void on(OrderCreatedEvent event) {
    reserveStock.execute(new ReserveStockCommand(event.eventId(), event.orderId(), event.lines()));
}
```

```java
public final class ReserveStockUseCase implements ReserveStockInputPort {

    private static final String EFFECT = "reserve-stock";     // stable: a rename must not replay old events

    @Override
    public ReserveStockResult execute(final ReserveStockCommand command) {
        return transactionBoundary.execute(() -> {
            if (processedEvents.contains(EFFECT, command.eventId())) {
                return ReserveStockResult.alreadyReserved();   // duplicate delivery — this effect happened
            }
            final Stock stock = stockRepository.findByProduct(command.productId()).orElseThrow();
            stock.reserve(command.orderId(), command.quantity());
            stockRepository.save(stock);
            processedEvents.markProcessed(EFFECT, command.eventId());
            return ReserveStockResult.reserved();
        });
    }
}
```

`ProcessedEvents` is a `Store` of the consuming module (`application/shared`), its adapter in the module's own
persistence — so the mark and the effect share one transaction where the store is transactional.

**Rules:**
- **Deduplicate per effect** — track processed event IDs keyed by the effect, in the consumer's own store and the effect's transaction, or make the operation naturally idempotent (e.g., `reserveStock(orderId)` upserts the reservation instead of inserting a new one)
- **Tolerate out-of-order arrival** — never assume the previous event was already seen
- **Never drop silently** — permanently failing events go to a dead-letter mechanism (e.g., alert plus manual resubmission of incomplete publications after retries are exhausted)
