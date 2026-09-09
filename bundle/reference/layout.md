---
type: Reference
title: DcaLayout
subject: layout
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/DcaLayout.java
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/DcaLayout.cs
tags: [reference, archunit, archunitnet]
---

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
| `applicationSubpackage` | `application` | `withApplicationSubpackage(...)` |  |
| `adapterSubpackage` | `adapter` | `withAdapterSubpackage(...)` |  |
| `incomingSubpackage` | `incoming` | `withIncomingSubpackage(...)` | Name of the incoming (driving/primary) adapter sub-package — `"in"` in some projects. |
| `outgoingSubpackage` | `outgoing` | `withOutgoingSubpackage(...)` | Name of the outgoing (driven/secondary) adapter sub-package — `"out"` in some projects. |
| `infrastructureSubpackage` | `infrastructure` | `withInfrastructureSubpackage(...)` |  |
| `apiSubpackage` | `api` | `withApiSubpackage(...)` | Sub-package of a module's *synchronous* published contract, e.g. `"api"` (default) or `"contract"`. Together with `withEventsSubpackage(String)` it is the only part of a module another module's adapters may depend on; the context-map rules and renderer use the same name for the channel. |
| `eventsSubpackage` | `events` | `withEventsSubpackage(...)` | Sub-package of a module's *asynchronous* published contract — its integration events — e.g. `"events"` (default) or `"published"`. |
| `useCaseSuffix` | `UseCase` | `withUseCaseSuffix(...)` | Suffix of use-case implementations, e.g. `"UseCase"` or `"ApplicationService"`. |
| `controllerSuffix` | `Controller` | `withControllerSuffix(...)` | Suffix of MVC (server-rendered) controllers, e.g. `"Controller"` (default) or `"Page"`. Read by the naming rule for classes carrying the configured `@Controller` annotation and by the rule that keeps controllers away from repositories; the REST suffix is configured separately. |
| `restControllerSuffix` | `Resource` | `withRestControllerSuffix(...)` | Suffix of REST controllers, e.g. `"Resource"` or `"Controller"`. |
| `frameworkCandidates` | `detection.candidates()` | constructor only |  |

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
| `BUILDING_BLOCKS_PACKAGE` | `dev.domaincentric.dca.buildingblocks..` |
| `BUILDING_BLOCKS_TACTICAL_PACKAGE` | `dev.domaincentric.dca.buildingblocks.ddd.tactical..` |
| `BUILDING_BLOCKS_STRATEGIC_PACKAGE` | `dev.domaincentric.dca.buildingblocks.ddd.strategic..` |
| `BUILDING_BLOCKS_PORT_PACKAGE` | `dev.domaincentric.dca.buildingblocks.hexagonal.port..` |
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
| `String sharedOutputPortPattern()` | `base.*.application.shared..` — output ports shared by the use cases of one context. |
| `String adapterPattern()` | `base.*.adapter..` |
| `String incomingAdapterPattern()` | `base.*.adapter.incoming..` |
| `String outgoingAdapterPattern()` | `base.*.adapter.outgoing..` |
| `String domainPattern(String contextPackage)` | `<contextPackage>.domain..` - the same pattern below the given context or module package. |
| `String domainModelPattern(String contextPackage)` | `<contextPackage>.domain.model..` - the same pattern below the given context or module package. |
| `String applicationPattern(String contextPackage)` | `<contextPackage>.application..` - the same pattern below the given context or module package. |
| `String sharedOutputPortPattern(String contextPackage)` | `<contextPackage>.application.shared..` - the same pattern below the given context or module package. |
| `String adapterPattern(String contextPackage)` | `<contextPackage>.adapter..` - the same pattern below the given context or module package. |
| `String incomingAdapterPattern(String contextPackage)` | `<contextPackage>.adapter.incoming..` - the same pattern below the given context or module package. |
| `String outgoingAdapterPattern(String contextPackage)` | `<contextPackage>.adapter.outgoing..` - the same pattern below the given context or module package. |

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

### Settings and defaults (.NET)

Create the default layout with `DcaLayout.ForRootNamespace(string)`.

| Setting | Default | Override |
|---|---|---|
| `SharedKernelSegment` | `SharedKernel` | `WithSharedKernelSegment(...)` |
| `DomainSegment` | `Domain` | `WithDomainSegment(...)` |
| `ApplicationSegment` | `Application` | `WithApplicationSegment(...)` |
| `AdapterSegment` | `Adapter` | `WithAdapterSegment(...)` |
| `IncomingSegment` | `Incoming` | `WithIncomingSegment(...)` |
| `OutgoingSegment` | `Outgoing` | `WithOutgoingSegment(...)` |
| `InfrastructureSegment` | `Infrastructure` | `WithInfrastructureSegment(...)` |
| `ApiSegment` | `Api` | `WithApiSegment(...)` |
| `EventsSegment` | `Events` | `WithEventsSegment(...)` |
| `UseCaseSuffix` | `UseCase` | `WithUseCaseSuffix(...)` |
| `ControllerSuffix` | `Controller` | `WithControllerSuffix(...)` |
| `RestControllerSuffix` | `Controller` | `WithRestControllerSuffix(...)` |

