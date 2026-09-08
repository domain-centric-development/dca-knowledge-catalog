---
type: Rule
id: DCA-NAM-009
title: No technical bucket packages - package by domain concept
rule: "Packages are named after domain concepts from the ubiquitous language, not technical patterns."
constraint: No technical bucket packages - package by domain concept.
selects: Every class under the base package.
checks: "No class resides in a package whose name contains a segment entities, valueobjects, helpers, util or utils, at any depth. Only these five segments are checked; other technical names such as model, service or impl are not reported. An empty selection passes."
enforced_by: "NamingRules#DCA-NAM-009"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

## Selection

Every class under the base package.

## Check

No class resides in a package whose name contains a segment entities, valueobjects, helpers, util or utils, at any depth. Only these five segments are checked; other technical names such as model, service or impl are not reported. An empty selection passes.

## .NET reading

**Selection.** Every type under the root namespace.

**Check.** No type resides in a namespace with a segment Entities, ValueObjects, Helpers, Util or Utils, in any casing and at any depth. Only these five segments are checked; other technical names such as Model, Service or Impl are not reported. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-NAM-009",
        "No technical bucket packages - package by domain concept",
        "Packages are named after domain concepts from the ubiquitous language, not technical"
            + " patterns",
        arch ->
            noClasses()
                .that()
                .resideInAPackage(layout.basePackage() + "..")
                .should()
                .resideInAnyPackage(
                    "..entities..", "..valueobjects..", "..helpers..", "..util..", "..utils..")
                .allowEmptyShould(true))
    .selecting("Every class under the base package.")
    .checking(
        "No class resides in a package whose name contains a segment entities, valueobjects,"
            + " helpers, util or utils, at any depth. Only these five segments are checked;"
            + " other technical names such as model, service or impl are not reported. An empty"
            + " selection passes.")
```

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
