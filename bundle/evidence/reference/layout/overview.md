---
type: Reference
title: DcaLayout — Overview
tags: [reference]
evidence_for: /reference/layout.md
---

[Full node and context](/reference/layout.md). This is an evidence excerpt; retain the parent selection and caveats.

Describes how a Domain-Centric Architecture code base is laid out in packages, so that the DCA
rules can be applied to any project regardless of its base package or naming conventions.

Obtain the DCA defaults with `forBasePackage(String)` and override individual settings
through the fluent `with*` methods:

```java
DcaLayout layout = DcaLayout.forBasePackage("com.acme.shop")
    .withIncomingSubpackage("in")
    .withOutgoingSubpackage("out")
    .withApiSubpackage("contract");
```

All package patterns returned by this class use ArchUnit's package-matching syntax (`..`
for any number of sub-packages, `*` for exactly one segment).

**Wildcard patterns versus discovered contexts.** The no-argument accessors (`domainPattern()` and its siblings) build `base.*.domain..`, where `*` is exactly one
segment — they therefore only ever match a bounded context that is a direct child of the base
package. They are kept for projects that have not declared their contexts yet, and for tooling
that needs a pattern without an imported class graph. **The rules do not use them.** Every
rule selects through `DcaArchitecture`'s discovery accessors (`contextDomainPatterns()`, `allDomainPatternsWithSharedKernel()`, …), which are built from
the packages that actually carry `@BoundedContext` and so work at any depth: `base.sales.order` and a single-context application that annotates its base package are both
governed.

The wildcard is deliberately not loosened to `base..domain..`: that would also match any
package merely *named* `domain` further down, such as an outgoing adapter mapping to a
foreign model. A module is instead found structurally by `DcaArchitecture.moduleRoots()` —
the shortest prefix that owns a layer — which needs no annotation and is not fooled by such a
package.

## Settings and defaults (Java)

Create the default layout with `DcaLayout.forBasePackage(String)`; every setting has a fluent override.

