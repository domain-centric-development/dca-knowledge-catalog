---
type: Rule
id: DCA-USE-003
title: "Types named *Query reside in the application layer"
rule: "Use case queries should be in application layer (CQRS pattern)."
constraint: "Types named *Query reside in the application layer."
selects: Classes under the base package whose simple name ends with Query.
checks: "Each resides in an application package of some module root (<module>.application..)."
enforced_by: "UseCaseRules#DCA-USE-003"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Types named *Query reside in the application layer

## Selection

Classes under the base package whose simple name ends with Query.

## Check

Each resides in an application package of some module root (<module>.application..).

## .NET reading

**Selection.** Types under the root namespace whose name ends with Query.

**Check.** Each resides in an application namespace of some module root (<module>.Application).

## Implementation

```java
DcaRule.of(
        "DCA-USE-003",
        "Types named *Query reside in the application layer",
        "Use case queries should be in application layer (CQRS pattern)",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Query")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Query.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..).")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-003",
        "Types named *Query reside in the application layer",
        "Use case queries should be in application layer (CQRS pattern)",
        arch =>
            Types()
                .That()
                .HaveNameEndingWith("Query")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllApplicationPatterns())))
    .Selecting(
        "Types under the root namespace whose name ends with Query.")
    .Checking(
        "Each resides in an application namespace of some module root"
            + " (<module>.Application).")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
