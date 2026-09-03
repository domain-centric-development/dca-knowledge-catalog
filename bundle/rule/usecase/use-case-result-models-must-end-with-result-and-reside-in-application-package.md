---
type: Rule
id: DCA-USE-006
title: Use Case Result Models must end with 'Result' and reside in application package
rule: Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in domain layer.
constraint: Use Case Result Models must end with 'Result' and reside in application package.
enforced_by: "UseCaseRules#DCA-USE-006"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-006",
    "Use Case Result Models must end with 'Result' and reside in application package",
    "Use case result models should be in application layer. Domain Value Objects with 'Result'"
        + " in name are allowed in domain layer.",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Result")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .and()
            .doNotImplement(Value.class)
            .should()
            .resideInAnyPackage(arch.allApplicationPatterns())
            .allowEmptyShould(true))
```

## Applies to markers

- [Value](/marker/tactical/value.md)
