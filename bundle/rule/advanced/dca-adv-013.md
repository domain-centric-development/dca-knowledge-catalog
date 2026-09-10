---
type: Rule
id: DCA-ADV-013
title: Factories should implement Factory Marker Interface
rule: Classes implementing Factory marker should have 'Factory' in their name.
constraint: Factories should implement Factory Marker Interface.
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

# Factories should implement Factory Marker Interface

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
        "Factories should implement Factory Marker Interface",
        "Classes implementing Factory marker should have 'Factory' in their name",
        arch ->
            classes()
                .that()
                .implement(Factory.class)
                .should()
                .haveSimpleNameEndingWith("Factory")
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to Factory.")
    .checking(
        "The simple name ends with Factory. Only the suffix is checked. An empty selection passes.")
```
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-013",
    "Factories should implement IFactory Marker Interface",
    "Classes implementing IFactory marker should have 'Factory' in their name",
    arch => Types()
        .That()
        .AreAssignableTo(typeof(IFactory))
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .HaveNameEndingWith("Factory"))
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
