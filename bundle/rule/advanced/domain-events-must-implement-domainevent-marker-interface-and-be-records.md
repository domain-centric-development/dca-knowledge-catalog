---
type: Rule
id: DCA-ADV-001
title: Domain Events must implement DomainEvent Marker Interface and be records
rule: "Domain events should be immutable records implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCleared)."
constraint: Domain Events must implement DomainEvent Marker Interface and be records.
enforced_by: "AdvancedPatternRules#DCA-ADV-001"
status: enforced
rule_set: advanced
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

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
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
