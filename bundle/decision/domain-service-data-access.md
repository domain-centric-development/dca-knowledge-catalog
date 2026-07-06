---
type: Decision
title: "Domain service data access: injected output port or passed-in data"
tags: [decision, tactical, domain-service, domain, gateway]
---

A domain service needs data it doesn't hold — a category's discount table, a price it must look up, some fact that lives in another aggregate or a repository. The tempting move is to inject the `Repository` (or another output port) straight into the domain service. DCA says: **don't** — a domain service is a pure domain class in the innermost ring and must not depend on the application layer or adapters. So the fork is: does the service take its data as **passed-in parameters** (the use case loads it), or through an **abstract domain interface** it owns (dependency inversion), or does it never legitimately need external data at all? This is the *data-access* companion to [where does the logic live](/decision/where-does-the-logic-live.md), which decides whether the logic belongs on the aggregate, in a domain service, or in the use case in the first place.

## The discriminator

Ask, in order:

1. **Can the use case load everything the service needs up front?** Then it does — the use case reads via output ports and passes plain domain objects (Value Objects, prices, quantities) as method parameters. The service stays **pure**: no injected port, no repository, trivially testable. This is the default and covers the large majority of cases.
2. **Must the domain service itself decide dynamically what to fetch** (it can't be pre-loaded because the query depends on branching domain logic), or do several services share the same lookup? Then invert the dependency: declare an **abstract domain interface (`DomainGateway`)** *in the domain package*, inject that interface, and implement it in an outgoing adapter. The domain depends only on its own abstraction, never on a `Repository` or adapter type.
3. **Is it a single, simple query at one call site?** A lightweight **Strategy/Callback** (a function passed in by the use case) avoids a dedicated interface.

A hard "no" underlies all three: **never inject a `Repository`, `Store`, or any concrete output port into a domain service.** That would drag an application-layer contract into the domain and break the dependency rule.

## Options

| | Pure (passed-in params) | DomainGateway | Strategy / Callback |
|---|---|---|---|
| Who loads the data | the use case, up front | the injected domain interface, on demand | the use case, via a passed function |
| Dependency in the domain | none | an **abstract interface owned by the domain** | none |
| Injected output port? | no | no — a domain abstraction, impl in adapter | no |
| Testability | trivial (plain args) | mock the gateway | inline lambda |
| Use when | data is pre-loadable (1–2 sources) | domain decides what it needs / shared lookup | single simple query at one service |
| Frequency | the default (~90%) | occasional | occasional |

## Consequences

- A domain service is **stateless — only final fields for dependencies** (see anchors), and those dependencies are *domain abstractions*, never repositories or adapters. It carries **no Spring annotations** and must **reside in the domain package**.
- Choosing "pure" keeps the use case as the single place that touches output ports: load → pass into the domain service → act on the result. If you find yourself wanting to inject a repository into the service, that is the signal to move the load up into the use case instead.
- The `DomainGateway` route is dependency inversion, not a loophole: the interface lives in the domain, the implementation in `adapter.outgoing`. It does **not** license the service to import a concrete `Repository`.
- Passing an aggregate's fields into a "service" that computes and would write them back is the [anemic domain model](/pitfall/anemic-domain-model.md) smell — that logic belonged on the aggregate.

## Anchors

- Markers: [DomainService](/marker/tactical/domainservice.md) · [DomainGateway](/marker/tactical/domaingateway.md) · [OutputPort](/marker/port-out/outputport.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [Store](/marker/port-out/store.md)
- Rules: [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/domain-services-should-be-stateless-only-final-fields-for-dependencies.md) · [Domain Services must not have Spring annotations](/rule/advanced/domain-services-must-not-have-spring-annotations.md) · [Domain Services must reside in domain package](/rule/advanced/domain-services-must-reside-in-domain-package.md) · [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- ADRs: [ADR-002 Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md) · [ADR-010 Domain Services Only for Multi-Aggregate Operations](/adr/adr-010-domain-services-multi-aggregate.md)
- Guide: [Problemstellung](/guide/domain-services-with-data-dependencies/problemstellung.md) · [Default rule: pure domain services](/guide/domain-services-with-data-dependencies/default-regel-pure-domain-services-90-der-fälle.md) · [DomainGateway Pattern](/guide/domain-services-with-data-dependencies/ansatz-1-domaingateway-pattern.md) · [Strategy/Callback Pattern](/guide/domain-services-with-data-dependencies/ansatz-2-strategy-callback-pattern.md) · [When to use which approach](/guide/domain-services-with-data-dependencies/vergleich-wann-welchen-ansatz-nutzen.md)
- Related decision: [Where does the logic live](/decision/where-does-the-logic-live.md) — the companion fork for *placing* the behaviour before you decide how it gets its data
- Related pitfall: [Anemic domain model](/pitfall/anemic-domain-model.md)
