---
type: Rule
id: DCA-USE-008
title: HTTP Response Models must end with 'Response' and reside in adapter incoming package
rule: HTTP response models should be in adapter incoming layer.
constraint: HTTP Response Models must end with 'Response' and reside in adapter incoming package.
enforced_by: "UseCaseRules#DCA-USE-008"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-008",
    "HTTP Response Models must end with 'Response' and reside in adapter incoming package",
    "HTTP response models should be in adapter incoming layer",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Response")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAPackage(layout.incomingAdapterPattern())
            .allowEmptyShould(true))
```
