---
type: Rule
id: DCA-ADV-018
title: Specifications must not have Spring annotations
rule: Specifications should be framework-independent value objects.
constraint: Specifications must not have Spring annotations.
selects: "Classes in <module>.domain.. of every module root whose simple name ends with Specification - interfaces included."
checks: "None carries the configured component or service annotation directly on the class. Only these two annotations are checked - others, and meta-annotations, are not. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-018"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Classes in <module>.domain.. of every module root whose simple name ends with Specification - interfaces included.

## Check

None carries the configured component or service annotation directly on the class. Only these two annotations are checked - others, and meta-annotations, are not. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Domain of every module root whose simple name ends with Specification - interfaces included.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-018",
        "Specifications must not have Spring annotations",
        "Specifications should be framework-independent value objects",
        arch ->
            noClasses()
                .that()
                .haveSimpleNameEndingWith("Specification")
                .and()
                .resideInAnyPackage(arch.allDomainPatterns())
                .should()
                .beAnnotatedWith(layout.frameworkAnnotations().component())
                .orShould()
                .beAnnotatedWith(layout.frameworkAnnotations().service())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.domain.. of every module root whose simple name ends with Specification -"
            + " interfaces included.")
    .checking(
        "None carries the configured component or service annotation directly on the class. Only these"
            + " two annotations are checked - others, and meta-annotations, are not. An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [Specification<T>](/marker/tactical/specification.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
