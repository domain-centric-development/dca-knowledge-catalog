---
type: Rule
id: DCA-ADV-013
title: "Types carrying the factory role are named *Factory"
rule: "A factory is found by its role, and read by its name: a type that creates aggregates and is not called one makes the creation site hard to find in review and in a search."
constraint: "Types carrying the factory role are named *Factory."
selects: Non-interface classes anywhere on the classpath under scan that are assignable to Factory.
checks: The simple name ends with Factory. Only the suffix is checked. An empty selection passes.
enforced_by: "AdvancedPatternRules#DCA-ADV-013"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Types carrying the factory role are named *Factory

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to Factory.

## Check

The simple name ends with Factory. Only the suffix is checked. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IFactory.

**Check.** The simple name ends with Factory. Only the suffix is checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-013",
        "Types carrying the factory role are named *Factory",
        "A factory is found by its role, and read by its name: a type that creates aggregates"
            + " and is not called one makes the creation site hard to find in review and in a"
            + " search",
        arch ->
            classes()
                .that()
                .areAssignableTo(arch.layout().markers().factory())
                .and()
                .areNotInterfaces()
                .should()
                .haveSimpleNameEndingWith(arch.layout().factorySuffix())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to Factory.")
    .checking(
        "The simple name ends with Factory. Only the suffix is checked. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-013",
    "Types carrying the factory role are named *Factory",
    "A factory is found by its role, and read by its name: a type that creates aggregates and is"
        + " not called one makes the creation site hard to find in review and in a search",
    arch => Types()
        .That()
        .FollowCustomPredicate(t => t.IsAssignableTo(arch.Layout.Markers.Factory), "are factories")
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .HaveNameEndingWith(arch.Layout.FactorySuffix))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IFactory.")
    .Checking(
        "The simple name ends with Factory. Only the suffix is checked. An empty selection "
        + "passes.")
```

## Related mentions (heuristic)

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
