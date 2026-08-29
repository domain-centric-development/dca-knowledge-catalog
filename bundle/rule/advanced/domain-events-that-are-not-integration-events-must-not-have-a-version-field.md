---
type: Rule
id: DCA-ADV-007
title: Domain Events that are not Integration Events must not have a version field
rule: Versioning is a contract concern of integration events — a purely internal domain event has no wire contract to version.
constraint: Domain Events that are not Integration Events must not have a version field.
enforced_by: "AdvancedPatternRules#DCA-ADV-007"
status: enforced
rule_set: advanced
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.check(
    "DCA-ADV-007",
    "Domain Events that are not Integration Events must not have a version field",
    "Versioning is a contract concern of integration events — a purely internal domain event"
        + " has no wire contract to version",
    arch -> {
      List<String> violations =
          violations(
              arch,
              c ->
                  c.isAssignableTo(DomainEvent.class)
                      && !c.isAssignableTo(IntegrationEvent.class)
                      && !c.isInterface(),
              AdvancedPatternRules::hasVersionField,
              c ->
                  c.getName()
                      + " has a version field but is not an IntegrationEvent — only"
                      + " IntegrationEvents need versioning");
      failIfAny(
          violations,
          "Domain Events (non-IntegrationEvent) must not have a version field — versioning is"
              + " only for IntegrationEvents:");
    })
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
- [IntegrationEvent](/marker/tactical/integrationevent.md)
