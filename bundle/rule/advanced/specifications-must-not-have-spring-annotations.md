---
type: Rule
id: DCA-ADV-018
title: Specifications must not have Spring annotations
rule: Specifications should be framework-independent value objects.
constraint: Specifications must not have Spring annotations.
enforced_by: "AdvancedPatternRules#DCA-ADV-018"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

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
```

## Applies to markers

- [Specification<T>](/marker/tactical/specification.md)
