---
type: Rule
id: DCA-NAM-001
title: Application layer InputPort implementations must end with 'UseCase'
rule: "InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)."
constraint: Application layer InputPort implementations must end with 'UseCase'.
enforced_by: "NamingRules#DCA-NAM-001"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-001",
    "Application layer InputPort implementations must end with '"
        + layout.useCaseSuffix()
        + "'",
    "InputPort implementations (use cases) should follow consistent naming conventions"
        + " (Hexagonal Architecture)",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .areNotInterfaces()
            .and()
            .areNotRecords()
            .and()
            .implement(UseCase.class)
            .should()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .allowEmptyShould(true))
```

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
