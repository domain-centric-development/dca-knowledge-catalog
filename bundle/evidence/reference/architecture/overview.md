---
type: Reference
title: DcaArchitecture — Overview
tags: [reference]
evidence_for: /reference/architecture.md
---

[Full node and context](/reference/architecture.md). This is an evidence excerpt; retain the parent selection and caveats.

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
