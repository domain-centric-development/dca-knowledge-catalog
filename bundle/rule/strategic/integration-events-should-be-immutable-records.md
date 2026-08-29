---
type: Rule
id: DCA-STR-008
title: Integration Events should be immutable records
rule: "Integration Events must be immutable to ensure event integrity across contexts (Event Sourcing best practice)."
constraint: Integration Events should be immutable records.
enforced_by: "StrategicPatternRules#DCA-STR-008"
status: enforced
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

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
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
