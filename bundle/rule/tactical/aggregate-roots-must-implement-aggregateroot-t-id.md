---
type: Rule
id: DCA-TAC-001
title: "Aggregate Roots must implement AggregateRoot<T, ID>"
rule: "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)."
constraint: "Aggregate Roots must implement AggregateRoot<T, ID>."
selects: "Non-interface classes in <module>.domain.model.. of every module root whose simple name ends with AggregateRoot, the marker interface AggregateRoot itself excluded."
checks: "The class implements the AggregateRoot marker. Only the name suffix triggers selection - an aggregate root not named *AggregateRoot is never reported, and an empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-001"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Non-interface classes in <module>.domain.model.. of every module root whose simple name ends with AggregateRoot, the marker interface AggregateRoot itself excluded.

## Check

The class implements the AggregateRoot marker. Only the name suffix triggers selection - an aggregate root not named *AggregateRoot is never reported, and an empty selection passes.

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
                .haveSimpleNameEndingWith("AggregateRoot")
                .and()
                .areNotInterfaces()
                .and()
                .doNotHaveSimpleName("AggregateRoot")
                .should()
                .implement(AggregateRoot.class)
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.model.. of every module root whose "
            + "simple name ends with AggregateRoot, the marker interface AggregateRoot itself "
            + "excluded.")
    .checking(
        "The class implements the AggregateRoot marker. Only the name suffix triggers "
            + "selection - an aggregate root not named *AggregateRoot is never reported, and "
            + "an empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
