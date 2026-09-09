---
type: Reference
title: DcaArchitecture
subject: architecture
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/DcaArchitecture.java
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/DcaArchitecture.cs
tags: [reference, archunit, archunitnet]
---

The classes under test together with the `t` that describes them, plus the
discovery helpers every DCA rule builds on: which packages are bounded contexts, where the shared
kernel lives, which annotations a `package-info` carries.

Create one instance per test run and pass it to every rule — class import and context
discovery are cached.

## How the rules find their subjects (Java)

- **Bounded contexts** are declared: a package whose `package-info` carries `@BoundedContext`, at any depth below the base package. `boundedContexts()` lists them; `contextName(...)` names one relative to the base package (`sales.order`).
- **The shared kernel** is the package carrying `@SharedKernel` (`sharedKernelPackage()`).
- **Module roots** are structural: the shortest package prefix below the base package whose next segment is a layer segment (`domain`, `application`, `adapter`). No annotation is needed, so a module that is deliberately not a bounded context is still governed by the layer rules. The shared kernel is a module root when it owns a layer; `isolatedModuleRoots()` is every module root except the shared kernel.
- The `all*Patterns()` accessors expand over **module roots**, the `context*Patterns()` accessors over **declared bounded contexts**. Rule nodes name the accessors they use under *Architecture queries*.

## Java API: `DcaArchitecture`

### Construction and access

#### `static DcaArchitecture load(DcaLayout layout)`

Imports all production classes below the layout's base package (excluding tests, jars and
archives) using the class path of the calling test.

#### `static DcaArchitecture of(DcaLayout layout, JavaClasses classes)`

Wraps already imported classes — for tests and custom importers.

#### `DcaLayout layout()`

#### `JavaClasses classes()`

### Bounded-context discovery

#### `Map<String, BoundedContext> boundedContexts()`

All packages whose `package-info` carries `t`, keyed by package name,
in encounter order. Discovery is by annotation, so a context may sit at any depth below the
base package — see `rootContextPackage(String)`.

#### `List<String> boundedContextPackages()`

Package names of all bounded contexts (no pattern suffix).

#### `String[] boundedContextPatterns()`

Bounded-context patterns, e.g. `com.acme.shop.cart..`.

#### `String[] boundedContextPatternsExcluding(String contextPackage)`

Bounded-context patterns without the given context package.

#### `Optional<String> sharedKernelPackage()`

The package annotated with `l`, at whatever depth below the base package it
sits.

#### `String rootContextPackage(String fullPackageName)`

The root package of the bounded context (or shared kernel) that a fully qualified package
belongs to — the nearest ancestor at or below the base package whose `package-info`
carries `t` or `l`.

Because the declaration is the annotation and not the position in the tree, a context may
sit at any depth: `com.acme.shop.cart.domain.model → com.acme.shop.cart` when `cart` is annotated, and `com.acme.shop.sales.order.domain.model → com.acme.shop.sales.order` when `sales.order` is. A single-context application may
annotate the base package itself.

Falls back to the direct sub-package of the base package when no ancestor is annotated, so
that a project which has not declared its contexts yet still groups classes the way it used to.
Such a package is not a discovered context; whether it owns layers — and is therefore governed
— is decided structurally by `moduleRoots()`, not by this fallback.

#### `String contextName(String contextPackage)`

The identifier of a context package: its name relative to the base package, e.g. `com.acme.shop.cart → cart` and `com.acme.shop.sales.order → sales.order`.

This is the name a context is referenced by in `@Upstream(context = ...)`, in the
rendered context map, and in rule messages. It deliberately matches the identifier a module
system derives from the package tree - the package name trailing the base package - so a module
declaration and the context map agree without a mapping layer. For a context that is a direct
child of the base package it is the last segment, so nothing changes for a flat layout; grouped
contexts keep their group in the name, which is also what makes them unambiguous — two contexts
named `order` under different groups would otherwise collide.

#### `static String simpleContextName(String contextPackage)`

Last segment of a package: `com.acme.shop.cart → cart`.

### package-info annotations

#### `<T extends Annotation> Optional<T> packageAnnotation(String packageName, Class<T> annotationType)`

