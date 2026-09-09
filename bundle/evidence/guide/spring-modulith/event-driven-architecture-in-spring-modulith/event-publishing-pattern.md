---
type: Reference
title: Event-Driven Architecture in Spring Modulith — Event Publishing Pattern
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-publishing-pattern"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-publishing-pattern). This is an evidence excerpt; retain the parent selection and caveats.

### Event Publishing Pattern

**Publishing Domain Event (internal):**
```java
@Service
@RequiredArgsConstructor
public class CreateOrderUseCase {
    private final ApplicationEventPublisher events;
    private final OrderRepository orders;

    @Transactional
    public OrderId execute(CreateOrderCommand command) {
        // 1. Create aggregate
        Order order = Order.create(command);

        // 2. Save aggregate
        orders.save(order);

        // 3. Publish domain event (same transaction)
        events.publishEvent(new OrderCreated(
            order.getId(),
            order.getCustomerId(),
            order.getTotalAmount(),
            Instant.now()
        ));

        return order.getId();
    }
}
```

**Converting to Integration Event (cross-module):**
```java
// Listening to domain event and publishing integration event
@Component
@RequiredArgsConstructor
class OrderEventPublisher {
    private final ApplicationEventPublisher events;

    @EventListener
    void on(OrderCreated event) {
        // Map domain event → integration event
        events.publishEvent(new OrderCreatedEvent(
            UUID.randomUUID().toString(),
            event.orderId().toString(),
            event.customerId().toString(),
            event.totalAmount().getAmount(),
            event.occurredAt(),
            "v1"  // Version for compatibility
        ));
        // Integration event persisted by Event Publication Registry
    }
}
```
