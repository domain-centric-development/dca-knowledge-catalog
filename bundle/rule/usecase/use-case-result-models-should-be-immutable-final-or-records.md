---
type: Rule
id: DCA-USE-007
title: "Use Case Result Models should be immutable (final or records)"
rule: "Use case result models should be immutable (value objects)."
constraint: "Use Case Result Models should be immutable (final or records)."
enforced_by: "UseCaseRules#DCA-USE-007"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-007",
    "Use Case Result Models should be immutable (final or records)",
    "Use case result models should be immutable (value objects)",
    arch -> immutableApplicationModels(layout, "Result"))
```
