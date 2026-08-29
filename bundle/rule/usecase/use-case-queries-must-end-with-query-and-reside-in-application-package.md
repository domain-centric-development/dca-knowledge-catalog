---
type: Rule
id: DCA-USE-003
title: Use Case Queries must end with 'Query' and reside in application package
rule: "Use case queries should be in application layer (CQRS pattern)."
constraint: Use Case Queries must end with 'Query' and reside in application package.
enforced_by: "UseCaseRules#DCA-USE-003"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-003",
    "Use Case Queries must end with 'Query' and reside in application package",
    "Use case queries should be in application layer (CQRS pattern)",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Query")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAnyPackage(layout.applicationPattern())
            .allowEmptyShould(true))
```
