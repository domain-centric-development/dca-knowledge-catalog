---
type: Rule
id: DCA-ADV-002
title: Domain Events must reside in domain package
rule: "Domain events are part of the domain layer (named in past tense)."
constraint: Domain Events must reside in domain package.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent.
checks: "Each resides in a domain package of some module root (<module>.domain..). An event in an application, adapter or infrastructure package is reported. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-002"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
resource_dotnet: dca-dotnet/src/DomainCentric.ArchRules/Rules/AdvancedPatternRules.cs
---

# Domain Events must reside in domain package

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent.

## Check

Each resides in a domain package of some module root (<module>.domain..). An event in an application, adapter or infrastructure package is reported. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An event in an application, adapter or infrastructure namespace is reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-002",
        "Domain Events must reside in domain package",
        "Domain events are part of the domain layer (named in past tense)",
        arch ->
            classes()
                .that()
                .implement(DomainEvent.class)
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An event in an"
            + " application, adapter or infrastructure package is reported. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).
### C# expression

```csharp
DcaRule.Of(
    "DCA-ADV-002",
    "Domain Events must reside in domain namespace",
    "Domain events are part of the domain layer (named in past tense)",
    arch => Types()
        .That()
        .AreAssignableTo(typeof(IDomainEvent))
        .And()
        .FollowCustomPredicate(t => t is not Interface, "are not interfaces")
        .Should()
        .ResideInNamespaceMatching(DcaLayout.AnyOf(arch.AllDomainPatterns())))
    .Selecting(
        "Non-interface types anywhere under scan that are assignable to IDomainEvent.")
    .Checking(
        "Each resides in a domain namespace of some module root (<module>.Domain or below). An "
        + "event in an application, adapter or infrastructure namespace is reported. An empty "
        + "selection passes.")
```

## Related mentions (heuristic)

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
