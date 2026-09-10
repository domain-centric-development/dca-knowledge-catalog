---
type: Reference
title: "Event-Driven Architecture in Spring Modulith — Event Mapper Pattern (Domain Event → Integration Event)"
tags: [reference]
evidence_for: "/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-mapper-pattern-domain-event--integration-event"
---

[Full node and context](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md#event-mapper-pattern-domain-event--integration-event). This is an evidence excerpt; retain the parent selection and caveats.

### Event Mapper Pattern (Domain Event → Integration Event)

The **Event Mapper** is the outbound equivalent of ACL - it translates internal domain events into external integration events.

**Structure:**
```
Producing Module (Order):
│
├── domain/event/
│   └── OrderCreated.java             ← Internal domain event
│
├── adapter/outgoing/messaging/
│   └── OrderEventMapper.java         ← Event Mapper
│
└── events/ (published)
    └── OrderCreatedEvent.java        ← External integration event
```

**Example:**

```java
// Internal Domain Event (Order's domain language)
package com.company.ecommerce.order.domain.event;

public record OrderCreated(
    OrderId orderId,                   // Domain value object
    CustomerId customerId,             // Domain value object
    List<OrderLine> orderLines,        // Domain entities
    Money totalAmount,                 // Domain value object
    Instant occurredAt
) implements DomainEvent {}

// Event Mapper (Adapter)
package com.company.ecommerce.order.adapter.outgoing.messaging;

@Component
@RequiredArgsConstructor
public class OrderEventMapper {

    private final ApplicationEventPublisher events;

    @EventListener  // Listen to internal domain event
    public void on(OrderCreated domainEvent) {

        // Map domain event → integration event (DTO)
        OrderCreatedEvent integrationEvent = toIntegrationEvent(domainEvent);

        // Publish integration event (persisted by Event Publication Registry)
        events.publishEvent(integrationEvent);
    }

    private OrderCreatedEvent toIntegrationEvent(OrderCreated domainEvent) {
        return new OrderCreatedEvent(
            UUID.randomUUID().toString(),         // Event ID for idempotency
            domainEvent.orderId().getValue(),     // Extract primitive from value object
            domainEvent.customerId().getValue(),  // Extract primitive from value object
            toOrderItemDtos(domainEvent.orderLines()),  // Map to DTOs
            domainEvent.totalAmount().getAmount(),
            domainEvent.totalAmount().getCurrency().getCurrencyCode(),
            domainEvent.occurredAt(),
            "v1"  // Version for compatibility
        );
    }

    private List<OrderItemDto> toOrderItemDtos(List<OrderLine> orderLines) {
        return orderLines.stream()
            .map(line -> new OrderItemDto(
                line.getProductId().getValue(),
                line.getQuantity(),
                line.getPrice().getAmount()
            ))
            .toList();
    }
}

// External Integration Event (Published DTO)
package com.company.ecommerce.order.events;

public record OrderCreatedEvent(
    String eventId,
    String orderId,
    String customerId,
    List<OrderItemDto> items,
    BigDecimal totalAmount,
    String currency,
    Instant timestamp,
    String version
) implements org.springframework.modulith.events.Externalized {}
```

**Key Principles:**

1. **Domain events stay internal** - Never cross module boundaries
2. **Integration events are DTOs** - Serializable, versioned, primitive types
3. **Event Mapper translates** - Domain language → External DTO
4. **Two-step publishing** - Domain event → Event Mapper → Integration event
