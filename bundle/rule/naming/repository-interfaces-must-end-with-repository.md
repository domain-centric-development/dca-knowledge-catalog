---
type: Rule
id: DCA-NAM-004
title: Repository Interfaces must end with 'Repository'
rule: "Repository interfaces should follow consistent naming conventions (DDD pattern)."
constraint: Repository Interfaces must end with 'Repository'.
enforced_by: "NamingRules#DCA-NAM-004"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-004",
    "Repository Interfaces must end with 'Repository'",
    "Repository interfaces should follow consistent naming conventions (DDD pattern)",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .areInterfaces()
            .and()
            .haveSimpleNameContaining("Repository")
            .and()
            .doNotHaveSimpleName("Repository")
            .should()
            .haveSimpleNameEndingWith("Repository")
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