A single annotation from the package's `package-info` class, if present.

#### `<T extends Annotation> List<T> packageAnnotations(String packageName, Class<T> annotationType)`

All instances of a repeatable annotation from the package's `package-info` class.

### Module discovery — structural, unlike context discovery

#### `List<String> moduleRoots()`

Every package that owns a DCA layer, in encounter order — the roots the layer rules apply to.

**Why this is not the same as `boundedContexts()`.** Being a bounded context is a
strategic statement: it is declared with `@BoundedContext` and it decides isolation, the
context map, upstream relationships. Owning a `domain`/`application`/`adapter` layer is a structural fact, and the layer rules — the domain knows no infrastructure,
transactions are an application concern, a `Command` lives in `application` — apply
to it either way. A module that is deliberately *not* a bounded context (an operational
backoffice reading other contexts' data, say) still follows DCA layering and must still be
governed.

A root is the **shortest** package prefix at or below the base package whose remainder
starts with a layer segment. Shortest wins so that an adapter's own `domain` package — an
outgoing adapter mapping to a foreign model — stays inside its module instead of becoming a
root of its own: for `base.cart.adapter.outgoing.domain.Foo` the root is `base.cart`, not `base.cart.adapter.outgoing`.

Because the test is structural, a module is found at any depth and without any annotation —
which is what keeps a grouped or nested layout governed. The isolation rules select over module
roots as well (`isolatedModuleRoots()`), so a module that declares nothing can neither
reach into a neighbour's internals nor have its own internals reached into. Declaring a module
a bounded context decides its place on the context map, nothing more.

#### `List<String> isolatedModuleRoots()`

The module roots the isolation rules govern: every module root except the shared kernel. The
shared kernel is a module root too (it may own `domain`, `application` and `adapter` packages), but everyone may depend on it, and what *it* may depend on is `DCA-STR-002`'s business.

#### `String[] moduleRootPatternsExcluding(String moduleRoot)`

Package patterns of every isolated module root except the given one — `root..` each.
Built from `isolatedModuleRoots()`, so an undeclared module is a forbidden target like
any other, not only a governed source.

#### `String[] publishedPackagePatternsExcluding(String moduleRoot)`

The published packages of every isolated module root except the given one: `root.api..`
(synchronous, in-process) and `root.events..` (asynchronous), with the segment names
taken from `publishedSubpackages()`. These are DCA's in-process contract
convention — package names, a convention of the architecture and not of any framework — and the
only part of a foreign module an adapter may depend on.

#### `java.util.Set<String> layerSegments()`

The layer sub-package names of this layout: `domain`, `application`, `adapter`.

#### `String moduleRootOf(String packageName)`

The module root of a package, or `null` when the package carries no layer segment — the
global infrastructure package, for instance, or a plain support package.

### Pattern helpers: context* over declared bounded contexts, all* over module roots

#### `String[] contextDomainPatterns()`

#### `String[] contextDomainModelPatterns()`

#### `String[] contextApplicationPatterns()`

#### `String[] contextAdapterPatterns()`

#### `String[] allApplicationPatterns()`

Application-layer patterns of every module root — the discovery equivalent of the former `base.*.application..` wildcard, which matched a direct child of the base package and nothing
else. Built from `moduleRoots()`, so it holds at any depth.

#### `String[] allAdapterPatterns()`

Adapter patterns of every module root.

#### `String[] allSharedOutputPortPatterns()`

Shared-output-port patterns (`application.shared`) of every module root.

#### `String[] allDomainPatterns()`

Domain-layer patterns of every module root.

#### `String[] allDomainModelPatterns()`

Domain-model patterns of every module root.

#### `String[] allIncomingAdapterPatterns()`

Incoming-adapter patterns of every module root.

#### `String[] allOutgoingAdapterPatterns()`

Outgoing-adapter patterns of every module root.

#### `List<String> infrastructurePackages()`

The infrastructure packages of this architecture: the global one (`base.infrastructure`)
and every isolated module's own (`base.cart.infrastructure`), each without pattern
suffix. A module's infrastructure is not a layer — it does not make the module a root — but it
is an implementation detail like the global one, and the rules that keep implementation details
out of the inner layers treat both alike.

The shared kernel's `infrastructure` package is deliberately not in this list. The
shared kernel is the one package everyone may depend on; what it keeps under `infrastructure` — a project-wide lifecycle annotation, say — is shared support, not a detail of
one module that another module's adapter would be reaching into.

#### `String[] allInfrastructurePatterns()`

`infrastructurePackages()` as patterns, `package..` each.

#### `DescribedPredicate<JavaClass> infrastructureImplementation()`

Classes residing in an infrastructure package — the package itself or any sub-package, with an
exact segment boundary: `base.infrastructure.Wiring` counts, `base.infrastructurex.Other` does not.

#### `List<String> packagesBelowBase()`

Every package at or below the base package that an imported class lives in, together with all
its ancestors down to the base package, in encounter order. This is the set of packages that
may carry a `package-info` declaration.

#### `static boolean inPackageTree(String packageName, String root)`

True when `packageName` is `root` itself or a sub-package of it.

## .NET twin: `DcaArchitecture` in `DomainCentric.ArchRules`

The types under test together with the `DcaLayout` that describes them, plus the
discovery helpers every DCA rule builds on: which namespaces are bounded contexts, where the shared
kernel lives, which context-level attributes a namespace carries.

Create one instance per test run and pass it to every rule — the ArchUnitNET import and the
context discovery are cached.

Context-level declarations (`[BoundedContext]`, `[SharedKernel]`, `[Upstream]`, …)
are read with reflection from a *marker class* that resides directly in the context's root
namespace — the .NET stand-in for Java's `package-info`. Therefore the assemblies passed to
`Load(DcaLayout, Assembly[])` must be the loaded runtime assemblies.

### .NET API

| Member | Summary |
|---|---|
| `static DcaArchitecture Load(DcaLayout layout, params Assembly[] assemblies)` | Imports every type of the given assemblies that resides in the layout's root namespace (or below). Pass the production assemblies of the application, e.g. `typeof(Program).Assembly` or one assembly per bounded context.  **Run architecture tests against Debug builds.** In a Release build the C# compiler emits async state machines as structs, and ArchUnitNET drops those compiler-generated value types — every dependency that occurs only inside an `async` method body becomes invisible to dependency rules. In a Debug build the state machine is a class whose dependencies ArchUnitNET attributes to the declaring type. This method therefore refuses JIT-optimized assemblies; use `Load(DcaLayout, bool, Assembly[])` with `allowOptimizedAssemblies: true` to accept the blind spot knowingly. |
| `static DcaArchitecture Load(DcaLayout layout, bool allowOptimizedAssemblies, params Assembly[] assemblies)` | Like `Load(DcaLayout, Assembly[])`; with `allowOptimizedAssemblies` set, Release-built assemblies are accepted although dependencies inside `async` method bodies are then not analysed. |
| `static DcaArchitecture Of(DcaLayout layout, Architecture architecture, params Assembly[] assemblies)` | Wraps an already built ArchUnitNET architecture — for tests and custom loaders. |
| `DcaLayout Layout` |  |
| `Architecture Architecture` | The ArchUnitNET model of the imported types. |
| `IEnumerable<IType> Types` | Imported types below the root namespace (ArchUnitNET model, referenced types excluded). |
| `IEnumerable<Class> Classes` | Imported classes below the root namespace. |
| `IEnumerable<Interface> Interfaces` | Imported interfaces below the root namespace. |
| `IReadOnlyDictionary<string, BoundedContextAttribute> BoundedContexts` | All namespaces at or below the root namespace that carry a `[BoundedContext]` marker class, keyed by namespace, in encounter order. A context may sit at any depth (`Acme.Shop.Cart`, `Acme.Shop.Sales.Order`, or the root namespace itself); the declaration is the attribute, not the position in the namespace tree. |
| `IReadOnlyList<string> BoundedContextNamespaces` | Namespaces of all bounded contexts (plain names). |
| `string[] BoundedContextPatterns()` | Bounded-context patterns, e.g. the regex for `Acme.Shop.Cart` and below. |
| `string[] BoundedContextPatternsExcluding(string contextNamespace)` | Bounded-context patterns without the given context namespace. |
| `string? SharedKernelNamespace` | The namespace, at whatever depth below the root, whose marker class carries `[SharedKernel]`. |
| `string? RootContextNamespace(string fullNamespace)` | The root namespace of the bounded context (or shared kernel) a full namespace belongs to — the nearest ancestor at or below the root namespace whose marker class carries `[BoundedContext]` or `[SharedKernel]`: `Acme.Shop.Cart.Domain.Model → Acme.Shop.Cart` when `Cart` is declared, `Acme.Shop.Sales.Order.Domain.Model → Acme.Shop.Sales.Order` when `Sales.Order` is.  Falls back to the direct child namespace of the root when no ancestor is declared, so that a project which has not declared its contexts yet still groups types the way it used to. Such a namespace is not a discovered context; whether it owns layers — and is therefore governed — is decided structurally by `ModuleRoots`, not by this fallback.  the context root namespace, or `null` for namespaces outside the root namespace |
| `string ContextName(string contextNamespace)` | The identifier of a context: its namespace relative to the root namespace — `Acme.Shop.Cart → Cart`, `Acme.Shop.Sales.Order → Sales.Order`. For a single-context application whose root namespace is the context, the root's last segment. Unambiguous for grouped contexts, where the last segment alone would not be; identical to the last segment for a context that is a direct child of the root, so existing `[Upstream("Cart")]` declarations keep working. |
| `static string SimpleContextName(string contextNamespace)` | Last segment of a namespace: `Acme.Shop.Cart → Cart`.  A context identifier is its name relative to the root namespace — use `ContextName`, which is unambiguous for grouped contexts. This method stays for the case where only a last segment is wanted. |
| `IReadOnlyList<string> ModuleRoots()` | Every namespace that owns a DCA layer, in encounter order — the roots the layer rules apply to.  **Why this is not the same as `BoundedContexts`.** Being a bounded context is a strategic statement: it is declared with `[BoundedContext]` and it decides the context map and the upstream relationships. Owning a `Domain`/`Application`/`Adapter` layer is a structural fact, and the layer rules — the domain knows no infrastructure, transactions are an application concern, a `Command` lives in `Application` — apply to it either way. A module that is deliberately *not* a bounded context still follows DCA layering and must still be governed.  A root is the **shortest** namespace prefix at or below the root namespace whose remainder starts with a layer segment. Shortest wins so that an adapter's own `Domain` namespace — an outgoing adapter mapping to a foreign model — stays inside its module instead of becoming a root of its own: for `Root.Cart.Adapter.Outgoing.Domain.Foo` the root is `Root.Cart`.  Because the test is structural, a module is found at any depth and without any attribute — which is what keeps a grouped or nested layout governed. The isolation rules select over module roots as well (`IsolatedModuleRoots`), so a module that declares nothing can neither reach into a neighbour's internals nor have its own internals reached into. Declaring a module a bounded context decides its place on the context map, nothing more. |
| `ISet<string> LayerSegments()` | The layer segments of this layout: `Domain`, `Application`, `Adapter`. |
| `string? ModuleRootOf(string ns)` | The module root of a namespace, or `null` when the namespace carries no layer segment — the global infrastructure namespace, for instance, or a plain support namespace. |
| `IReadOnlyList<string> IsolatedModuleRoots()` | The module roots the isolation rules govern: every module root except the shared kernel. The shared kernel is a module root too (it may own `Domain`, `Application` and `Adapter` namespaces), but everyone may depend on it, and what *it* may depend on is `DCA-STR-002`'s business. |
| `string[] ModuleRootPatternsExcluding(string moduleRoot)` | Patterns of every isolated module root except the given one — `root` and below, each. Built from `IsolatedModuleRoots`, so an undeclared module is a forbidden target like any other, not only a governed source. |
| `string[] PublishedPatternsExcluding(string moduleRoot)` | The published namespaces of every isolated module root except the given one: `root.Api` (synchronous, in-process) and `root.Events` (asynchronous) and below, with the segment names taken from `PublishedSegments`. DCA's in-process contract convention — namespace names, a convention of the architecture and not of any framework — and the only part of a foreign module an adapter may depend on. |
| `T? NamespaceAttribute<T>(string ns)` | The single attribute of type  declared on a marker class residing exactly in `ns`, or `null`. |
| `IReadOnlyList<T> NamespaceAttributes<T>(string ns)` | All attributes of type  declared on classes residing exactly in `ns` (repeatable attributes such as `[Upstream]`). |
| `IReadOnlyList<Type> RuntimeTypes()` | The runtime `Type`s of the loaded assemblies below the root namespace. |
| `Type? RuntimeType(IType type)` | The runtime `Type` behind an ArchUnitNET type, or `null` when it is not in the loaded assemblies. |
| `static bool IsJitOptimized(Assembly assembly)` | Whether the assembly was compiled with optimizations (Release) according to its `DebuggableAttribute`. |
| `string[] ContextDomainPatterns()` |  |
| `string[] ContextDomainModelPatterns()` |  |
| `string[] ContextApplicationPatterns()` |  |
| `string[] ContextAdapterPatterns()` |  |
| `string[] AllDomainPatterns()` | Domain patterns of every module root — the layer rules' selection, at any depth. |
| `string[] AllDomainModelPatterns()` | Domain-model patterns of every module root. |
| `string[] AllApplicationPatterns()` | Application patterns of every module root. |
| `string[] AllSharedOutputPortPatterns()` | Shared-output-port patterns (`Application.Shared`) of every module root. |
| `string[] AllAdapterPatterns()` | Adapter patterns of every module root. |
| `string[] AllIncomingAdapterPatterns()` | Incoming-adapter patterns of every module root (contexts, shared kernel and undeclared modules alike). |
| `string[] AllOutgoingAdapterPatterns()` | Outgoing-adapter patterns of every module root. |
| `string[] AllDomainPatternsWithSharedKernel()` | Domain patterns of every module root — the shared kernel is a module root when it owns a domain layer. |
| `string[] AllDomainModelPatternsWithSharedKernel()` | Domain-model patterns of every module root. |
| `IReadOnlyList<string> InfrastructureNamespaces()` | The infrastructure namespaces of this architecture: the global one (`Root.Infrastructure`) and every isolated module's own (`Root.Cart.Infrastructure`), each without pattern. A module's infrastructure is not a layer — it does not make the module a root — but it is an implementation detail like the global one, and the rules that keep implementation details out of the inner layers treat both alike. The shared kernel's `Infrastructure` namespace is deliberately not listed: the shared kernel is the one namespace everyone may depend on, and what it keeps there is shared support, not a detail of one module. |
| `string[] AllInfrastructurePatterns()` | `InfrastructureNamespaces` as patterns, each namespace and below. |
| `bool IsInfrastructureImplementation(IType type)` | Whether a type resides in an infrastructure namespace — the namespace itself or below, with an exact segment boundary: `Root.Infrastructure.Wiring` counts, `Root.InfrastructureX.Other` does not. |
| `IReadOnlyList<string> NamespacesBelowRoot()` | Every namespace at or below the root namespace that a loaded type lives in, together with all its ancestors down to the root namespace, in encounter order — the set of namespaces that may carry a marker class with context-map declarations. |

## See also

- [DcaLayout](/reference/layout.md)

## Evidence slices

- [Overview](/evidence/reference/architecture/overview.md)
- [Construction and access](/evidence/reference/architecture/construction-and-access.md)
- [Bounded-context discovery](/evidence/reference/architecture/bounded-context-discovery.md)
- [package-info annotations](/evidence/reference/architecture/package-info-annotations.md)
- [Module discovery — structural, unlike context discovery](/evidence/reference/architecture/module-discovery-structural-unlike-context-discovery.md)
- [Pattern helpers: context* over declared bounded contexts, all* over module roots](/evidence/reference/architecture/pattern-helpers-context-over-declared-bounded-contexts-all-over-module-roots.md)
- [.NET API](/evidence/reference/architecture/net-api.md)
