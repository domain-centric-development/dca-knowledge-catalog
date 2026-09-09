---
type: Marker
title: Id
category: tactical
kind: interface
signature: public interface Id
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Id.java
tags: [tactical, marker]
---

Marker interface for typed identifiers of Entities and Aggregate Roots.

An identifier is a Value Object whose only job is to name one Entity for its whole life.
Giving every Entity its own identifier type (`ContractId`, `ShipmentId`) instead of a
bare `UUID` or `String` lets the compiler reject one aggregate's id passed where
another's is expected, and lets a Repository's signature say which aggregate it manages.

**Characteristics:**

- Immutable, with attribute equality - a record is the natural shape
- Validates its own wrapped value (never null, well-formed)
- Carries no behaviour beyond identity; generation (`newId()`) may live on the type
- Lives in the domain layer of the context that owns the Entity; identifiers shared across
contexts belong in the shared kernel

**Example:**

```java
public record ProductId(UUID value) implements Id {
  public ProductId {
    Objects.requireNonNull(value, "value");
  }

  public static ProductId newId() {
    return new ProductId(UUID.randomUUID());
  }
}
```

## Governed by

- [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Complete Test Suites](/guide/archunit-governance/complete-test-suites.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [6. JWT Claims Design](/guide/jwt-implementation-guide/6-jwt-claims-design.md)
- [Building Blocks](/guide/language-mappings/building-blocks.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [RULES](/guide/readme/rules.md)
