---
type: Rule
id: DCA-STR-008
title: Integration Events should be immutable records
rule: "Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)."
constraint: Integration Events should be immutable records.
selects: Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan.
checks: The class is a record. A final class with final fields does not count - only the record form is accepted. The components' own immutability is not checked.
enforced_by: "StrategicPatternRules#DCA-STR-008"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

## Selection

Non-interface classes assignable to IntegrationEvent - directly or through a sub-interface - anywhere on the classpath under scan.

## Check

The class is a record. A final class with final fields does not count - only the record form is accepted. The components' own immutability is not checked.

## .NET reading

**Selection.** Non-interface types below the root namespace whose implemented interfaces include IIntegrationEvent - directly or through a derived interface; classes, records and structs alike, compiler-generated types excluded.

**Check.** The type is a record class or a struct (a record struct is a struct in the model and counts). A sealed class with init-only properties does not - only the record form is accepted. The components' own immutability is not checked.

## Implementation

```java
DcaRule.of(
        "DCA-STR-008",
        "Integration Events should be immutable records",
        "Integration Events must be immutable to ensure event integrity across contexts (Event"
            + " Sourcing best practice)",
        arch ->
            classes()
                .that()
                .implement(IntegrationEvent.class)
                .should()
                .beRecords()
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes assignable to IntegrationEvent - directly or through a"
            + " sub-interface - anywhere on the classpath under scan.")
    .checking(
        "The class is a record. A final class with final fields does not count - only the"
            + " record form is accepted. The components' own immutability is not checked.")
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
