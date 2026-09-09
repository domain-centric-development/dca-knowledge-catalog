---
type: Marker
title: "AggregateRoot<T, ID>"
category: tactical
kind: interface
signature: "public interface AggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> extends Entity<T, ID>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
generics: "T extends AggregateRoot<T, ID>, ID extends Id"
extends: [Entity]
methods: ["List<DomainEvent> domainEvents()", "void clearDomainEvents()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/AggregateRoot.java
tags: [tactical, marker]
---

Marker interface for Aggregate Roots.

An aggregate root is the entry point to an aggregate - a cluster of domain objects that are
treated as a single unit. The aggregate root is responsible for maintaining invariants within the
aggregate and collecting domain events that occur during state changes.

**Domain Events:**

Aggregate roots collect domain events when state changes occur. These events are published
after the aggregate is persisted, enabling eventual consistency and loose coupling between
aggregates and bounded contexts.

**Usage Pattern:**

```java
// 1. Aggregate performs business operation and raises event
product.changePrice(newPrice);

// 2. Repository saves aggregate
productRepository.save(product);

// 3. Use case publishes and clears the events, still inside the transaction
eventPublisher.publishAndClearEvents(product);
```

Publishing and clearing is one step, `DomainEventPublisher.publishAndClearEvents`: the
publisher dispatches every collected event and clears the aggregate only once every listener
returned. Iterating `domainEvents()` and calling `publish` per event leaves the
clearing to the caller and is not the sanctioned form.

## Extends

- [Entity<T, ID>](/marker/tactical/entity.md)

## Governed by

- [Aggregate Roots must not have fields with other Aggregate Root types](/rule/tactical/dca-tac-003.md)

## Related mentions in guides (heuristic)

- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [RULES](/guide/readme/rules.md)
