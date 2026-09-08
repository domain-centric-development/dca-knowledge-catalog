---
type: Rule
id: DCA-USE-008
title: HTTP Response Models must end with 'Response' and reside in adapter incoming package
rule: HTTP response models should be in adapter incoming layer.
constraint: HTTP Response Models must end with 'Response' and reside in adapter incoming package.
selects: Classes under the base package whose simple name ends with Response.
checks: "Each resides in an incoming-adapter package of some module root (<module>.adapter.incoming..), the shared kernel's included."
enforced_by: "UseCaseRules#DCA-USE-008"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

## Selection

Classes under the base package whose simple name ends with Response.

## Check

Each resides in an incoming-adapter package of some module root (<module>.adapter.incoming..), the shared kernel's included.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Response.

**Check.** Each resides in an incoming-adapter namespace of some module root (<module>.Adapter.Incoming or below), the shared kernel's included.

## Implementation

```java
DcaRule.of(
        "DCA-USE-008",
        "HTTP Response Models must end with 'Response' and reside in adapter incoming package",
        "HTTP response models should be in adapter incoming layer",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Response")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Response.")
    .checking(
        "Each resides in an incoming-adapter package of some module root (<module>.adapter.incoming..), the shared kernel's included.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
