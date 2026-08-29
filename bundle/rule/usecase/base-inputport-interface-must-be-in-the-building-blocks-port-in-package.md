---
type: Rule
id: DCA-USE-001
title: Base InputPort interface must be in the building-blocks port in package
rule: "Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture)."
constraint: Base InputPort interface must be in the building-blocks port in package.
enforced_by: "UseCaseRules#DCA-USE-001"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-001",
    "Base InputPort interface must be in the building-blocks port in package",
    "Base InputPort interface defines the generic contract for all use cases (Hexagonal"
        + " Architecture)",
    arch ->
        classes()
            .that()
            .areInterfaces()
            .and()
            .haveSimpleName("InputPort")
            .should()
            .resideInAPackage(DcaLayout.BUILDING_BLOCKS_PORT_IN_PACKAGE)
            .allowEmptyShould(true))
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
