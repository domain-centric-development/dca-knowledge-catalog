---
type: Reference
title: "DcaArchitecture — Module discovery — structural, unlike context discovery"
tags: [reference]
evidence_for: "/reference/architecture.md#module-discovery--structural-unlike-context-discovery"
---

[Full node and context](/reference/architecture.md#module-discovery--structural-unlike-context-discovery). This is an evidence excerpt; retain the parent selection and caveats.

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
