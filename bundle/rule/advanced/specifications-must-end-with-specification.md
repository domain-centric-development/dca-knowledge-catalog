---
type: Rule
id: DCA-ADV-017
title: Specifications must end with 'Specification'
rule: Specification implementations are part of the domain layer.
constraint: Specifications must end with 'Specification'.
selects: "Non-interface classes anywhere on the classpath under scan whose simple name ends with Specification, excluding a class named exactly Specification. No marker is involved - only the name selects."
checks: "Each resides in a domain package of some module root (<module>.domain..). An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-017"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan whose simple name ends with Specification, excluding a class named exactly Specification. No marker is involved - only the name selects.

## Check

Each resides in a domain package of some module root (<module>.domain..). An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan whose simple name ends with Specification, excluding a type named exactly Specification. No marker is involved - only the name selects.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-017",
        "Specifications must end with 'Specification'",
        "Specification implementations are part of the domain layer",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Specification")
                .and()
                .areNotInterfaces()
                .and()
                .doNotHaveSimpleName("Specification")
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan whose simple name ends with"
            + " Specification, excluding a class named exactly Specification. No marker is involved - only"
            + " the name selects.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
