---
type: Marker
title: "Specification<T>"
category: tactical
kind: interface
signature: "public interface Specification<T>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
generics: T
methods: ["boolean isSatisfiedBy(T candidate)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Specification.java
tags: [tactical, marker]
---

Marker interface for Specifications.

Specifications express business rules as first-class objects. They test whether an object
satisfies certain criteria and can be combined to create complex business rules.

**Use Cases:**

- Validating whether an object meets certain criteria
- Selecting objects from a collection
- Specifying how to create objects that fulfill requirements

**Characteristics:**

- Immutable value objects
- Combinable (AND, OR, NOT operations)
- Express business rules in the Ubiquitous Language
- Should NOT have Spring annotations
- Part of the domain model

**Example:**

```java
public final class ProductAvailabilitySpecification implements Specification<Product> {
  @Override
  public boolean isSatisfiedBy(Product product) {
    return product.isAvailable();
  }

  public Specification<Product> and(Specification<Product> other) {
    return candidate -> isSatisfiedBy(candidate) && other.isSatisfiedBy(candidate);
  }
}
```

**Pattern:** the interface is generic in the candidate type; `isSatisfiedBy(Object)`
evaluates the specification for one candidate.

**References:**

- Eric Evans' Domain-Driven Design (2003), Chapter 9: "Specification"
- Martin Fowler's Specifications
Pattern

## Governed by

- [Specifications must end with 'Specification'](/rule/advanced/specifications-must-end-with-specification.md)
- [Specifications must not have Spring annotations](/rule/advanced/specifications-must-not-have-spring-annotations.md)

## Discussed in

- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [ELEMENTS](/guide/readme/elements.md)
