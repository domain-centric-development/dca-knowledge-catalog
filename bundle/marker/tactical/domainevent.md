---
type: Marker
title: DomainEvent
category: tactical
kind: interface
signature: public interface DomainEvent
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
methods: ["UUID eventId()", "Instant occurredOn()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/DomainEvent.java
tags: [tactical, marker]
---

Interface for Domain Events.

Domain Events represent something that happened in the domain that domain experts care about.
They are internal to a bounded context and can evolve freely without versioning concerns.

**Characteristics:**

- Immutable (final classes or records)
- Named in the past tense (e.g., ProductCreated, CartCleared, PriceChanged)
- Include timestamp, unique ID, and event-specific data
- Should NOT have Spring annotations (@Component, @EventListener)
- Part of the Ubiquitous Language
- Internal to a bounded context — no versioning needed

**Use Cases:**

- Triggering side effects in other aggregates or contexts
- Enabling eventual consistency between bounded contexts
- Audit trail and event sourcing
- Decoupling bounded contexts

**Required Methods:**

- `eventId()` - Unique identifier for this event instance
- `occurredOn()` - When the event occurred

For events that cross bounded context boundaries, see `t` which adds
versioning for backward compatibility.

**Example:**

```java
public record ProductCreated(
    UUID eventId,
    ProductId productId,
    Instant occurredOn) implements DomainEvent {

  public static ProductCreated now(ProductId productId) {
    return new ProductCreated(UUID.randomUUID(), productId, Instant.now());
  }
}
```

**References:**

- Eric Evans' Domain-Driven Design (2003)
- Vaughn Vernon's Implementing Domain-Driven Design (2013), Chapter 8: "Domain Events"

## Governed by

- [Domain Events must have a timestamp field](/rule/advanced/domain-events-must-have-a-timestamp-field.md)
- [Domain Events must implement DomainEvent Marker Interface and be records](/rule/advanced/domain-events-must-implement-domainevent-marker-interface-and-be-records.md)
- [Domain Events must not have Spring annotations](/rule/advanced/domain-events-must-not-have-spring-annotations.md)
- [Domain Events must reside in domain package](/rule/advanced/domain-events-must-reside-in-domain-package.md)
- [Domain Events should be immutable (final or records)](/rule/advanced/domain-events-should-be-immutable-final-or-records.md)
- [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
