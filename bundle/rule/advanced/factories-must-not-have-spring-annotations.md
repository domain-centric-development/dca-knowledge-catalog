---
type: Rule
id: DCA-ADV-015
title: Factories must not have Spring annotations
rule: Factories should be framework-independent.
constraint: Factories must not have Spring annotations.
enforced_by: "AdvancedPatternRules#DCA-ADV-015"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-015",
    "Factories must not have Spring annotations",
    "Factories should be framework-independent",
    arch ->
        noClasses()
            .that()
            .implement(Factory.class)
            .and()
            .resideInAnyPackage(layout.domainPattern())
            .should()
            .beAnnotatedWith(layout.frameworkAnnotations().component())
            .orShould()
            .beAnnotatedWith(layout.frameworkAnnotations().service())
            .allowEmptyShould(true))
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
