---
type: Rule
id: DCA-USE-011
title: DTOs must not be used in the Application Layer
rule: "Application layer should use Command/Query/Response models, not presentation DTOs (Clean Architecture)."
constraint: DTOs must not be used in the Application Layer.
enforced_by: "UseCaseRules#DCA-USE-011"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-011",
    "DTOs must not be used in the Application Layer",
    "Application layer should use Command/Query/Response models, not presentation DTOs (Clean"
        + " Architecture)",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(layout.applicationPattern())
            .should()
            .dependOnClassesThat()
            .haveSimpleNameEndingWith("Dto")
            .allowEmptyShould(true))
```
