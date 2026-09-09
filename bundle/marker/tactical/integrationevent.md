---
type: Marker
title: IntegrationEvent
category: tactical
kind: interface
signature: public interface IntegrationEvent
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
methods: ["UUID eventId()", "Instant occurredOn()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/IntegrationEvent.java
tags: [tactical, marker]
---

Marker interface for Integration Events — adapter-layer DTOs published across bounded contexts.

Integration Events are **not** domain events. They are adapter-layer data transfer objects
created when an outgoing event adapter consumes an internal `t` and publishes a
cross-context representation. This separation acts as an Anti-Corruption Layer (ACL) between the
publishing context's domain model and external consumers.

**Key Differences from Domain Events:**

- **Layer:** Adapter layer (`adapter.outgoing.event`), not domain layer
- **Purpose:** Cross bounded context communication (domain events are internal)
- **Versioning:** Strict backward compatibility required (domain events can change
freely). The schema version is a **class property**, declared via `e`, never a data field on the event instance.
- **Naming:** Suffixed with `Event` (e.g., `CartCheckedOutEvent`), while
domain events have no suffix (e.g., `CartCheckedOut`)
- **Creation:** Created by outgoing event adapters via `from(DomainEvent)` factory
methods
- **Consumption:** Consumed by incoming event adapters in other contexts

**Event Flow:**

```java
Aggregate raises DomainEvent
  → Outgoing EventPublisher adapter listens
    → Creates IntegrationEvent via from() factory
      → Publishes IntegrationEvent
        → Incoming EventConsumer in other context receives it
```

**Example — Integration Event (adapter layer):**

```java
// In cart/adapter/outgoing/event/
&#64;IntegrationEventType(name = "cart-checked-out", version = 1)
public record CartCheckedOutEvent(
    UUID eventId,
    CartId cartId,
    CustomerId customerId,
    Money totalAmount,
    int itemCount,
    List<ItemInfo> items,
    Instant occurredOn) implements IntegrationEvent {

  public record ItemInfo(ProductId productId, int quantity) {}

  public static CartCheckedOutEvent from(CartCheckedOut domainEvent) {
    List<ItemInfo> items = domainEvent.items().stream()
        .map(i -> new ItemInfo(i.productId(), i.quantity()))
        .toList();
    return new CartCheckedOutEvent(
        domainEvent.eventId(), domainEvent.cartId(), ...items, domainEvent.occurredOn());
  }
}
```

**Example — Outgoing Event Publisher (adapter):**

```java
&#64;Component
public class CartCheckedOutEventPublisher {
  private final ApplicationEventPublisher publisher;

  &#64;EventListener
  public void on(CartCheckedOut domainEvent) {
    publisher.publishEvent(CartCheckedOutEvent.from(domainEvent));
  }
}
```

## Governed by

- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/dca-adv-005.md)
- [Integration events carry the schema version in their type metadata, not in the payload](/rule/advanced/dca-adv-006.md)

## Related mentions in guides (heuristic)

- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [References & Further Reading](/guide/readme/references-further-reading.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
