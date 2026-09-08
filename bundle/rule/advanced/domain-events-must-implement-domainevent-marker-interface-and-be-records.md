---
type: Rule
id: DCA-ADV-001
title: Domain Events must implement DomainEvent Marker Interface and be records
rule: "Domain events should be immutable records implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCleared)."
constraint: Domain Events must implement DomainEvent Marker Interface and be records.
selects: Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent - directly or through a supertype.
checks: The class is a record. A final class or an enum implementing DomainEvent is reported; interfaces are not selected. An empty selection passes.
enforced_by: "AdvancedPatternRules#DCA-ADV-001"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

## Selection

Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent - directly or through a supertype.

## Check

The class is a record. A final class or an enum implementing DomainEvent is reported; interfaces are not selected. An empty selection passes.

## .NET reading

**Selection.** Non-interface types anywhere under scan that are assignable to IDomainEvent - directly or through a supertype.

**Check.** The type is a record class or a struct (a record struct is a struct to the analysis, so any struct counts). A plain class implementing IDomainEvent is reported, sealed or not; interfaces are not selected. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-ADV-001",
        "Domain Events must implement DomainEvent Marker Interface and be records",
        "Domain events should be immutable records implementing DomainEvent (named in past tense,"
            + " e.g., ProductCreated, CartCleared)",
        arch ->
            classes()
                .that()
                .implement(DomainEvent.class)
                .and()
                .areNotInterfaces()
                .should()
                .beRecords()
                .allowEmptyShould(true))
    .selecting(
        "Non-interface classes anywhere on the classpath under scan that are assignable to DomainEvent"
            + " - directly or through a supertype.")
    .checking(
        "The class is a record. A final class or an enum implementing DomainEvent is reported; interfaces"
            + " are not selected. An empty selection passes.")
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
