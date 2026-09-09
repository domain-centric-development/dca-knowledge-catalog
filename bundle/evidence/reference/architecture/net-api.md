---
type: Reference
title: DcaArchitecture — .NET API
tags: [reference]
evidence_for: "/reference/architecture.md#net-api"
---

[Full node and context](/reference/architecture.md#net-api). This is an evidence excerpt; retain the parent selection and caveats.

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
