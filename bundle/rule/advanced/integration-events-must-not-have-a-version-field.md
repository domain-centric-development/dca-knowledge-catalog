---
type: Rule
id: DCA-ADV-006
title: Integration Events must not have a version field
rule: "The schema version is a class property (@IntegrationEventType), never per-instance payload data — a version data field duplicates the annotation and can drift from it."
constraint: Integration Events must not have a version field.
enforced_by: "AdvancedPatternRules#DCA-ADV-006"
status: enforced
rule_set: advanced
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.check(
    "DCA-ADV-006",
    "Integration Events must not have a version field",
    "The schema version is a class property (@IntegrationEventType), never per-instance payload"
        + " data — a version data field duplicates the annotation and can drift from it",
    arch -> {
      List<String> violations =
          violations(
              arch,
              c -> c.isAssignableTo(IntegrationEvent.class) && !c.isInterface(),
              AdvancedPatternRules::hasVersionField,
              c ->
                  c.getName()
                      + " carries a version data field — declare the version in"
                      + " @IntegrationEventType instead");
      failIfAny(
          violations,
          "Integration Events must not have a version field — @IntegrationEventType is the"
              + " single source of truth:");
    })
```

## Applies to markers

- [IntegrationEvent](/marker/tactical/integrationevent.md)
- [@IntegrationEventType](/marker/tactical/integrationeventtype.md)
