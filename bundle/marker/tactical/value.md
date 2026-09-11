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

- [Value Objects must not contain Aggregate Roots or Entities](/rule/tactical/dca-tac-008.md)
- [Value Object classes should be final (immutability)](/rule/tactical/dca-tac-009.md)
- [Value Object fields must be final (shallow immutability)](/rule/tactical/dca-tac-010.md)
- [Value Objects must not have setter methods](/rule/tactical/dca-tac-011.md)

## Related mentions in guides (heuristic)

- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [Application Layer (Use Cases / Application Business Rules)](/guide/elements/application-layer-use-cases-application-business-rules.md)
- [Enriched Read Model Pattern](/guide/integration-patterns/enriched-read-model-pattern.md)
- [6. JWT Claims Design](/guide/jwt-implementation-guide/6-jwt-claims-design.md)
- [8. CSRF Protection](/guide/jwt-implementation-guide/8-csrf-protection.md)
- [DOMAIN LAYER RULES](/guide/rules/domain-layer-rules.md)
- [Event-Driven Architecture in Spring Modulith](/guide/spring-modulith/event-driven-architecture-in-spring-modulith.md)
- [Shared Kernel Pattern (Strategic DDD)](/guide/strategic-design/shared-kernel-pattern-strategic-ddd.md)
- [What belongs in the shared kernel](/guide/strategic-design/what-belongs-in-the-shared-kernel.md)
