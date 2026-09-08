---
type: Rule
id: DCA-NAM-002
title: "Use case classes must be annotated with @Service"
rule: Use case classes must be Spring-managed beans.
constraint: "Use case classes must be annotated with @Service."
selects: "Non-interface classes in <module>.application.. of every module root whose simple name ends with the configured use-case suffix."
checks: "The class is annotated with the configured @Service annotation. Records are selected like any other class; the marker interfaces are not consulted - only the suffix selects. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-002"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
not_applicable_dotnet: ".NET has no @Service stereotype — use cases are registered in the DI container by code, there is no attribute to check"
---

## Selection

Non-interface classes in <module>.application.. of every module root whose simple name ends with the configured use-case suffix.

## Check

The class is annotated with the configured @Service annotation. Records are selected like any other class; the marker interfaces are not consulted - only the suffix selects. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-002",
        "Use case classes must be annotated with @Service",
        "Use case classes must be Spring-managed beans",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .and()
                .haveSimpleNameEndingWith(layout.useCaseSuffix())
                .and()
                .areNotInterfaces()
                .should()
                .beAnnotatedWith(layout.frameworkAnnotations().service())
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes in <module>.application.. of every module root whose simple name"
            + " ends with the configured use-case suffix.")
    .checking(
        "The class is annotated with the configured @Service annotation. Records are selected"
            + " like any other class; the marker interfaces are not consulted - only the suffix"
            + " selects. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
