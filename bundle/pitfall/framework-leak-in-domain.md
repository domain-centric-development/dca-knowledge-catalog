---
type: Pitfall
title: "Framework leak in the domain layer"
tags: [pitfall, onion, domain, spring]
---

Domain classes that import Spring or JPA — `@Entity`, `@Component`, `@Service`, `@Autowired`, `@Table`, `jakarta.persistence.*`, `org.springframework.*` — right on the aggregates, value objects, and domain services. It feels convenient ("the aggregate *is* the table row"), but it welds the innermost, most valuable layer to infrastructure it should never know about.

## Why it is wrong

- It inverts the dependency rule. The domain is the innermost layer; everything points inward toward it. A Spring/JPA import points the domain *outward* at a framework, breaking the onion.
- It couples the model's shape to persistence and DI concerns. Adding a column, changing an ORM mapping, or swapping frameworks now forces edits to domain logic.
- It poisons testing. A domain that needs an application context or an ORM to instantiate can't be unit-tested as pure logic — the fast, dependency-free tests that make a rich model worth having disappear.
- It smuggles infrastructure semantics (lazy loading, proxies, transaction demarcation) into code that should express only business rules.

## What forbids it

- [The Domain Model should be framework independent and should not use 3rd party libraries when possible](/rule/onion/the-domain-model-should-be-framework-independent-and-should-not-use-3rd-party-libraries-when-possible.md)
- [Domain Models must not have Spring/JPA annotations](/rule/onion/domain-models-must-not-have-spring-jpa-annotations.md) — mechanically blocks the annotations this anti-pattern relies on.
- [Domain must not have dependencies on Infrastructure](/rule/layered/domain-must-not-have-dependencies-on-infrastructure.md)

## Do instead

Keep the domain pure Java. Model persistence with a separate mapping in the outgoing adapter (a JPA entity or a mapper that translates domain ↔ persistence), and let Spring wire the *adapters and application services*, never the domain types. Dependencies the domain needs are expressed as output-port interfaces it owns; adapters implement them.

Domain: `public final class Money { … }` with no annotations. Persistence: a separate `MoneyEmbeddable` / mapper in `adapter/outgoing`.

## Anchors

- Guide: [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md) · [Layer elements](/guide/readme/elements.md)
- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [DomainService](/marker/tactical/domainservice.md) · [Value](/marker/tactical/value.md)
- Related pitfall: [DTO in the application layer](/pitfall/dto-in-application-layer.md) · [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md)
