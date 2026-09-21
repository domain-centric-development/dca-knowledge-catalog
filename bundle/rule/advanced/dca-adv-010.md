---
type: Rule
id: DCA-ADV-010
title: Marked domain services reside in a module domain
rule: "Domain services are part of the domain layer, not application layer."
constraint: Marked domain services reside in a module domain.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.
checks: "Each resides in a domain package of some module root (<module>.domain..). An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-010"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Marked domain services reside in a module domain

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.

## Check

Each resides in a domain package of some module root (<module>.domain..). An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainService.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-010",
        "Marked domain services reside in a module domain",
        "Domain services are part of the domain layer, not application layer",
        arch ->
            classes()
                .that()
                .areAssignableTo(arch.layout().markers().domainService())
                .and()
                .areNotInterfaces()
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " DomainService.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-010",
    "Marked domain services reside in a module domain",
    "Domain services are part of the domain layer, not application layer",
    arch => Types()
        .That()
        .FollowCustomPredicate(t => t.IsAssignableTo(arch.Layout.Markers.DomainService), "are domain services")
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns())))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainService.")
    .Checking(
        "Each resides in a domain namespace of some module root (<module>.Domain or below). An "
        + "empty selection passes.")
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
