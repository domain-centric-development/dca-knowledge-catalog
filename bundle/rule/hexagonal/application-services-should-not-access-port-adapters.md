---
type: Rule
id: DCA-HEX-002
title: Application Services should not access port adapters
rule: "Application services should only depend on domain and outbound ports, not adapters."
constraint: Application Services should not access port adapters.
selects: "Classes in <module>.application.. of every module root, application.shared included."
checks: "No dependency on a class in <module>.adapter.. of any module root. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-002"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Classes in <module>.application.. of every module root, application.shared included.

## Check

No dependency on a class in <module>.adapter.. of any module root. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Application of every module root, Application.Shared included.

**Check.** No dependency on a type in <module>.Adapter of any module root. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-002",
        "Application Services should not access port adapters",
        "Application services should only depend on domain and outbound ports, not adapters",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(arch.allAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.application.. of every module root, application.shared"
            + " included.")
    .checking(
        "No dependency on a class in <module>.adapter.. of any module root. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()`, `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
