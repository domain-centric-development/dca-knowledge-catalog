---
type: Rule
id: DCA-NAM-003
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
enforced_by: "NamingRules#DCA-NAM-003"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-003",
    "InputPort interfaces must end with 'InputPort'",
    "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(arch.allApplicationPatterns())
            .and()
            .areInterfaces()
            .and()
            .areAssignableTo(InputPort.class)
            .and()
            .doNotHaveSimpleName("InputPort")
            .and()
            .doNotHaveSimpleName("UseCase")
            .should()
            .haveSimpleNameEndingWith("InputPort")
            .allowEmptyShould(true))
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
