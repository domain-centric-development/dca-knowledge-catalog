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

- [Domain Events must have a timestamp field](/rule/advanced/domain-events-must-have-a-timestamp-field.md)
- [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)
- [Integration Events must be annotated with IntegrationEventType](/rule/advanced/integration-events-must-be-annotated-with-integrationeventtype.md)
- [Integration Events must not have a version field](/rule/advanced/integration-events-must-not-have-a-version-field.md)
- [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/integration-events-must-be-in-events-or-adapter-outgoing-event-packages.md)
- [Integration Events should be immutable records](/rule/strategic/integration-events-should-be-immutable-records.md)

## Discussed in

- [Service Decomposition](/guide/deployment-patterns/service-decomposition.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
