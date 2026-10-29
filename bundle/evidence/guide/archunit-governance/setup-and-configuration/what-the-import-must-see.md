---
type: Reference
title: Setup and Configuration — What the Import Must See
tags: [reference]
evidence_for: "/guide/archunit-governance/setup-and-configuration.md#what-the-import-must-see"
---

[Full node and context](/guide/archunit-governance/setup-and-configuration.md#what-the-import-must-see). This is an evidence excerpt; retain the parent selection and caveats.

### What the Import Must See

A rule can only report what the import found. `DcaArchitecture.load(layout)` reads the class path of
the running test and keeps every class below the base package — from the compiled classes of the
module under test and from jars alike. Jars matter: in a multi-module build every other module reaches
the test class path as a jar, and a module that is not imported has no contexts, no aggregates and no
violations. Every rule about it then passes.

Two mechanisms keep that silence from reading as success:

- `load` refuses an import that found no class below the base package. A misspelt base package and a
  test module that depends on no production module both end as a failed test with a message, not as a
  green suite.
- `DCA-STR-011` fails when no package declares `@BoundedContext`. The structural rules govern a module
  by its layers and need no declaration; the context-map and isolation rules select over the declared
  contexts, and without one they assert nothing. A code base that deliberately declares no context
  switches the rule off with a recorded reason.

The module that runs the architecture test therefore depends on every module that holds production
code. Where a third-party artifact ships the project's own base package, narrow the import instead of
widening the test module:

```java
DcaArchitecture.load(
    DcaLayout.forBasePackage("com.company.project"),
    ImportOption.Predefined.DO_NOT_INCLUDE_TESTS,
    ImportOption.Predefined.DO_NOT_INCLUDE_JARS);   // sibling modules are then excluded as well
```

In .NET the assemblies are named instead of found: `DcaArchitecture.Load(layout, assemblies)` reads
exactly what it is passed, so the test project references every production project and passes every
assembly. `Load` refuses a run whose assemblies hold no type below the root namespace, and
`DCA-STR-011` covers the missing declaration there under the same id.
