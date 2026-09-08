---
type: Rule
id: DCA-NAM-007
title: "DTOs must reside in the adapter layer, not in domain or application"
rule: "DTOs are adapter concerns (presentation or external API) - not in domain or application."
constraint: "DTOs must reside in the adapter layer, not in domain or application."
selects: Classes under the base package whose simple name ends with Dto.
checks: "Each resides in an adapter package of some module root (<module>.adapter..), incoming or outgoing. A Dto in a domain, application or infrastructure package is reported; what the class contains is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-007"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Classes under the base package whose simple name ends with Dto.

## Check

Each resides in an adapter package of some module root (<module>.adapter..), incoming or outgoing. A Dto in a domain, application or infrastructure package is reported; what the class contains is not checked. An empty selection passes.

## .NET reading

**Selection.** Types under the root namespace whose name ends with Dto.

**Check.** Each resides in an adapter namespace of some module root (<module>.Adapter or below), incoming or outgoing. A Dto in a domain, application or infrastructure namespace is reported; what the type contains is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-007",
        "DTOs must reside in the adapter layer, not in domain or application",
        "DTOs are adapter concerns (presentation or external API) - not in domain or application",
        arch ->
            classes()
                .that()
                .haveSimpleNameEndingWith("Dto")
                .and()
                .resideInAnyPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(arch.allAdapterPatterns())
                .allowEmptyShould(true))
    .selecting("Classes under the base package whose simple name ends with Dto.")
    .checking(
        "Each resides in an adapter package of some module root (<module>.adapter..), incoming"
            + " or outgoing. A Dto in a domain, application or infrastructure package is"
            + " reported; what the class contains is not checked. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
