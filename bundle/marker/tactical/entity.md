---
type: Marker
title: "Entity<T, ID>"
category: tactical
kind: interface
signature: "public interface Entity<T extends Entity<T, ID>, ID extends Id>"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
generics: "T extends Entity<T, ID>, ID extends Id"
methods: ["ID id()", "default boolean sameIdentityAs(T other)"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Entity.java
tags: [tactical, marker]
---

Marker interface for Entities.

An Entity is a domain object defined by its identity, not by its attributes: a line item stays
the same line item while its quantity changes, and two line items with equal attributes are still
two. Every Entity carries a typed identifier (`d`) that is stable for its whole life.

An Entity that is not itself an Aggregate Root lives inside exactly one aggregate. It is
created, changed and removed only through its root, is never loaded or saved on its own, and is
therefore never returned from a Repository. Its identity is unique within the aggregate, not
necessarily across the system.

**Characteristics:**

- Has an identifier field returned by `id()`
- Equality means identity: `sameIdentityAs(Entity)` compares identifiers only
- Changes state through behaviour methods named in the ubiquitous language, never setters
- Non-root Entities expose no public constructor - the Aggregate Root creates them
- Holds no reference to an Aggregate Root; it is reached from the root, not the other way

**Example:**

```java
public class LineItem implements Entity<LineItem, LineItemId> {
  private final LineItemId id;
  private Quantity quantity;

  LineItem(LineItemId id, ProductId product, Quantity quantity) { ... }  // package-private

  public LineItemId id() { return id; }

  public void increaseBy(Quantity amount) { this.quantity = quantity.plus(amount); }
}
```

## Governed by

- [Domain model classes must not have public setter methods](/rule/tactical/domain-model-classes-must-not-have-public-setter-methods.md)
- [Entities must have an ID field](/rule/tactical/entities-must-have-an-id-field.md)
- [Entities must not be instantiated directly from outside the aggregate](/rule/tactical/entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md)
- [Entities must not have fields with Aggregate Root types](/rule/tactical/entities-must-not-have-fields-with-aggregate-root-types.md)
- [Repository methods must not return non-root Entities](/rule/tactical/repository-methods-must-not-return-non-root-entities.md)
- [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)
- [Use Case Result Models must not expose aggregate roots or entities](/rule/usecase/use-case-result-models-must-not-expose-aggregate-roots-or-entities.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Complete Test Suites](/guide/archunit-governance/complete-test-suites.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
