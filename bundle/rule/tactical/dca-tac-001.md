---
type: Rule
id: DCA-TAC-001
title: "Aggregate Roots must implement AggregateRoot<T, ID>"
rule: "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)."
constraint: "Aggregate Roots must implement AggregateRoot<T, ID>."
selects: "Non-interface classes in <module>.domain.model.. of every module root whose simple name ends with AggregateRoot, the marker of the aggregate-root role itself excluded."
checks: "The class is assignable to the aggregate-root role - through the marker or an intermediate base class. Only the name suffix triggers selection - an aggregate root not named *AggregateRoot is never reported, and an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-001"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Aggregate Roots must implement AggregateRoot<T, ID>

## Selection

Non-interface classes in <module>.domain.model.. of every module root whose simple name ends with AggregateRoot, the marker of the aggregate-root role itself excluded.

## Check

The class is assignable to the aggregate-root role - through the marker or an intermediate base class. Only the name suffix triggers selection - an aggregate root not named *AggregateRoot is never reported, and an empty selection passes.

## .NET reading

**Selection.** Non-interface types - classes, structs and enums - in <module>.Domain.Model of every module root whose name ends with AggregateRoot; the type named exactly AggregateRoot is excluded.

**Check.** The type implements the IAggregateRoot marker. Only the name suffix triggers selection - an aggregate root not named *AggregateRoot is never reported, and an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-001",
        "Aggregate Roots must implement AggregateRoot<T, ID>",
        "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.aggregateRootSuffix())
                .and()
                .areNotInterfaces()
                .and()
                .doNotHaveSimpleName(layout.aggregateRootSuffix())
                .should()
                .beAssignableTo(arch.layout().markers().aggregateRoot())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.model.. of every module root whose "
            + "simple name ends with AggregateRoot, the marker of the aggregate-root role "
            + "itself excluded.")
    .checking(
        "The class is assignable to the aggregate-root role - through the marker or an "
            + "intermediate base class. Only the name suffix triggers "
            + "selection - an aggregate root not named *AggregateRoot is never reported, and "
            + "an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()`, `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-001",
    "Aggregate Roots must implement IAggregateRoot",
    "Classes named *AggregateRoot must implement the IAggregateRoot interface (DDD pattern)",
    arch =>
    {
        var violations = new List<string>();
        foreach (var type in NonInterfaceTypes(arch))
        {
            if (!type.Name.EndsWith(arch.Layout.AggregateRootSuffix, StringComparison.Ordinal)
                || type.Name == arch.Layout.AggregateRootSuffix
                || !ResidesInAny(type, arch.AllDomainModelPatterns()))
            {
                continue;
            }

            if (!IsAssignableTo(arch, type, arch.Layout.Markers.AggregateRoot))
            {
                violations.Add($"{type.FullName} is named *AggregateRoot but does not implement {nameof(IAggregateRoot)}");
            }
        }

        DcaRule.Fail("Classes named *AggregateRoot must implement the IAggregateRoot marker.", violations);
    })
    .Selecting(
        "Non-interface types - classes, structs and enums - in <module>.Domain.Model of "
        + "every module root whose name ends with AggregateRoot; the type named exactly "
        + "AggregateRoot is excluded.")
    .Checking(
        "The type implements the IAggregateRoot marker. Only the name suffix triggers "
        + "selection - an aggregate root not named *AggregateRoot is never reported, "
        + "and an empty selection passes.")
```

## Related mentions (heuristic)

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
