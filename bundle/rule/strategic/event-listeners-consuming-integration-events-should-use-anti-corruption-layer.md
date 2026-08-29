---
type: Rule
id: DCA-STR-010
title: Event Listeners consuming integration events should use Anti-Corruption Layer
rule: "Consumed integration events are translated into the consuming context's own language before they reach its domain — verified by code review, not statically."
constraint: Event Listeners consuming integration events should use Anti-Corruption Layer.
enforced_by: "StrategicPatternRules#DCA-STR-010"
status: informational
rule_set: strategic
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/StrategicPatternRules.java
tags: [strategic, archunit]
---

```java
DcaRule.check(
    "DCA-STR-010",
    "Event Listeners consuming integration events should use Anti-Corruption Layer",
    "Consumed integration events are translated into the consuming context's own language"
        + " before they reach its domain — verified by code review, not statically",
    arch -> {})
```
