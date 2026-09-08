---
type: Rule
id: DCA-TAC-013
title: Repository Interfaces should extend Repository Marker Interface
rule: Repository interfaces should extend Repository marker interface.
constraint: Repository Interfaces should extend Repository Marker Interface.
selects: "Interfaces in <module>.application.. of every module root whose simple name ends with Repository, the marker Repository itself excluded."
checks: "The interface is assignable to the Repository marker. A *Repository interface outside <module>.application.. is not selected; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-013"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Interfaces in <module>.application.. of every module root whose simple name ends with Repository, the marker Repository itself excluded.

## Check

The interface is assignable to the Repository marker. A *Repository interface outside <module>.application.. is not selected; an empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root whose name ends with Repository; interfaces named exactly Repository or IRepository excluded.

**Check.** The interface is assignable to the IRepository marker. A *Repository interface elsewhere is not selected; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-013",
        "Repository Interfaces should extend Repository Marker Interface",
        "Repository interfaces should extend Repository marker interface",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areInterfaces()
                .and()
                .haveSimpleNameEndingWith(REPOSITORY_SUFFIX)
                .and()
                .doNotHaveSimpleName(REPOSITORY_SUFFIX)
                .should()
                .beAssignableTo(Repository.class)
                .allowEmptyShould(true))
    .selecting(
        "Interfaces in <module>.application.. of every module root whose simple name "
            + "ends with Repository, the marker Repository itself excluded.")
    .checking(
        "The interface is assignable to the Repository marker. A *Repository interface "
            + "outside <module>.application.. is not selected; an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
