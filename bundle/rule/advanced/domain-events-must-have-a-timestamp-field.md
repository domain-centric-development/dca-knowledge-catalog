---
type: Rule
id: DCA-ADV-008
title: Domain Events must have a timestamp field
rule: "An event records something that happened — without a timestamp the fact cannot be ordered, replayed or audited."
constraint: Domain Events must have a timestamp field.
enforced_by: "AdvancedPatternRules#DCA-ADV-008"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.check(
    "DCA-ADV-008",
    "Domain Events must have a timestamp field",
    "An event records something that happened — without a timestamp the fact cannot be"
        + " ordered, replayed or audited",
    arch -> {
      List<String> violations =
          violations(
              arch,
              c -> c.isAssignableTo(DomainEvent.class) && !c.isInterface(),
              c -> !hasTimestampField(c),
              c -> c.getName() + " does not have a timestamp field");
      failIfAny(
          violations, "Domain Events must have a timestamp field (when did the event occur?):");
    })
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
