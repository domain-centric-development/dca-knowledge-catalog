---
type: Decision
title: "Where does the logic live: aggregate method, domain service, or use case"
tags: [decision, tactical, domain, application, domain-service, use-case]
---

You have a piece of business logic to place. It can go in three places, and picking the wrong one is how domain models turn anemic or use cases turn into fat transaction scripts. The fork: does the behaviour belong **on an aggregate**, in a **domain service**, or in the **use case** (application service)?

## The discriminator

Ask, in order:

1. **Does the logic operate on the state of a single aggregate?** Then it is a **method on that aggregate**. `order.ship()`, not `orderService.ship(order)`. This is the default and should absorb the large majority of domain logic — behaviour belongs where the data is.
2. **Does it express a genuine domain rule that spans several aggregates and belongs to no single one?** Then it is a **domain service** — stateless, framework-free, living in the domain package. Domain services should be **rare**; reach for one only when the operation truly has no natural home on an entity or value object.
3. **Is it orchestration — loading aggregates, calling one behaviour, saving, publishing events, mapping to a result?** Then it is the **use case**. The use case coordinates; it must not *contain* business logic, validation, or calculation.

A quick tell: if the "service" reads an aggregate's fields, computes, and writes them back, the logic belonged on the aggregate — you are building an [anemic domain model](/pitfall/anemic-domain-model.md).

## Options

| | Aggregate method | Domain service | Use case (application service) |
|---|---|---|---|
| Holds business logic | yes — on its own state | yes — pure calculation across aggregates | no — orchestration only |
| State | mutates its own guarded state | stateless (only final deps) | stateless orchestrator |
| Framework | none | none — plain domain class, no Spring | Spring-wired (`@Service`, `@Transactional`) |
| Lives in | domain (the aggregate) | domain package | application (use case folder) |
| Frequency | the common case | rare | one per operation |

**Default: put it on the aggregate.** Only lift logic into a domain service when it genuinely spans aggregates and fits none of them. The preferred shape for a domain service is *pure*: the use case loads the data via output ports and passes it in as parameters, so the domain service stays dependency-free and trivially testable.

## Consequences

- A domain service is stateless and carries no Spring annotations — it is a plain domain class enforced to reside in the domain package (see anchors).
- The use case orchestrates and delegates: load → invoke one domain behaviour → save → publish events → map to result. If it starts branching on domain state or computing totals, that logic belongs inward.
- An aggregate method mutates only its own state through intention-revealing operations that protect invariants; it must not reach out to repositories or other output ports.

## Anchors

- Markers: [DomainService](/marker/tactical/domainservice.md) · [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md)
- Rules: [Domain Services must reside in domain package](/rule/advanced/domain-services-must-reside-in-domain-package.md) · [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/domain-services-should-be-stateless-only-final-fields-for-dependencies.md) · [Domain Services must not have Spring annotations](/rule/advanced/domain-services-must-not-have-spring-annotations.md) · [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- ADRs: [ADR-010 Domain Services Only for Multi-Aggregate Operations](/adr/adr-010-domain-services-multi-aggregate.md) · [ADR-002 Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md) · [ADR-021 Enriched Domain Model Pattern](/adr/adr-021-enriched-domain-model-pattern.md)
- Book: [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md) · [Use Case Implementation](/book/06-application-layer/use-case-implementation.md)
- Guide: [Default rule: pure domain services](/guide/domain-services-with-data-dependencies/default-regel-pure-domain-services-90-der-fälle.md) · [When to use which approach](/guide/domain-services-with-data-dependencies/vergleich-wann-welchen-ansatz-nutzen.md)
- Recipes: [Add a use case](/recipe/add-a-use-case.md) · [Add an aggregate](/recipe/add-an-aggregate.md)
- Related pitfall: [Anemic domain model](/pitfall/anemic-domain-model.md)
