---
type: Reference
title: DcaArchitecture — Bounded-context discovery
tags: [reference]
evidence_for: "/reference/architecture.md#bounded-context-discovery"
---

[Full node and context](/reference/architecture.md#bounded-context-discovery). This is an evidence excerpt; retain the parent selection and caveats.

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
