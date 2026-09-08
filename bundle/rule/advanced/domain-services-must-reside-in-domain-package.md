---
type: Rule
id: DCA-ADV-010
title: Domain Services must reside in domain package
rule: "Domain services are part of the domain layer, not application layer."
constraint: Domain Services must reside in domain package.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.
checks: "Each resides in a domain package of some module root (<module>.domain..). An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-010"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.

## Check

Each resides in a domain package of some module root (<module>.domain..). An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainService.

**Check.** Each resides in a domain namespace of some module root (<module>.Domain or below). An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-010",
        "Domain Services must reside in domain package",
        "Domain services are part of the domain layer, not application layer",
        arch ->
            classes()
                .that()
                .implement(DomainService.class)
                .should()
                .resideInAnyPackage(arch.allDomainPatterns())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " DomainService.")
    .checking(
        "Each resides in a domain package of some module root (<module>.domain..). An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
