---
type: Rule
id: DCA-NAM-005
title: Controller classes must end with 'Controller'
rule: "@Controller annotated classes should follow naming conventions."
constraint: Controller classes must end with 'Controller'.
selects: "Classes in <module>.adapter.incoming.. of every module root that are directly annotated with the configured @Controller annotation."
checks: "The simple name ends with the literal Controller - this suffix is not configurable. A class carrying only the REST-controller annotation is not selected here, and a controller outside an incoming-adapter package is not checked. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-005"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Classes in <module>.adapter.incoming.. of every module root that are directly annotated with the configured @Controller annotation.

## Check

The simple name ends with the literal Controller - this suffix is not configurable. A class carrying only the REST-controller annotation is not selected here, and a controller outside an incoming-adapter package is not checked. An empty selection passes.

## .NET reading

**Selection.** Classes in <module>.Adapter.Incoming of every module root that derive from the configured controller base class without carrying the configured API-controller attribute, or that derive from the configured page-model base class.

**Check.** The name ends with the literal Controller - this suffix is not configurable. A class carrying the API-controller attribute is not selected here, and a controller outside an incoming-adapter namespace is not checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-005",
        "Controller classes must end with 'Controller'",
        "@Controller annotated classes should follow naming conventions",
        arch ->
            classes()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .and()
                .areAnnotatedWith(layout.frameworkAnnotations().controller())
                .should()
                .haveSimpleNameEndingWith("Controller")
                .allowEmptyShould(true))
    .selecting(
        "Classes in <module>.adapter.incoming.. of every module root that are directly"
            + " annotated with the configured @Controller annotation.")
    .checking(
        "The simple name ends with the literal Controller - this suffix is not configurable. A"
            + " class carrying only the REST-controller annotation is not selected here, and a"
            + " controller outside an incoming-adapter package is not checked. An empty"
            + " selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
