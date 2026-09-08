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
- Should NOT have Spring annotations (@Component, @Service)
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

## Governed by

- [Factories must not have Spring annotations](/rule/advanced/factories-must-not-have-spring-annotations.md)
- [Factories must reside in domain package](/rule/advanced/factories-must-reside-in-domain-package.md)
- [Factories should be stateless (only final fields for dependencies)](/rule/advanced/factories-should-be-stateless-only-final-fields-for-dependencies.md)
- [Factories should implement Factory Marker Interface](/rule/advanced/factories-should-implement-factory-marker-interface.md)
- [Domain classes must not use technical suffixes (Manager, Helper, Util, Impl, Implementation)](/rule/naming/domain-classes-must-not-use-technical-suffixes-manager-helper-util-impl-implementation.md)
- [Enriched Domain Models must be Value Object records](/rule/tactical/enriched-domain-models-must-be-value-object-records.md)

## Discussed in

- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
