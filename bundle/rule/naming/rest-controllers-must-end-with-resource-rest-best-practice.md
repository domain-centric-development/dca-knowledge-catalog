---
type: Rule
id: DCA-NAM-006
title: "REST Controllers must end with 'Resource' (REST best practice)"
rule: "@RestController annotated classes should end with 'Resource' following RESTful naming conventions."
constraint: "REST Controllers must end with 'Resource' (REST best practice)."
selects: "Classes in <module>.adapter.incoming.. of every module root that are directly annotated with the configured @RestController annotation."
checks: "The simple name ends with the configured REST-controller suffix. Classes annotated with the plain @Controller annotation are not selected, and a REST controller outside an incoming-adapter package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-006"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with the configured @RestController annotation.

## Check

The simple name ends with the configured REST-controller suffix. Classes annotated with the plain @Controller annotation are not selected, and a REST controller outside an incoming-adapter package is not checked. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root that carry the configured API-controller attribute ([ApiController] by default).

**Check.** The name ends with the configured REST-controller suffix. Controllers without the attribute are not selected, and an API controller outside an incoming-adapter namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-006",
        "REST Controllers must end with '"
            + layout.restControllerSuffix()
            + "' (REST best practice)",
        "@RestController annotated classes should end with '"
            + layout.restControllerSuffix()
            + "' following RESTful naming conventions",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .and()
                .areAnnotatedWith(layout.frameworkAnnotations().restController())
                .should()
                .haveSimpleNameEndingWith(layout.restControllerSuffix())
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root that are directly"
            + " annotated with the configured @RestController annotation.")
    .checking(
        "The simple name ends with the configured REST-controller suffix. Classes annotated"
            + " with the plain @Controller annotation are not selected, and a REST controller"
            + " outside an incoming-adapter package is not checked. An empty selection"
            + " passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
