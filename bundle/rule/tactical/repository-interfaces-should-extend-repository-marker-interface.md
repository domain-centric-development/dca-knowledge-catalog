---
type: Rule
id: DCA-TAC-013
title: Repository Interfaces should extend Repository Marker Interface
rule: Repository interfaces should extend Repository marker interface.
constraint: Repository Interfaces should extend Repository Marker Interface.
enforced_by: "TacticalPatternRules#DCA-TAC-013"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-013",
    "Repository Interfaces should extend Repository Marker Interface",
    "Repository interfaces should extend Repository marker interface",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .areInterfaces()
            .and()
            .haveSimpleNameEndingWith(REPOSITORY_SUFFIX)
            .and()
            .doNotHaveSimpleName(REPOSITORY_SUFFIX)
            .should()
            .beAssignableTo(Repository.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