| Setting | Default | Override | Meaning |
|---|---|---|---|
| `basePackage` | the argument of `forBasePackage(...)` | constructor only | Root package of the application; everything the rules govern lies below it. |
| `sharedKernelSubpackage` | `sharedkernel` | `withSharedKernelSubpackage(...)` |  |
| `domainSubpackage` | `domain` | `withDomainSubpackage(...)` |  |
| `modelSubpackage` | `model` | `withModelSubpackage(...)` | Sub-package of the domain layer that holds the domain model — aggregates, entities, value objects — e.g. `"model"` (default) or `"entities"`. The domain-model rules and the domain cycle rule select `.domain...`. |
| `applicationSubpackage` | `application` | `withApplicationSubpackage(...)` |  |
| `sharedSubpackage` | `shared` | `withSharedSubpackage(...)` | Sub-package of the application layer that holds the output ports shared by the use cases of one context - e.g. `"shared"` (default), `"ports"` or `"spi"`. The name is reserved: it may not be used as an operation container. |
| `adapterSubpackage` | `adapter` | `withAdapterSubpackage(...)` |  |
| `incomingSubpackage` | `incoming` | `withIncomingSubpackage(...)` | Name of the incoming (driving/primary) adapter sub-package — `"in"` in some projects. |
| `incomingEventSubpackage` | `event` | `withIncomingEventSubpackage(...)` | Sub-package of the incoming adapters that holds the event consumers — the adapters that react to other modules' integration events — e.g. `"event"` (default) or `"listener"`. Classes below `.adapter.incoming...` are the one kind of incoming adapter the adapter-isolation rules exempt. |
| `webSubpackage` | `web` | `withWebSubpackage(...)` | Sub-package of the incoming adapters that holds the web adapter - e.g. `"web"` (default), `"ui"` or `"mvc"`. Only `DCA-NAM-011` reads it: a ViewModel belongs below `.adapter.incoming...`. |
| `outgoingSubpackage` | `outgoing` | `withOutgoingSubpackage(...)` | Name of the outgoing (driven/secondary) adapter sub-package — `"out"` in some projects. |
| `infrastructureSubpackage` | `infrastructure` | `withInfrastructureSubpackage(...)` |  |
| `apiSubpackage` | `api` | `withApiSubpackage(...)` | Sub-package of a module's *synchronous* published contract, e.g. `"api"` (default) or `"contract"`. Together with `withEventsSubpackage(String)` it is the only part of a module another module's adapters may depend on; the context-map rules and renderer use the same name for the channel. |
| `eventsSubpackage` | `events` | `withEventsSubpackage(...)` | Sub-package of a module's *asynchronous* published contract — its integration events — e.g. `"events"` (default) or `"published"`. |
| `useCaseSuffix` | `UseCase` | `withUseCaseSuffix(...)` | Suffix of use-case implementations, e.g. `"UseCase"` or `"ApplicationService"`. |
| `controllerSuffix` | `Controller` | `withControllerSuffix(...)` | Suffix of MVC (server-rendered) controllers, e.g. `"Controller"` (default) or `"Page"`. Read by the naming rule for classes carrying the configured `@Controller` annotation and by the rule that keeps controllers away from repositories; the REST suffix is configured separately. |
| `restControllerSuffix` | `Resource` | `withRestControllerSuffix(...)` | Suffix of REST controllers, e.g. `"Resource"` or `"Controller"`. |
| `aggregateRootSuffix` | `AggregateRoot` | `withAggregateRootSuffix(...)` | Suffix by which `DCA-TAC-001` finds a project's aggregate roots by name - `"AggregateRoot"` by default. Only the suffix selects: an aggregate root named otherwise is never reported by that rule, and the role is what every other tactical rule selects on. |
| `repositorySuffix` | `Repository` | `withRepositorySuffix(...)` | Suffix of a repository port, `"Repository"` by default - read by `DCA-TAC-013` and `DCA-TAC-016`, which also requires the name to be the bound aggregate plus this suffix. |
| `storeSuffix` | `Store` | `withStoreSuffix(...)` | Suffix of a store port, `"Store"` by default - read by `DCA-TAC-018`. |
| `factorySuffix` | `Factory` | `withFactorySuffix(...)` | Suffix of a factory, `"Factory"` by default - read by `DCA-ADV-013`. |
| `specificationSuffix` | `Specification` | `withSpecificationSuffix(...)` | Suffix by which a specification is found when it carries no marker, `"Specification"` by default - read by `DCA-ADV-017` and `DCA-ADV-018` alongside the specification role. |
| `timestampTypes` | `DEFAULT_TIMESTAMP_TYPES` | `withTimestampTypes(...)` | Types a domain event may store its occurrence time in, by fully qualified name. Replaces the default list (`java.time.Instant`, `OffsetDateTime`, `ZonedDateTime`, `LocalDateTime`) - a project whose own event vocabulary wraps the timestamp in a value object names that type here instead of excluding `DCA-ADV-008`. At least one name is required: an empty list would report every event. |
| `markers` | `DcaMarkers.dca()` | `withMarkers(...)` | The building-block types the rules select on, by role — `dca()` by default, or a vocabulary pointed at the project's own markers. The rules then select what carries those types instead of the library's, so a code base with an established vocabulary needs no rule exclusions. |
| `frameworkCandidates` | `detection.candidates()` | constructor only |  |
| `OperationContainers` | see declaration | `withOperationContainers(...)` | Organisational package segments ignored when measuring operation depth; empty by default. |
| `FrameworkPreset` | see declaration | `withFrameworkPreset(...)` | The preset registered under the given name — built-in (`spring`, `jakarta`, `quarkus`, `micronaut`, `none`) or contributed by a library through `FrameworkAnnotationsProvider`. This is what `dca.framework=` in `dca-archunit.properties` applies; an unknown name fails, a typo must not fall back silently. |

