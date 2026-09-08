---
type: Rule
id: DCA-ADV-013
title: Factories should implement Factory Marker Interface
rule: Classes implementing Factory marker should have 'Factory' in their name.
constraint: Factories should implement Factory Marker Interface.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to Factory.
checks: The simple name ends with Factory. Only the suffix is checked. An empty selection passes.
enforced_by: "AdvancedPatternRules#DCA-ADV-013"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to Factory.

## Check

The simple name ends with Factory. Only the suffix is checked. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IFactory.

**Check.** The simple name ends with Factory. Only the suffix is checked. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-013",
        "Factories should implement Factory Marker Interface",
        "Classes implementing Factory marker should have 'Factory' in their name",
        arch ->
            classes()
                .that()
                .implement(Factory.class)
                .should()
                .haveSimpleNameEndingWith("Factory")
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to Factory.")
    .checking(
        "The simple name ends with Factory. Only the suffix is checked. An empty selection passes.")
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
