---
type: Rule
id: DCA-USE-002
title: Use Case Commands must end with 'Command' and reside in application package
rule: "Use case commands should be in application layer (CQRS pattern)."
constraint: Use Case Commands must end with 'Command' and reside in application package.
selects: Classes under the base package whose simple name ends with Command.
checks: "Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported."
enforced_by: "UseCaseRules#DCA-USE-002"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

## Selection

Classes under the base package whose simple name ends with Command.

## Check

Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Command.

**Check.** Each resides in an application namespace of some module root (<module>.Application). A Command in a domain, adapter or infrastructure namespace is reported.

## Implementation

```java
DcaRule.of(
        "DCA-USE-002",
        "Use Case Commands must end with 'Command' and reside in application package",
        "Use case commands should be in application layer (CQRS pattern)",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Command")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Command.")
    .checking(
        "Each resides in an application package of some module root (<module>.application..). A Command in a domain, adapter or infrastructure package is reported.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
