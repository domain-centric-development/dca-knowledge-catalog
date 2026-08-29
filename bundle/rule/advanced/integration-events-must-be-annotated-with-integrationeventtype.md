---
type: Rule
id: DCA-ADV-005
title: Integration Events must be annotated with IntegrationEventType
rule: "@IntegrationEventType(name, version) is the contract identity of every integration event — the serializer keys (name, version) to the class and stamps both onto the wire envelope."
constraint: Integration Events must be annotated with IntegrationEventType.
enforced_by: "AdvancedPatternRules#DCA-ADV-005"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-005",
    "Integration Events must be annotated with IntegrationEventType",
    "@IntegrationEventType(name, version) is the contract identity of every integration event"
        + " — the serializer keys (name, version) to the class and stamps both onto the wire"
        + " envelope",
    arch ->
        classes()
            .that()
            .areAssignableTo(IntegrationEvent.class)
            .and()
            .areNotInterfaces()
            .should()
            .beAnnotatedWith(IntegrationEventType.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