## Third-party packages the domain may depend on (Java default)

- `java..`
- `lombok..`
- `org.apache.commons.lang3..`
- `org.apache.commons.collections4..`
- `org.jspecify.annotations..`

Replace the list with `withThirdPartyPackagesAllowedInDomain(List)` or extend it with `allowingInDomain(String...)`.

## Building-block package constants (Java)

| Constant | Pattern |
|---|---|
| `BUILDING_BLOCKS_PORT_IN_PACKAGE` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.in..` |
| `BUILDING_BLOCKS_PORT_OUT_PACKAGE` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out..` |

## Derived package names and patterns (Java)

ArchUnit pattern syntax: `..` any number of sub-packages, `*` exactly one segment. The no-argument wildcard accessors match direct children of the base package only; the rules select through [DcaArchitecture](/reference/architecture.md) instead, which works at any depth.

| Accessor | Yields |
|---|---|
| `String sharedKernelPackage()` | `base.sharedkernel` (no pattern suffix). |
| `String sharedKernelPattern()` | `base.sharedkernel..` |
| `String sharedKernelDomainPattern()` | `base.sharedkernel.domain..` |
| `String sharedKernelDomainModelPattern()` | `base.sharedkernel.domain.model..` |
| `String infrastructurePackage()` | `base.infrastructure` (no pattern suffix). |
| `String infrastructurePattern()` | `base.infrastructure..` |
| `String infrastructurePackage(String modulePackage)` | `base.cart.infrastructure` — a module's own infrastructure package (no suffix). |
| `String channelSubpackage(Upstream.Consumes channel)` | The sub-package a consumed channel maps to: `apiSubpackage()` for `API`, `eventsSubpackage()` for `EVENTS`. The context-map rules and the renderer name channels through this one method. |
| `String domainPattern()` | `base.*.domain..` — the domain layer of every *direct* sub-package. Matches a bounded context only when it is a direct child of the base package; prefer `DcaArchitecture.contextDomainPatterns()`, which is derived from the declared contexts and holds at any depth. |
| `String domainModelPattern()` | `base.*.domain.model..` |
| `String applicationPattern()` | `base.*.application..` |
| `String sharedOutputPortPattern()` | `base.*.application...` — output ports shared by the use cases of one context. |
| `String adapterPattern()` | `base.*.adapter..` |
| `String incomingAdapterPattern()` | `base.*.adapter.incoming..` |
| `String outgoingAdapterPattern()` | `base.*.adapter.outgoing..` |
| `String domainPattern(String contextPackage)` | `<contextPackage>.domain..` - the same pattern below the given context or module package. |
| `String domainModelPattern(String contextPackage)` | `<contextPackage>.domain.model..` - the same pattern below the given context or module package. |
| `String domainModelPackage(String contextPackage)` | `base.cart.domain.model` — a module's domain-model package (no pattern suffix). |
| `String applicationPattern(String contextPackage)` | `<contextPackage>.application..` - the same pattern below the given context or module package. |
| `String sharedOutputPortPattern(String contextPackage)` | `<contextPackage>.application...` - the same pattern below the given context or module package. |
| `String adapterPattern(String contextPackage)` | `<contextPackage>.adapter..` - the same pattern below the given context or module package. |
| `String incomingAdapterPattern(String contextPackage)` | `<contextPackage>.adapter.incoming..` - the same pattern below the given context or module package. |
| `String incomingEventAdapterPattern()` | `..adapter.incoming.event..` — the event consumers of any module, at any depth; the segment names come from this layout. |
| `String outgoingAdapterPattern(String contextPackage)` | `<contextPackage>.adapter.outgoing..` - the same pattern below the given context or module package. |
| `String markersReport()` | One line for the report: `dca (library default)` while every role names the building blocks' own marker, or the vocabulary's name and the roles that differ, so a reader sees which types the rules actually selected on — `company (aggregateRoot=com.company.ddd.Root, repository=com.company.ddd.Store)`. |

