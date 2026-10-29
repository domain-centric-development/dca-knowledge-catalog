---
type: Rule
id: DCA-USE-003
title: Queries reside in the application layer
rule: "Use case queries should be in application layer (CQRS pattern)."
constraint: Queries reside in the application layer.
selects: Classes under the base package the configured query role recognises - by default a simple name ending with Query.
checks: "Each resides in an application package of some module root (<module>.application..)."
enforced_by: "UseCaseRules#DCA-USE-003"
status: enforced
maturity: released
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Queries reside in the application layer

## Selection

Classes under the base package the configured query role recognises - by default a simple name ending with Query.

## Check

Each resides in an application package of some module root (<module>.application..).

## .NET reading

**Selection.** Types under the root namespace the configured query role recognises - by default a simple name ending with Query.

**Check.** Each resides in an application namespace of some module root (<module>.Application).

## Implementation

```java
DcaRule.of(
        "DCA-USE-003",
        "Queries reside in the application layer",
        "Use case queries should be in application layer (CQRS pattern)",
        arch ->
            classes()
                .that(arch.layout().markers().is("query"))
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should(LayerConditions.be(arch.inApplication()))
                .allowEmptyShould(true))
    .selecting(
        "Classes under the base package the configured query role recognises - by default a"
            + " simple name ending with Query.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..).")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-003",
        "Queries reside in the application layer",
        "Use case queries should be in application layer (CQRS pattern)",
        arch =>
            Types()
                .That()
                .FollowCustomPredicate(t => arch.Layout.Markers.Is("Query", t), "are queries")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .FollowCustomCondition(LayerConditions.PlacedIn(arch.InApplication, "the application layer"), "be in the application layer"))
    .Selecting(
        "Types under the root namespace the configured query role recognises - by default a simple name"
            + " ending with Query.")
    .Checking(
        "Each resides in an application namespace of some module root"
            + " (<module>.Application).")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
