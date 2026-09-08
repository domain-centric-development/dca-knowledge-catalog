---
type: Marker
title: "BaseAggregateRoot<T, ID>"
category: tactical
kind: class
signature: "public abstract class BaseAggregateRoot<T extends AggregateRoot<T, ID>, ID extends Id> implements AggregateRoot<T, ID>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
generics: "T extends AggregateRoot<T, ID>, ID extends Id"
modifiers: [public, abstract]
extends: [AggregateRoot]
methods: ["public void registerEvent(DomainEvent event)", "public List<DomainEvent> domainEvents()", "public void clearDomainEvents()"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/BaseAggregateRoot.java
tags: [tactical, marker]
---

Abstract base class for Aggregate Roots providing domain event collection.

This class provides a reusable implementation of domain event collection that aggregate roots
can use by extending this class. It handles the storage and management of domain events that
occur during aggregate state changes.

**Usage:**

```java
public final class Product extends BaseAggregateRoot<Product, ProductId> {
  // ... fields

  public void changePrice(Price newPrice) {
    Price oldPrice = this.price;
    this.price = newPrice;

    // Raise domain event
    registerEvent(new ProductPriceChanged(this.id, oldPrice, newPrice));
  }
}
```

## Extends

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