## Framework annotations the rules look for (Java, `FrameworkAnnotations`)

Annotations are matched by fully qualified name and grouped by *role*; the rule library has no framework dependency. `DcaLayout.forBasePackage` detects the preset from the framework on the test class path (Spring when nothing is found) and the report names the choice; `withFrameworkPreset(name)` or `dca.framework=<name>` in the properties selects one by name, `withFrameworkAnnotations(...)` sets one in code and always wins. A library contributes a preset through the `FrameworkAnnotationsProvider` SPI (`ServiceLoader`). Start from a preset — `spring()`, `jakarta()`, `quarkus()`, `micronaut()`, `none()` — and adjust single roles with `withInjectable(...)`, `withTransactional(...)` and their siblings; `none()` leaves every role empty, so rules that forbid a role have nothing to forbid and rules that require one select nothing. A rule that forbids a role treats every listed annotation as forbidden; a rule that requires a role accepts any of them. The preset in use is named in the test report.

| Role | `spring()` | `jakarta()` | `quarkus()` | `micronaut()` | Used for |
|---|---|---|---|---|---|
| `injectable` | `org.springframework.stereotype.Service`<br>`org.springframework.stereotype.Component` | `jakarta.enterprise.context.ApplicationScoped`<br>`jakarta.enterprise.context.Dependent`<br>`jakarta.enterprise.context.RequestScoped`<br>`jakarta.inject.Singleton` | `jakarta.enterprise.context.ApplicationScoped`<br>`jakarta.enterprise.context.Dependent`<br>`jakarta.enterprise.context.RequestScoped`<br>`jakarta.inject.Singleton` | `jakarta.inject.Singleton`<br>`io.micronaut.context.annotation.Prototype`<br>`io.micronaut.context.annotation.Bean` | stereotypes of container-managed components |
| `webController` | `org.springframework.stereotype.Controller` | `jakarta.mvc.Controller` | — | — | stereotype of server-rendering controllers |
| `restController` | `org.springframework.web.bind.annotation.RestController` | `jakarta.ws.rs.Path` | `jakarta.ws.rs.Path` | `io.micronaut.http.annotation.Controller` | stereotype of REST endpoint classes |
| `transactional` | `org.springframework.transaction.annotation.Transactional`<br>`jakarta.transaction.Transactional` | `jakarta.transaction.Transactional` | `jakarta.transaction.Transactional` | `io.micronaut.transaction.annotation.Transactional`<br>`jakarta.transaction.Transactional` | declarative transaction demarcation |
| `eventListener` | `org.springframework.context.event.EventListener` | `jakarta.enterprise.event.Observes` | `jakarta.enterprise.event.Observes`<br>`io.quarkus.vertx.ConsumeEvent` | `io.micronaut.runtime.event.annotation.EventListener` | in-process event listener |
| `moduleDeclaration` | `org.springframework.modulith.ApplicationModule` | — | — | — | module declaration on `package-info` |
| `publishedInterface` | `org.springframework.modulith.NamedInterface` | — | — | — | published-package declaration on `package-info` |
| `persistenceEntity` | `jakarta.persistence.Entity`<br>`jakarta.persistence.Table` | `jakarta.persistence.Entity`<br>`jakarta.persistence.Table` | `jakarta.persistence.Entity`<br>`jakarta.persistence.Table` | `jakarta.persistence.Entity`<br>`jakarta.persistence.Table`<br>`io.micronaut.data.annotation.MappedEntity` | ORM mapping annotations of a persistent class |
| `injectionSite` | `org.springframework.beans.factory.annotation.Autowired`<br>`jakarta.inject.Inject`<br>`jakarta.annotation.Resource` | `jakarta.inject.Inject` | `jakarta.inject.Inject` | `jakarta.inject.Inject` | constructor, field or setter injection annotations |
| `persistenceMapping` | `jakarta.persistence.Id`<br>`jakarta.persistence.Column`<br>`jakarta.persistence.Embedded`<br>`jakarta.persistence.OneToMany`<br>`jakarta.persistence.ManyToOne`<br>`jakarta.persistence.OneToOne`<br>`jakarta.persistence.ManyToMany`<br>`jakarta.persistence.Transient`<br>`jakarta.persistence.Version` | `jakarta.persistence.Id`<br>`jakarta.persistence.Column`<br>`jakarta.persistence.Embedded`<br>`jakarta.persistence.OneToMany`<br>`jakarta.persistence.ManyToOne`<br>`jakarta.persistence.OneToOne`<br>`jakarta.persistence.ManyToMany`<br>`jakarta.persistence.Transient`<br>`jakarta.persistence.Version` | `jakarta.persistence.Id`<br>`jakarta.persistence.Column`<br>`jakarta.persistence.Embedded`<br>`jakarta.persistence.OneToMany`<br>`jakarta.persistence.ManyToOne`<br>`jakarta.persistence.OneToOne`<br>`jakarta.persistence.ManyToMany`<br>`jakarta.persistence.Transient`<br>`jakarta.persistence.Version` | `jakarta.persistence.Id`<br>`jakarta.persistence.Column`<br>`jakarta.persistence.Embedded`<br>`jakarta.persistence.OneToMany`<br>`jakarta.persistence.ManyToOne`<br>`jakarta.persistence.OneToOne`<br>`jakarta.persistence.ManyToMany`<br>`jakarta.persistence.Transient`<br>`jakarta.persistence.Version`<br>`io.micronaut.data.annotation.Id`<br>`io.micronaut.data.annotation.MappedProperty`<br>`io.micronaut.data.annotation.Relation` | member-level persistence mapping annotations |
| `transactionApi` | `org.springframework.transaction.support.TransactionTemplate`<br>`org.springframework.transaction.support.TransactionOperations`<br>`org.springframework.transaction.reactive.TransactionalOperator`<br>`jakarta.transaction.UserTransaction` | `jakarta.transaction.UserTransaction` | `jakarta.transaction.UserTransaction`<br>`io.quarkus.narayana.jta.QuarkusTransaction` | `io.micronaut.transaction.TransactionOperations`<br>`io.micronaut.transaction.SynchronousTransactionManager`<br>`jakarta.transaction.UserTransaction` | types code uses to run a transaction (templates, user transactions), matched as class dependencies rather than as annotations |
| `transactionManager` | `org.springframework.transaction.PlatformTransactionManager`<br>`org.springframework.transaction.TransactionManager`<br>`org.springframework.transaction.ReactiveTransactionManager`<br>`jakarta.transaction.TransactionManager` | `jakarta.transaction.TransactionManager` | `jakarta.transaction.TransactionManager` | `jakarta.transaction.TransactionManager` | types a composition root declares or wires (transaction managers), matched as class dependencies rather than as annotations |
| `transportStatus` | `org.springframework.web.bind.annotation.ResponseStatus` | — | — | `io.micronaut.http.annotation.Status` | annotations that fix the protocol answer of the type they sit on |

