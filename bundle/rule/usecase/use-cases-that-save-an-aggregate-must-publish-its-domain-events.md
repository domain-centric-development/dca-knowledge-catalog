---
type: Rule
id: DCA-USE-009
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - even when the action raised no event."
constraint: Use cases that save an aggregate must publish its domain events.
enforced_by: "UseCaseRules#DCA-USE-009"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-009",
    "Use cases that save an aggregate must publish its domain events",
    "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the"
        + " instance they may later be published out of context. Publishing belongs after the"
        + " save, in the use case that owns the unit of work - even when the action raised no"
        + " event",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(arch.allApplicationPatterns())
            .and()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .and()
            .areNotInterfaces()
            .should(publishAfterSaving())
            .allowEmptyShould(true))
```
