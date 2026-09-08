---
type: Rule
id: DCA-ADV-003
title: "Domain Events should be immutable (final or records)"
rule: "Domain events should be immutable (final classes or records)."
constraint: "Domain Events should be immutable (final or records)."
selects: "Non-interface, non-enum, non-record classes in <module>.domain.. of every module root that are assignable to DomainEvent."
checks: "The class is final. Records and enums are not selected, so a record event always passes here. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-003"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface, non-enum, non-record classes in <module>.domain.. of every module root that are assignable to DomainEvent.

## Check

The class is final. Records and enums are not selected, so a record event always passes here. An empty selection passes.

## .NET reading

**Selection.** Non-record classes in <module>.Domain of every module root that are assignable to IDomainEvent. Records, structs and interfaces are not selected.

**Check.** The class is sealed. A record event is not selected, so it always passes here. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-003",
        "Domain Events should be immutable (final or records)",
        "Domain events should be immutable (final classes or records)",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .and()
                .implement(DomainEvent.class)
                .and()
                .areNotInterfaces()
                .and()
                .areNotEnums()
                .and()
                .areNotRecords()
                .should()
                .haveModifier(JavaModifier.FINAL)
                .allowEmptyShould(true))
    .selecting(
        "Non-interface, non-enum, non-record classes in <module>.domain.. of every module root that are"
            + " assignable to DomainEvent.")
    .checking(
        "The class is final. Records and enums are not selected, so a record event always passes here."
            + " An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
