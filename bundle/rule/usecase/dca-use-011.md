---
type: Rule
id: DCA-USE-011
title: DTOs must not be used in the Application Layer
rule: "Application layer should use Command/Query/Response models, not presentation DTOs (Clean Architecture)."
constraint: DTOs must not be used in the Application Layer.
selects: "Classes in <module>.application.. of every module root."
checks: "No dependency on a class whose simple name ends with Dto. Command, Query and Result models are not DTOs by this rule's definition - only the Dto suffix is checked."
enforced_by: "UseCaseRules#DCA-USE-011"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# DTOs must not be used in the Application Layer

## Selection

Classes in <module>.application.. of every module root.

## Check

No dependency on a class whose simple name ends with Dto. Command, Query and Result models are not DTOs by this rule's definition - only the Dto suffix is checked.

## .NET reading

**Selection.** Types in <module>.Application of every module root.

**Check.** No dependency on a type whose name ends with Dto. Command, Query and Result models are not DTOs by this rule's definition - only the Dto suffix is checked.

## Implementation

```java
DcaRule.of(
        "DCA-USE-011",
        "DTOs must not be used in the Application Layer",
        "Application layer should use Command/Query/Response models, not presentation DTOs (Clean"
            + " Architecture)",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .should()
                .dependOnClassesThat()
                .haveSimpleNameEndingWith("Dto")
                .allowEmptyShould(true))
    .selecting("Classes in <module>.application.. of every module root.")
    .checking(
        "No dependency on a class whose simple name ends with Dto. Command, Query and Result models are not DTOs by this rule's definition - only the Dto suffix is checked.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-011",
        "DTOs must not be used in the Application Layer",
        "Application layer should use Command/Query/Response models, not presentation DTOs (Clean Architecture)",
        arch =>
            Types()
                .That()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllApplicationPatterns()))
                .Should()
                .NotDependOnAnyTypesThat()
                .HaveNameEndingWith("Dto"))
    .Selecting(
        "Types in <module>.Application of every module root.")
    .Checking(
        "No dependency on a type whose name ends with Dto. Command, Query and Result"
            + " models are not DTOs by this rule's definition - only the Dto suffix is checked.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
