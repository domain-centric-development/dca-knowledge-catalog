---
type: Rule
id: DCA-USE-004
title: "Use Case Commands should be immutable (final or records)"
rule: "Use case commands should be immutable (value objects)."
constraint: "Use Case Commands should be immutable (final or records)."
enforced_by: "UseCaseRules#DCA-USE-004"
status: enforced
rule_set: usecase
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-004",
    "Use Case Commands should be immutable (final or records)",
    "Use case commands should be immutable (value objects)",
    arch -> immutableApplicationModels(layout, "Command"))
```
