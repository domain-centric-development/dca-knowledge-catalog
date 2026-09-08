---
type: Rule
id: DCA-ADV-004
title: Domain Events must not have Spring annotations
rule: Domain events must be framework-independent POJOs.
constraint: Domain Events must not have Spring annotations.
selects: "Non-interface classes in <module>.domain.. of every module root that are assignable to DomainEvent."
checks: "None carries the configured component, service or event-listener annotation directly on the class. Only these three annotations are checked - others, and meta-annotations, are not. An empty selection passes."
enforced_by: "AdvancedPatternRules#DCA-ADV-004"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes in <module>.domain.. of every module root that are assignable to DomainEvent.

## Check

None carries the configured component, service or event-listener annotation directly on the class. Only these three annotations are checked - others, and meta-annotations, are not. An empty selection passes.

## .NET reading

**Selection.** Non-interface types in <module>.Domain of every module root that are assignable to IDomainEvent.

**Check.** Every attribute on the type itself - not on members, not inherited - has a type whose namespace lies below an allowed prefix: the configured third-party namespaces the domain may use (by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks), the building blocks, or a domain namespace of some module root. Any other attribute is a framework attribute and is reported; a type without a loadable runtime type is skipped. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-004",
        "Domain Events must not have Spring annotations",
        "Domain events must be framework-independent POJOs",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainPatterns())
                .and()
                .implement(DomainEvent.class)
                .should()
                .beAnnotatedWith(layout.frameworkAnnotations().component())
                .orShould()
                .beAnnotatedWith(layout.frameworkAnnotations().service())
                .orShould()
                .beAnnotatedWith(layout.frameworkAnnotations().eventListener())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.domain.. of every module root that are assignable to"
            + " DomainEvent.")
    .checking(
        "None carries the configured component, service or event-listener annotation directly on the"
            + " class. Only these three annotations are checked - others, and meta-annotations, are not."
            + " An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
