---
type: Rule
id: DCA-ONI-003
title: Domain Models must not have Spring/JPA annotations
rule: "Domain models must be framework-independent (no Spring or JPA annotations)."
constraint: Domain Models must not have Spring/JPA annotations.
selects: "Classes in <module>.domain.model.. of every module root."
checks: "None carries the configured component or service stereotype annotation, jakarta.persistence.Entity or jakarta.persistence.Table directly on the class. Only these four annotations are checked; other framework annotations, and classes elsewhere in the domain layer (domain.service, domain.event), are not."
enforced_by: "OnionRules#DCA-ONI-003"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

## Selection

Classes in <module>.domain.model.. of every module root.

## Check

None carries the configured component or service stereotype annotation, jakarta.persistence.Entity or jakarta.persistence.Table directly on the class. Only these four annotations are checked; other framework annotations, and classes elsewhere in the domain layer (domain.service, domain.event), are not.

## .NET reading

**Selection.** Types in <module>.Domain.Model of every module root, the shared kernel's included when it owns a domain layer.

**Check.** Every attribute on the type or on one of its own, non-inherited members has a namespace below a prefix of the layout's third-party allow-list - by default System, Microsoft.Extensions.Logging.Abstractions and DomainCentric.BuildingBlocks. Any other attribute is reported, whatever framework it comes from; types elsewhere in the domain layer (Domain.Service, Domain.Event) are not selected.

## Implementation

```java
DcaRule.of(
        "DCA-ONI-003",
        "Domain Models must not have Spring/JPA annotations",
        "Domain models must be framework-independent (no Spring or JPA annotations)",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allDomainModelPatterns())
                .should()
                .beAnnotatedWith(layout.frameworkAnnotations().component())
                .orShould()
                .beAnnotatedWith(layout.frameworkAnnotations().service())
                .orShould()
                .beAnnotatedWith("jakarta.persistence.Entity")
                .orShould()
                .beAnnotatedWith("jakarta.persistence.Table")
                .allowEmptyShould(true))
    .selecting("Classes in <module>.domain.model.. of every module root.")
    .checking(
        "None carries the configured component or service stereotype annotation,"
            + " jakarta.persistence.Entity or jakarta.persistence.Table directly on the class."
            + " Only these four annotations are checked; other framework annotations, and"
            + " classes elsewhere in the domain layer (domain.service, domain.event), are"
            + " not.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allDomainModelPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
