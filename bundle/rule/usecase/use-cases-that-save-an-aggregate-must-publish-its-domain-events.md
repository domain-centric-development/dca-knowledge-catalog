---
type: Rule
id: DCA-USE-009
title: Use cases that save an aggregate must publish its domain events
rule: "A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be published out of context. Publishing belongs after the save, in the use case that owns the unit of work - even when the action raised no event. Checked per entry path, following calls within the use case class: every entry point that reaches a save - a method callable from outside the class, or one nothing in the class calls - must also reach a publication; a wrapper that publishes does not cover a direct call of the public method it wraps, and a helper two methods share does not connect them. That the publication follows the save and concerns the same aggregate is not established statically."
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
        + " event. Checked per entry path, following calls within the use case class: every"
        + " entry point that reaches a save - a method callable from outside the class, or one"
        + " nothing in the class calls - must also reach a publication; a wrapper that publishes"
        + " does not cover a direct call of the public method it wraps, and a helper two methods"
        + " share does not connect them. That the"
        + " publication follows the save and concerns the same aggregate is not established"
        + " statically",
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
