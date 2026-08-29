---
type: Rule
id: DCA-TAC-018
title: "Store interfaces must extend the Store marker, not Repository"
rule: Stores extend the Store marker; Repository is reserved for Aggregate Roots.
constraint: "Store interfaces must extend the Store marker, not Repository."
enforced_by: "TacticalPatternRules#DCA-TAC-018"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-018",
    "Store interfaces must extend the Store marker, not Repository",
    "Stores extend the Store marker; Repository is reserved for Aggregate Roots",
    arch ->
        classes()
            .that()
            .areInterfaces()
            .and()
            .haveSimpleNameEndingWith(STORE_SUFFIX)
            .and()
            .doNotHaveSimpleName(STORE_SUFFIX)
            .should()
            .beAssignableTo(Store.class)
            .andShould()
            .notBeAssignableTo(Repository.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
- [Store](/marker/port-out/store.md)