### Third-party namespaces the domain may depend on (.NET default)

- `System`
- `Microsoft.Extensions.Logging.Abstractions`
- `DomainCentric.BuildingBlocks`

Note the difference to Java: the whole `DomainCentric.BuildingBlocks` namespace is allowed, strategic and `Ports.In` markers included.

### Building-block namespace constants (.NET)

| Constant | Namespace |
|---|---|
| `BuildingBlocksNamespace` | `DomainCentric.BuildingBlocks` |
| `BuildingBlocksTacticalNamespace` | `DomainCentric.BuildingBlocks.Ddd.Tactical` |
| `BuildingBlocksStrategicNamespace` | `DomainCentric.BuildingBlocks.Ddd.Strategic` |
| `BuildingBlocksPortsNamespace` | `DomainCentric.BuildingBlocks.Hexagonal.Ports` |
| `BuildingBlocksPortsInNamespace` | `DomainCentric.BuildingBlocks.Hexagonal.Ports.In` |
| `BuildingBlocksPortsOutNamespace` | `DomainCentric.BuildingBlocks.Hexagonal.Ports.Out` |

### Derived namespaces and patterns (.NET)

Patterns are .NET regular expressions over full namespace names for ArchUnitNET's `ResideInNamespaceMatching`.

| Member | Yields |
|---|---|
| `string SharedKernelPattern` | Pattern for `Root.SharedKernel` and everything below. |
| `string SharedKernelDomainPattern` | Pattern for `Root.SharedKernel.Domain` and below. |
| `string SharedKernelDomainModelPattern` | Pattern for `Root.SharedKernel.Domain.Model` and below. |
| `string InfrastructurePattern` | Pattern for `Root.Infrastructure` and below. |
| `string DomainPattern` | Pattern for `Root.*.Domain` and below — the domain layer of every direct child namespace (context). |
| `string DomainModelPattern` | Pattern for `Root.*.Domain.Model` and below. |
| `string ApplicationPattern` | Pattern for `Root.*.Application` and below. |
| `string SharedOutputPortPattern` | Pattern for `Root.*.Application.Shared` and below — output ports shared by the use cases of one context. |
| `string AdapterPattern` | Pattern for `Root.*.Adapter` and below. |
| `string IncomingAdapterPattern` | Pattern for `Root.*.Adapter.Incoming` and below. |
| `string OutgoingAdapterPattern` | Pattern for `Root.*.Adapter.Outgoing` and below. |
| `string DomainPatternOf(string contextNamespace)` |  |
| `string DomainModelPatternOf(string contextNamespace)` |  |
| `string ApplicationPatternOf(string contextNamespace)` |  |
| `string SharedOutputPortPatternOf(string contextNamespace)` |  |
| `string AdapterPatternOf(string contextNamespace)` |  |
| `string IncomingAdapterPatternOf(string contextNamespace)` |  |
| `string OutgoingAdapterPatternOf(string contextNamespace)` |  |
| `static string Below(string ns)` | Regex matching `ns` itself and every namespace below it (ArchUnit's `ns..`). Literal parts are escaped; `Segment` wildcards are kept. |
| `static string AnyOf(IEnumerable<string> patterns)` | Alternation of complete namespace patterns (each already anchored). An empty list yields a pattern that matches nothing — never an empty string, which would match everything. |
| `static string AnySegmentPath(string dottedPath)` | ArchUnit's `..A.B..`: the dotted path appears anywhere on segment boundaries. |
| `static string Exactly(string ns)` | Regex matching exactly `ns` (no sub-namespaces). |

### Framework types the rules look for (.NET, `FrameworkTypes.AspNetCore()`)

Types are matched by full name and grouped by role; `DcaLayout` defaults to the `AspNetCore()` preset, `None()` leaves every role empty (controllers are then recognised by suffix only), and a `with` expression adjusts single roles. The preset in use is part of the layout's `ToString()`.

| Role | `AspNetCore()` | Used for |
|---|---|---|
| `ControllerBase` | `Name` | Base class of server-rendering and API controllers. |
| `ApiControllerAttribute` | `DcaLayout.ToString` | Attribute marking API controllers. |
| `PageModelBase` | `ControllerBase` | Base class of page models (server-rendered pages without a controller). |
| `TransactionScope` | `ApiControllerAttribute` | Type used for explicit transaction demarcation. |

.NET has no injectable stereotype attribute; the Java rules that depend on one have no .NET reading and are listed as not applicable in the rule catalog.

## See also

- [DcaArchitecture](/reference/architecture.md)
