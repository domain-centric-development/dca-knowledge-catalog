---
type: Rule
id: DCA-NAM-004
title: "Repository Interfaces must end with 'Repository' (name-based discovery)"
rule: "Repository interfaces should follow consistent naming conventions (DDD pattern)."
constraint: "Repository Interfaces must end with 'Repository' (name-based discovery)."
selects: "Interfaces in <module>.application.. of every module root whose simple name contains Repository, except one named exactly Repository."
checks: "The simple name ends with Repository (RepositoryPort or ProductRepositoryAdapter is reported). Selection is by name only - whether the interface extends the Repository marker is not checked, and classes are not selected. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-004"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/NamingRules.cs
---

# Repository Interfaces must end with 'Repository' (name-based discovery)

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
        "Repository Interfaces must end with 'Repository' (name-based discovery)",
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
### C# expression

```csharp
DcaRule.Check(
        "DCA-NAM-004",
        "Repository Interfaces must end with 'Repository' (name-based discovery)",
        "Repository interfaces should follow consistent naming conventions (DDD pattern)",
        arch =>
        {
            var violations = arch.Interfaces
                .Where(i => InNamespace(i, DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                    && i.Name.Contains("Repository", StringComparison.Ordinal)
                    && i.Name != "Repository"
                    && i.Name != "IRepository"
                    && !i.Name.EndsWith("Repository", StringComparison.Ordinal))
                .Select(i => $"{i.FullName} does not end with 'Repository'")
                .ToList();
            DcaRule.Fail("Repository Interfaces must end with 'Repository'", violations, "rename the interface to I<Aggregate>Repository");
        })
    .Selecting(
        "Interfaces in <module>.Application of every module root whose name contains"
            + " Repository, except one named exactly Repository or IRepository.")
    .Checking(
        "The name ends with Repository (IRepositoryPort or IProductRepositoryAdapter is"
            + " reported). Selection is by name only - whether the interface extends the"
            + " IRepository marker is not checked, and classes are not selected. An empty"
            + " selection passes.")
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
