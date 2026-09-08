---
type: Rule
id: DCA-ADV-011
title: Domain Services must not have Spring annotations
rule: Domain services should be framework-independent.
constraint: Domain Services must not have Spring annotations.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.
checks: "None carries the configured service or component annotation directly on the class. Only these two annotations are checked - others, and meta-annotations, are not. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-011"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainService.

## Check

None carries the configured service or component annotation directly on the class. Only these two annotations are checked - others, and meta-annotations, are not. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainService.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-011",
        "Domain Services must not have Spring annotations",
        "Domain services should be framework-independent",
        arch ->
            noClasses()
                .that()
                .implement(DomainService.class)
                .should()
                .beAnnotatedWith(layout.frameworkAnnotations().service())
                .orShould()
                .beAnnotatedWith(layout.frameworkAnnotations().component())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to"
            + " DomainService.")
    .checking(
        "None carries the configured service or component annotation directly on the class. Only these"
            + " two annotations are checked - others, and meta-annotations, are not. An empty selection"
            + " passes.")
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
