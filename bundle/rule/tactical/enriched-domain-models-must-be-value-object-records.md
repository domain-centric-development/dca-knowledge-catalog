---
type: Rule
id: DCA-TAC-022
title: Enriched Domain Models must be Value Object records
rule: Enriched domain models are immutable read projections and must be records implementing Value.
constraint: Enriched Domain Models must be Value Object records.
selects: "Classes in <module>.domain.model.. of every module root whose simple name starts with Enriched and that do not implement Factory; interfaces included."
checks: "The class is a record and is assignable to Value; both must hold. An Enriched*Factory is excluded because it implements Factory; an interface named Enriched* is selected and reported since it is not a record. An empty selection passes."
enforced_by: "TacticalPatternRules#DCA-TAC-022"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

## Selection

Classes in <module>.domain.model.. of every module root whose simple name starts with Enriched and that do not implement Factory; interfaces included.

## Check

The class is a record and is assignable to Value; both must hold. An Enriched*Factory is excluded because it implements Factory; an interface named Enriched* is selected and reported since it is not a record. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Domain.Model of every module root whose name starts with Enriched and that do not implement IFactory; interfaces included, compiler-generated types excluded.

**Check.** The type is a record class or a struct and is assignable to IValue; both must hold, and each failing alone is reported - an interface named Enriched* is reported because it is no record. An Enriched*Factory is excluded because it implements IFactory. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-TAC-022",
        "Enriched Domain Models must be Value Object records",
        "Enriched domain models are immutable read projections and must be records implementing"
            + " Value",
        arch ->
            classes()
                .that()
                .haveSimpleNameStartingWith("Enriched")
                .and()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .and()
                .doNotImplement(Factory.class)
                .should()
                .beRecords()
                .andShould()
                .beAssignableTo(Value.class)
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.model.. of every module root whose simple name "
            + "starts with Enriched and that do not implement Factory; interfaces included.")
    .checking(
        "The class is a record and is assignable to Value; both must hold. An "
            + "Enriched*Factory is excluded because it implements Factory; an interface named "
            + "Enriched* is selected and reported since it is not a record. An empty "
            + "selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Factory](/marker/tactical/factory.md)
- [Value](/marker/tactical/value.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
