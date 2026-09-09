---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Idempotent Consumers
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#idempotent-consumers"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#idempotent-consumers). This is an evidence excerpt; retain the parent selection and caveats.

### Idempotent Consumers

At-least-once delivery means every listener must expect duplicates and out-of-order arrival:

```java
@ApplicationModuleListener
void on(OrderCreatedEvent event) {
    if (processedEvents.contains(event.eventId())) {
        return; // Duplicate delivery — already handled
    }
    reserveStock.execute(toCommand(event));
    processedEvents.markProcessed(event.eventId());
}
```

**Rules:**
- **Deduplicate** — track processed event IDs in the consumer's own store, or make the operation naturally idempotent (e.g., `reserveStock(orderId)` upserts the reservation instead of inserting a new one)
- **Tolerate out-of-order arrival** — never assume the previous event was already seen
- **Never drop silently** — permanently failing events go to a dead-letter mechanism (e.g., alert plus manual resubmission of incomplete publications after retries are exhausted)
