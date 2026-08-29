---
type: Rule
id: DCA-ADV-016
title: "Factories should be stateless (only final fields for dependencies)"
rule: "Factories should be stateless (only final fields for dependencies)."
constraint: "Factories should be stateless (only final fields for dependencies)."
enforced_by: "AdvancedPatternRules#DCA-ADV-016"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-016",
    "Factories should be stateless (only final fields for dependencies)",
    "Factories should be stateless (only final fields for dependencies)",
    arch ->
        classes()
            .that()
            .implement(Factory.class)
            .and()
            .resideInAnyPackage(layout.domainPattern())
            .should()
            .haveOnlyFinalFields()
            .allowEmptyShould(true))
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
