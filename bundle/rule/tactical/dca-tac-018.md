---
type: Rule
id: DCA-TAC-018
title: "Store interfaces must extend the Store marker, not Repository"
rule: Stores extend the Store marker; Repository is reserved for Aggregate Roots.
constraint: "Store interfaces must extend the Store marker, not Repository."
selects: "Interfaces anywhere under scan whose simple name ends with Store, the marker Store itself excluded."
checks: "The interface is assignable to the Store marker and not assignable to Repository; both must hold. An interface not named *Store is never reported; an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-018"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/TacticalPatternRules.cs
---

# Store interfaces must extend the Store marker, not Repository

## Selection

Interfaces anywhere under scan whose simple name ends with Store, the marker Store itself excluded.

## Check

The interface is assignable to the Store marker and not assignable to Repository; both must hold. An interface not named *Store is never reported; an empty selection passes.

## .NET reading

**Selection.** Interfaces below the root namespace whose name ends with Store; interfaces named exactly Store or IStore excluded.

**Check.** The interface is assignable to the IStore marker and not assignable to IRepository; both must hold, and each failing alone is reported. An interface not named *Store is never reported; an empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-018",
        "Store interfaces must extend the Store marker, not Repository",
        "Stores extend the Store marker; Repository is reserved for Aggregate Roots",
        arch ->
            classes()
                .that()
                .areInterfaces()
                .and()
                .haveSimpleNameEndingWith(arch.layout().storeSuffix())
                .and()
                .doNotHaveSimpleName(arch.layout().storeSuffix())
                .should()
                .beAssignableTo(arch.layout().markers().store())
                .andShould()
                .notBeAssignableTo(arch.layout().markers().repository())
                .allowEmptyShould(true))
    .selecting(
        "Interfaces anywhere under scan whose simple name ends with Store, the marker "
            + "Store itself excluded.")
    .checking(
        "The interface is assignable to the Store marker and not assignable to "
            + "Repository; both must hold. An interface not named *Store is never reported; "
            + "an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `layout()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Check(
    "DCA-TAC-018",
    "Store interfaces must extend the IStore marker, not IRepository",
    "Stores extend the IStore marker; IRepository is reserved for Aggregate Roots",
    arch =>
    {
        var violations = new List<string>();
        foreach (var candidate in arch.Interfaces)
        {
            if (!HasSuffixButIsNotMarker(candidate, arch.Layout.StoreSuffix))
            {
                continue;
            }

            if (!IsAssignableTo(arch, candidate, arch.Layout.Markers.Store))
            {
                violations.Add($"{candidate.FullName} is named *Store but does not extend {nameof(IStore)}");
            }

            if (IsAssignableTo(arch, candidate, arch.Layout.Markers.Repository))
            {
                violations.Add($"{candidate.FullName} is named *Store but extends {nameof(IRepository)}");
            }
        }

        DcaRule.Fail("Store interfaces must extend IStore and must not extend IRepository.", violations);
    })
    .Selecting(
        "Interfaces below the root namespace whose name ends with Store; interfaces "
        + "named exactly Store or IStore excluded.")
    .Checking(
        "The interface is assignable to the IStore marker and not assignable to "
        + "IRepository; both must hold, and each failing alone is reported. An "
        + "interface not named *Store is never reported; an empty selection passes.")
```

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
