---
type: Rule
id: DCA-USE-002
title: Use Case Commands must end with 'Command' and reside in application package
rule: "Use case commands should be in application layer (CQRS pattern)."
constraint: Use Case Commands must end with 'Command' and reside in application package.
enforced_by: "UseCaseRules#DCA-USE-002"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-002",
    "Use Case Commands must end with 'Command' and reside in application package",
    "Use case commands should be in application layer (CQRS pattern)",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Command")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAnyPackage(layout.applicationPattern())
            .allowEmptyShould(true))
```
