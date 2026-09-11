---
type: Marker
title: Factory
category: tactical
kind: interface
signature: public interface Factory
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Factory.java
tags: [tactical, marker]
---

Marker interface for Factories.

Factories encapsulate complex object creation logic, particularly for Aggregates and Entities.
They ensure invariants are maintained from the moment of creation and hide complex construction
details.

**When to Use:**

- Object construction is complex and involves multiple steps
- Creation requires knowledge not belonging to the object itself
- The constructor would violate the object's invariants
- Need to create different configurations of the same type

**Characteristics:**

- Stateless or with minimal state
- Return fully formed, valid objects
- Carries no container stereotype - a factory is a domain object
- Part of the domain model

**Example:**

```java
public class ProductFactory implements Factory {
  public Product createProduct(ProductName name, SKU sku, Price price) {
    // Complex construction logic and validation
    return new Product(...);
  }
}
```

**Alternative:** For simple cases, static factory methods on the domain object itself
(e.g., `Product.of(...)`) are preferred over separate Factory classes.

**Reference:** Eric Evans' Domain-Driven Design (2003), Chapter 6: "The Life Cycle of a
Domain Object"

## Related mentions in guides (heuristic)

- [Factory for Cross-Context Assembly](/guide/integration-patterns/factory-for-cross-context-assembly.md)
