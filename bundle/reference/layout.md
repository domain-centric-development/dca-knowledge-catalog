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
| `restControllerSuffix` | `Resource` | `withRestControllerSuffix(...)` | Suffix of REST controllers, e.g. `"Resource"` or `"Controller"`. |

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

## Framework annotations the rules look for (Java, `FrameworkAnnotations.spring()`)

Annotations are matched by fully qualified name; the rule library has no framework dependency. Replace the set with `withFrameworkAnnotations(FrameworkAnnotations.of(...))` for another container.

| Role | Default annotation | Used for |
|---|---|---|
| `service` | `org.springframework.stereotype.Service` | stereotype for application services / use-case beans |
| `component` | `org.springframework.stereotype.Component` | generic component stereotype |
| `controller` | `org.springframework.stereotype.Controller` | MVC controller stereotype |
| `restController` | `org.springframework.web.bind.annotation.RestController` | REST controller stereotype |
| `transactional` | `org.springframework.transaction.annotation.Transactional` | transaction demarcation |
| `eventListener` | `org.springframework.context.event.EventListener` | in-process event listener |
| `applicationModule` | `org.springframework.modulith.ApplicationModule` | module declaration on `package-info` (Spring Modulith's `@ApplicationModule`); may be `null` when the project uses no module system |

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

| Role | Default type | Used for |
|---|---|---|
| `ControllerBase` | `Microsoft.AspNetCore.Mvc.ControllerBase` | Base class of MVC / API controllers. |
| `ApiControllerAttribute` | `Microsoft.AspNetCore.Mvc.ApiControllerAttribute` | Attribute marking API controllers. |
| `PageModelBase` | `Microsoft.AspNetCore.Mvc.RazorPages.PageModel` | Base class of Razor Pages page models. |
| `TransactionScope` | `System.Transactions.TransactionScope` | Type used for explicit transaction demarcation. |

.NET has no `@Service`/`@Component`-style stereotypes; the Java rules that depend on them have no .NET reading and are listed as not applicable in the rule catalog.

## See also

- [DcaArchitecture](/reference/architecture.md)
