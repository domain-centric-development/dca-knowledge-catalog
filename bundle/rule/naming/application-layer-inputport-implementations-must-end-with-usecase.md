---
type: Rule
id: DCA-NAM-001
title: Application layer InputPort implementations must end with 'UseCase'
rule: "InputPort implementations (use cases) should follow consistent naming conventions (Hexagonal Architecture)."
constraint: Application layer InputPort implementations must end with 'UseCase'.
selects: "Non-interface, non-record classes in <module>.application.. of every module root that implement UseCase."
checks: The simple name ends with the configured use-case suffix. Interfaces and records are not selected; a class implementing only InputPort without UseCase is not selected either. An empty selection passes.
enforced_by: "NamingRules#DCA-NAM-001"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Non-interface, non-record classes in <module>.application.. of every module root that implement UseCase.

## Check

The simple name ends with the configured use-case suffix. Interfaces and records are not selected; a class implementing only InputPort without UseCase is not selected either. An empty selection passes.

## .NET reading

**Selection.** Non-record classes in <module>.Application of every module root that implement IUseCase<TInput, TOutput> - directly or through an I*InputPort interface that extends it.

**Check.** The name ends with the configured use-case suffix. Interfaces and records are not selected; a class implementing only IInputPort without IUseCase is not selected either. An empty selection passes.

## Implementation

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
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .areNotInterfaces()
                .and()
                .areNotRecords()
                .and()
                .implement(UseCase.class)
                .should()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface, non-record classes in <module>.application.. of every module root that"
            + " implement UseCase.")
    .checking(
        "The simple name ends with the configured use-case suffix. Interfaces and records are"
            + " not selected; a class implementing only InputPort without UseCase is not"
            + " selected either. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
