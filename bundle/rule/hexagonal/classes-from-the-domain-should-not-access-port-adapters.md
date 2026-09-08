---
type: Rule
id: DCA-HEX-001
title: Classes from the domain should not access port adapters
rule: "Domain should not depend on adapters (ports and adapters pattern)."
constraint: Classes from the domain should not access port adapters.
selects: "Classes in <module>.domain.model.. of every module root - the domain model package, not the whole domain layer."
checks: "No dependency on a class in <module>.adapter.. of any module root, incoming or outgoing. Domain classes outside the model package (domain services, events) are not selected. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-001"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Classes in <module>.domain.model.. of every module root - the domain model package, not the whole domain layer.

## Check

No dependency on a class in <module>.adapter.. of any module root, incoming or outgoing. Domain classes outside the model package (domain services, events) are not selected. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Domain.Model of every module root - the domain model namespace, not the whole domain layer.

**Check.** No dependency on a type in <module>.Adapter of any module root, incoming or outgoing. Domain types outside the model namespace (domain services, events) are not selected. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-001",
        "Classes from the domain should not access port adapters",
        "Domain should not depend on adapters (ports and adapters pattern)",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .should()
                .dependOnClassesThat()
                .resideInAnyPackage(arch.allAdapterPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.model.. of every module root - the domain model"
            + " package, not the whole domain layer.")
    .checking(
        "No dependency on a class in <module>.adapter.. of any module root, incoming or"
            + " outgoing. Domain classes outside the model package (domain services, events) are"
            + " not selected. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()`, `allDomainModelPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
