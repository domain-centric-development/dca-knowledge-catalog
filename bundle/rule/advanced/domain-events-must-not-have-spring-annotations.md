---
type: Rule
id: DCA-ADV-004
title: Domain Events must not have Spring annotations
rule: Domain events must be framework-independent POJOs.
constraint: Domain Events must not have Spring annotations.
enforced_by: "AdvancedPatternRules#DCA-ADV-004"
status: enforced
rule_set: advanced
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-004",
    "Domain Events must not have Spring annotations",
    "Domain events must be framework-independent POJOs",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(layout.domainPattern())
            .and()
            .implement(DomainEvent.class)
            .should()
            .beAnnotatedWith(layout.frameworkAnnotations().component())
            .orShould()
            .beAnnotatedWith(layout.frameworkAnnotations().service())
            .orShould()
            .beAnnotatedWith(layout.frameworkAnnotations().eventListener())
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
