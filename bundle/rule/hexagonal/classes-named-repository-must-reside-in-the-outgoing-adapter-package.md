---
type: Rule
id: DCA-HEX-008
title: "Classes named *Repository must reside in the outgoing adapter package"
rule: "Repository implementations are secondary adapters (outgoing ports)."
constraint: "Classes named *Repository must reside in the outgoing adapter package."
selects: Non-interface classes anywhere on the classpath under scan whose simple name ends with Repository - implementations and abstract base classes alike. The Repository port interfaces themselves are not selected.
checks: "Each resides in <module>.adapter.outgoing.. of some module root. Whether the class implements a Repository port is not checked - only the name is. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-008"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan whose simple name ends with Repository - implementations and abstract base classes alike. The Repository port interfaces themselves are not selected.

## Check

Each resides in <module>.adapter.outgoing.. of some module root. Whether the class implements a Repository port is not checked - only the name is. An empty selection passes.

## .NET reading

**Selection.** Classes anywhere in the loaded assemblies whose name ends with Repository - implementations and abstract base classes alike. The IRepository port interfaces themselves are not selected.

**Check.** Each resides in <module>.Adapter.Outgoing of some module root. Whether the class implements an IRepository port is not checked - only the name is. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-008",
        "Classes named *Repository must reside in the outgoing adapter package",
        "Repository implementations are secondary adapters (outgoing ports)",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Repository")
                .and()
                .areNotInterfaces()
                .should()
                .resideInAnyPackage(arch.allOutgoingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan whose simple name"
            + " ends with Repository - implementations and abstract base classes alike. The"
            + " Repository port interfaces themselves are not selected.")
    .checking(
        "Each resides in <module>.adapter.outgoing.. of some module root. Whether the"
            + " class implements a Repository port is not checked - only the name is. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allOutgoingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
