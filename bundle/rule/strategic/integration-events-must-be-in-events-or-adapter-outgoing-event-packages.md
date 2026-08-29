---
type: Rule
id: DCA-STR-007
title: Integration Events must be in events or adapter outgoing event packages
rule: "Integration Events must be in events/ packages (published named interface) or adapter.outgoing.event/ packages."
constraint: Integration Events must be in events or adapter outgoing event packages.
enforced_by: "StrategicPatternRules#DCA-STR-007"
status: enforced
rule_set: strategic
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.of(
    "DCA-STR-007",
    "Integration Events must be in events or adapter outgoing event packages",
    "Integration Events must be in events/ packages (published named interface) or"
        + " adapter.outgoing.event/ packages",
    arch ->
        classes()
            .that()
            .implement(IntegrationEvent.class)
            .should()
            .resideInAnyPackage("..events..", outgoingEventAdapterPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
