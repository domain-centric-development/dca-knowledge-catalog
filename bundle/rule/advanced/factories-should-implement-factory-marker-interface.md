---
type: Rule
id: DCA-ADV-013
title: Factories should implement Factory Marker Interface
rule: Classes implementing Factory marker should have 'Factory' in their name.
constraint: Factories should implement Factory Marker Interface.
enforced_by: "AdvancedPatternRules#DCA-ADV-013"
status: enforced
rule_set: advanced
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-013",
    "Factories should implement Factory Marker Interface",
    "Classes implementing Factory marker should have 'Factory' in their name",
    arch ->
        classes()
            .that()
            .implement(Factory.class)
            .should()
            .haveSimpleNameEndingWith("Factory")
            .allowEmptyShould(true))
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
