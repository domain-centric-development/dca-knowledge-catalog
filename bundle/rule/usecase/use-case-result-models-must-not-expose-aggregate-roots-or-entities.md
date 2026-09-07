---
type: Rule
id: DCA-USE-015
title: Use Case Result Models must not expose aggregate roots or entities
rule: "A result is the use case's answer, not a handle on the model: identity and behaviour stay behind the port; values, enriched models and read models may cross. Checked transitively through nested records, part records anywhere in the application layer (application.shared included), generic type arguments (List<T>, Optional<T>, Map<K,V>) and inherited fields, a generic base class's type parameters resolved as the result binds them."
constraint: Use Case Result Models must not expose aggregate roots or entities.
enforced_by: "UseCaseRules#DCA-USE-015"
status: enforced
rule_set: usecase
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/UseCaseRules.java
tags: [usecase, archunit]
---

```java
DcaRule.check(
    "DCA-USE-015",
    "Use Case Result Models must not expose aggregate roots or entities",
    "A result is the use case's answer, not a handle on the model: identity and behaviour stay"
        + " behind the port; values, enriched models and read models may cross. Checked"
        + " transitively through nested records, part records anywhere in the application layer"
        + " (application.shared included), generic type arguments (List<T>, Optional<T>,"
        + " Map<K,V>) and inherited fields, a generic base class's type parameters resolved as"
        + " the result binds them",
    arch -> checkResultsCarryNoIdentities(arch))
```
