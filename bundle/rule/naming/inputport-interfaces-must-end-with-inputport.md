---
type: Rule
id: DCA-NAM-003
title: InputPort interfaces must end with 'InputPort'
rule: "Input port interfaces should follow consistent naming conventions (Hexagonal Architecture)."
constraint: InputPort interfaces must end with 'InputPort'.
selects: "Interfaces in <module>.application.. of every module root that are assignable to InputPort, except those named exactly InputPort or UseCase."
checks: "The simple name ends with InputPort. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-003"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Interfaces in <module>.application.. of every module root that are assignable to InputPort, except those named exactly InputPort or UseCase.

## Check

The simple name ends with InputPort. Classes and records are not selected, and an interface extending InputPort outside an application package is not checked. An empty selection passes.

## .NET reading

**Selection.** Interfaces in <module>.Application of every module root that are assignable to IInputPort, except those named exactly InputPort, IInputPort, UseCase or IUseCase.

**Check.** The name starts with I and ends with InputPort (IPlaceOrderInputPort). Classes and records are not selected, and an interface extending IInputPort outside an application namespace is not checked. An empty selection passes.

## Implementation

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
    .selecting(
        "Interfaces in <module>.application.. of every module root that are assignable to"
            + " InputPort, except those named exactly InputPort or UseCase.")
    .checking(
        "The simple name ends with InputPort. Classes and records are not selected, and an"
            + " interface extending InputPort outside an application package is not checked. An"
            + " empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
