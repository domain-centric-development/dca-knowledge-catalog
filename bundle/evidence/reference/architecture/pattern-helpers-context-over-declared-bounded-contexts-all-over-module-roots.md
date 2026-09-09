---
type: Reference
title: "DcaArchitecture — Pattern helpers: context* over declared bounded contexts, all* over module roots"
tags: [reference]
evidence_for: "/reference/architecture.md#pattern-helpers-context-over-declared-bounded-contexts-all-over-module-roots"
---

[Full node and context](/reference/architecture.md#pattern-helpers-context-over-declared-bounded-contexts-all-over-module-roots). This is an evidence excerpt; retain the parent selection and caveats.

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
