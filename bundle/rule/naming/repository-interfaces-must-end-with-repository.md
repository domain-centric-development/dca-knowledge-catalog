---
type: Rule
id: DCA-NAM-004
title: Repository Interfaces must end with 'Repository'
rule: "Repository interfaces should follow consistent naming conventions (DDD pattern)."
constraint: Repository Interfaces must end with 'Repository'.
selects: "Interfaces in <module>.application.. of every module root whose simple name contains Repository, except one named exactly Repository."
checks: "The simple name ends with Repository (RepositoryPort or ProductRepositoryAdapter is reported). Selection is by name only - whether the interface extends the Repository marker is not checked, and classes are not selected. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-004"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Interfaces in <module>.application.. of every module root whose simple name contains Repository, except one named exactly Repository.

## Check

The simple name ends with Repository (RepositoryPort or ProductRepositoryAdapter is reported). Selection is by name only - whether the interface extends the Repository marker is not checked, and classes are not selected. An empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root whose name contains Repository, except one named exactly Repository or IRepository.

**Check.** The name ends with Repository (IRepositoryPort or IProductRepositoryAdapter is reported). Selection is by name only - whether the interface extends the IRepository marker is not checked, and classes are not selected. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-004",
        "Repository Interfaces must end with 'Repository'",
        "Repository interfaces should follow consistent naming conventions (DDD pattern)",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areInterfaces()
                .and()
                .haveSimpleNameContaining("Repository")
                .and()
                .doNotHaveSimpleName("Repository")
                .should()
                .haveSimpleNameEndingWith("Repository")
                .allowEmptyShould(true))
    .selecting(
        "Interfaces in <module>.application.. of every module root whose simple name contains"
            + " Repository, except one named exactly Repository.")
    .checking(
        "The simple name ends with Repository (RepositoryPort or ProductRepositoryAdapter is"
            + " reported). Selection is by name only - whether the interface extends the"
            + " Repository marker is not checked, and classes are not selected. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
