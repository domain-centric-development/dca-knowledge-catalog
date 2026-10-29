---
type: Rule
id: DCA-USE-002
title: Commands reside in the application layer
rule: "Use case commands should be in application layer (CQRS pattern)."
constraint: Commands reside in the application layer.
selects: Classes under the base package the configured command role recognises - by default a simple name ending with Command.
checks: "Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported."
enforced_by: "UseCaseRules#DCA-USE-002"
status: enforced
maturity: released
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/UseCaseRules.cs
---

# Commands reside in the application layer

## Selection

Classes under the base package the configured command role recognises - by default a simple name ending with Command.

## Check

Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported.

## .NET reading

**Selection.** Types under the root namespace the configured command role recognises - by default a simple name ending with Command.

**Check.** Each resides in an application namespace of some module root (<module>.Application). A Command in a domain, adapter or infrastructure namespace is reported.

## Implementation

```java
DcaRule.of(
        "DCA-USE-002",
        "Commands reside in the application layer",
        "Use case commands should be in application layer (CQRS pattern)",
        arch ->
            classes()
                .that(arch.layout().markers().is("command"))
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should(LayerConditions.be(arch.inApplication()))
                .allowEmptyShould(true))
    .selecting(
        "Classes under the base package the configured command role recognises - by default a"
            + " simple name ending with Command.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `inApplication()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
        "DCA-USE-002",
        "Commands reside in the application layer",
        "Use case commands should be in application layer (CQRS pattern)",
        arch =>
            Types()
                .That()
                .FollowCustomPredicate(t => arch.Layout.Markers.Is("Command", t), "are commands")
                .And()
                .ResideInNamespaceMatching(DcaLayout.Below(layout.RootNamespace))
                .Should()
                .FollowCustomCondition(LayerConditions.PlacedIn(arch.InApplication, "the application layer"), "be in the application layer"))
    .Selecting(
        "Types under the root namespace the configured command role recognises - by default a simple name"
            + " ending with Command.")
    .Checking(
        "Each resides in an application namespace of some module root"
            + " (<module>.Application). A Command in a domain, adapter or infrastructure"
            + " namespace is reported.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