## Building-block types the rules select on (`DcaMarkers`)

The rules never name a building block as a type: every selection asks the layout for a *role*, resolved by fully qualified name. The default vocabulary is this library's own markers, so a project on the building blocks configures nothing. A project that already has its own markers - or another library's - points the roles at its own types and is then governed by the whole catalog, instead of excluding the rule ids that would have selected nothing. The same roles exist in both languages (`withMarkers(DcaMarkers.dca().withAggregateRoot("..."))` in Java, `WithMarkers(DcaMarkers.Dca() with { AggregateRoot = "..." })` in .NET; the .NET defaults are the `I`-prefixed twins).

A role names exactly one type and must not be blank - an empty role would select nothing and report success. Two vocabularies at once are outside this: a migration points the role at one of them. What the roles do **not** cover are the strategic annotations, because the rules read their members (the context a relationship names, the dependencies a module allows) and a type name carries none.

| Role | Default (Java) | Selects |
|---|---|---|
| `aggregateRoot` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.AggregateRoot` | the marker of an aggregate root |
| `entity` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.Entity` | the marker of an entity |
| `value` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.Value` | the marker of a value object |
| `id` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.Id` | the marker of an identifier |
| `domainEvent` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainEvent` | the marker of a domain event |
| `integrationEvent` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.IntegrationEvent` | the marker of an integration event |
| `domainService` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainService` | the marker of a domain service |
| `factory` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.Factory` | the marker of a factory |
| `specification` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.Specification` | the marker of a specification — a predicate over a domain object, selected by `DCA-ADV-017` and `DCA-ADV-018` alongside the name suffix |
| `domainException` | `dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainException` | the base type of a domain failure |
| `useCaseException` | `dev.domaincentric.dca.buildingblocks.application.UseCaseException` | the base type of a use-case failure |
| `transactionBoundary` | `dev.domaincentric.dca.buildingblocks.application.TransactionBoundary` | the explicit transaction boundary of the application layer |
| `inputPort` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.in.InputPort` | the base type of every incoming (driving) port |
| `useCase` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.in.UseCase` | the input port that takes a command or query and answers with a result |
| `outputPort` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out.OutputPort` | the base type of every outgoing (driven) port |
| `repository` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out.Repository` | the outgoing port that loads and stores an aggregate |
| `store` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out.Store` | the outgoing port that holds data no aggregate owns |
| `domainEventPublisher` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out.DomainEventPublisher` | the outgoing port that publishes an aggregate's domain events |
| `integrationEventPublisher` | `dev.domaincentric.dca.buildingblocks.hexagonal.port.out.IntegrationEventPublisher` | the outgoing port that publishes an integration event — read by `DCA-USE-013`, which separates the output ports that live inside the transaction from those that may leave the process. The .NET twin carries the role without a caller, because that rule is not applicable there |

## .NET twin: `DcaLayout` in `DomainCentric.ArchRules`

Describes how a Domain-Centric Architecture code base is laid out in namespaces, so that the DCA
rules can be applied to any project regardless of its root namespace or naming conventions.

Obtain the DCA defaults with `ForRootNamespace` and override individual settings
through the fluent `With*` methods:

```csharp
var layout = DcaLayout.ForRootNamespace("Acme.Shop")
.WithIncomingSegment("In")
.WithOutgoingSegment("Out");
```

Every `*Pattern` member returns a .NET regular expression over full namespace names,
ready for ArchUnitNET's `ResideInNamespaceMatching(pattern)`. Layout segments are matched
case-sensitively, exactly as written.

The layout assumes one root namespace per application. A namespace at any depth below it
that carries a `[BoundedContext]` marker class is a bounded context (`Acme.Shop.Cart`,
`Acme.Shop.Sales.Order`, or the root itself for a single-context application); the one carrying
`[SharedKernel]` is the shared kernel. Bounded contexts may live in one assembly or in one
assembly each — the rules work on namespaces, so both layouts are supported.

**Wildcard patterns versus discovered modules.** The parameterless `*Pattern`
properties (`DomainPattern` and siblings) build `Root.[^.]+.Domain`, where the
wildcard is exactly one segment — they only ever match a module that is a direct child of the root
namespace. They are kept for tooling that needs a pattern without a loaded type graph. **The rules
do not use them.** Every rule selects through `DcaArchitecture`'s discovery accessors
(`AllDomainPatterns()`, `ContextDomainPatterns()`, …), built from the module roots and
declared contexts actually present, and so works at any depth. The wildcard is deliberately not
loosened to `.*`: that would also match any namespace merely *named* `Domain` further
down, such as an outgoing adapter mapping to a foreign model.
