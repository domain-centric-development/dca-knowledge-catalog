---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Event Consumption Pattern
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-consumption-pattern"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-consumption-pattern). This is an evidence excerpt; retain the parent selection and caveats.

### Event Consumption Pattern

**Consuming Integration Event (from another module):**
```java
@Component
@RequiredArgsConstructor
class InventoryEventListener {
    private final ReserveStockUseCase reserveStock;

    @ApplicationModuleListener  // Spring Modulith async listener
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    void on(OrderCreatedEvent event) {
        // Anti-Corruption Layer: Convert integration event → command
        var command = new ReserveStockCommand(
            OrderId.of(event.orderId()),
            // Map to Inventory's domain language
        );

        // Execute use case in Inventory's bounded context
        reserveStock.execute(command);

        // Event marked complete in Event Publication Registry
    }
}
```

**Key Points:**
- `@ApplicationModuleListener` enables async processing in new transaction
- `Propagation.REQUIRES_NEW` ensures independent transaction
- Failures trigger automatic retry (configured via Spring Modulith)
- Anti-Corruption Layer protects consuming module's domain
