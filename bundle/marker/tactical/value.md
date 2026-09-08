---
type: Marker
title: Value
category: tactical
kind: interface
signature: public interface Value
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/Value.java
tags: [tactical, marker]
---

Marker interface for Value Objects.

A Value Object describes a characteristic - an amount of money, an address, a quantity - and
has no identity: two values with the same attributes are the same value. It is immutable; a
change produces a new instance. Because it has no life cycle of its own, it is never loaded or
saved on its own - it travels inside the Entity or Aggregate Root that holds it.

**Characteristics:**

- Immutable: all fields final, no setters; a record is the natural shape
- Equality by attributes, not by reference or identifier
- Self-validating: the constructor rejects values that make no sense in the domain
- Behaviour is side-effect free and returns new values (`money.add(other)`)
- Must not reference Aggregate Roots or Entities

**Example:**

```java
public record Money(BigDecimal amount, Currency currency) implements Value {
  public Money {
    Objects.requireNonNull(amount, "amount");
    Objects.requireNonNull(currency, "currency");
  }

  public Money add(Money other) {
    requireSameCurrency(other);
    return new Money(amount.add(other.amount), currency);
  }
}
```

Identifiers are Value Objects too, but carry their own marker: `d`.

## Governed by

- [Enriched Domain Models must be Value Object records](/rule/tactical/enriched-domain-models-must-be-value-object-records.md)
- [Value Object classes should be final (immutability)](/rule/tactical/value-object-classes-should-be-final-immutability.md)
- [Value Object fields must be final (deep immutability)](/rule/tactical/value-object-fields-must-be-final-deep-immutability.md)
- [Value Objects must be records or immutable classes with attribute equality](/rule/tactical/value-objects-must-be-records-or-immutable-classes-with-attribute-equality.md)
- [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)
- [Value Objects must not have setter methods](/rule/tactical/value-objects-must-not-have-setter-methods.md)
- [Use Case Result Models must end with 'Result' and reside in application package](/rule/usecase/use-case-result-models-must-end-with-result-and-reside-in-application-package.md)

## Discussed in

- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [6. JWT Claims Design](/guide/jwt-implementation-guide/6-jwt-claims-design.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
