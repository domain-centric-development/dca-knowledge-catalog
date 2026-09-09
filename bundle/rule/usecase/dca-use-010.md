---
type: Rule
id: DCA-USE-010
title: DTOs must not be used in the Domain Layer
rule: "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle."
constraint: DTOs must not be used in the Domain Layer.
selects: "Classes in <module>.domain.. of every module root."
checks: No dependency on a class whose simple name ends with Dto.
enforced_by: "UseCaseRules#DCA-USE-010"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# DTOs must not be used in the Domain Layer

## Selection

Classes in <module>.domain.. of every module root.

## Check

No dependency on a class whose simple name ends with Dto.

## .NET reading

**Selection.** Types in <module>.Domain of every module root.

**Check.** No dependency on a type whose name ends with Dto.

## Implementation

```java
DcaRule.of(
        "DCA-USE-010",
        "DTOs must not be used in the Domain Layer",
        "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion"
            + " Principle",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should()
                .dependOnClassesThat()
                .haveSimpleNameEndingWith("Dto")
                .allowEmptyShould(true))
    .selecting("Classes in <module>.domain.. of every module root.")
    .checking("No dependency on a class whose simple name ends with Dto.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-010",
        "DTOs must not be used in the Domain Layer",
        "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle",
        arch =>
            Types()
                .That()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns()))
                .Should()
                .NotDependOnAnyTypesThat()
                .HaveNameEndingWith("Dto"))
    .Selecting(
        "Types in <module>.Domain of every module root.")
    .Checking(
        "No dependency on a type whose name ends with Dto.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
