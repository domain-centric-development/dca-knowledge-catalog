---
type: Rule
id: DCA-ADV-011
title: Domain Services must not have Spring annotations
rule: Domain services should be framework-independent.
constraint: Domain Services must not have Spring annotations.
enforced_by: "AdvancedPatternRules#DCA-ADV-011"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

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
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
