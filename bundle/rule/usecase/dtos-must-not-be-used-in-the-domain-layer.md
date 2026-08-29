---
type: Rule
id: DCA-USE-010
title: DTOs must not be used in the Domain Layer
rule: "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle."
constraint: DTOs must not be used in the Domain Layer.
enforced_by: "UseCaseRules#DCA-USE-010"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-010",
    "DTOs must not be used in the Domain Layer",
    "Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion"
        + " Principle",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(layout.domainPattern())
            .should()
            .dependOnClassesThat()
            .haveSimpleNameEndingWith("Dto")
            .allowEmptyShould(true))
```
