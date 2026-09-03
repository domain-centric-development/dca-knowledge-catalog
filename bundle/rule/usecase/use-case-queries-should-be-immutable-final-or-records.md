---
type: Rule
id: DCA-USE-005
title: "Use Case Queries should be immutable (final or records)"
rule: "Use case queries should be immutable (value objects)."
constraint: "Use Case Queries should be immutable (final or records)."
enforced_by: "UseCaseRules#DCA-USE-005"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.of(
    "DCA-USE-005",
    "Use Case Queries should be immutable (final or records)",
    "Use case queries should be immutable (value objects)",
    arch -> immutableApplicationModels(arch, "Query"))
```
