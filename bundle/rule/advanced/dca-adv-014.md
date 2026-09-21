---
type: Rule
id: DCA-ADV-014
title: Factories must reside in domain package
rule: "Factories are part of the domain layer (complex aggregate creation logic)."
constraint: Factories must reside in domain package.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to Factory.
checks: "Each resides in a domain package of some module root (<module>.domain..). An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-014"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Factories must reside in domain package

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to Factory.

## Check

Each resides in a domain package of some module root (<module>.domain..). An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IFactory.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-014",
        "Factories must reside in domain package",
        "Factories are part of the domain layer (complex aggregate creation logic)",
        arch ->
            classes()
                .that()
                .areAssignableTo(arch.layout().markers().factory())
                .and()
                .areNotInterfaces()
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to Factory.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-014",
    "Factories must reside in domain namespace",
    "Factories are part of the domain layer (complex aggregate creation logic)",
    arch => Types()
        .That()
        .FollowCustomPredicate(t => t.IsAssignableTo(arch.Layout.Markers.Factory), "are factories")
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns())))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IFactory.")
    .Checking(
        "Each resides in a domain namespace of some module root (<module>.Domain or below). An "
        + "empty selection passes.")
```

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
