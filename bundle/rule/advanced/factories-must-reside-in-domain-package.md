---
type: Rule
id: DCA-ADV-014
title: Factories must reside in domain package
rule: "Factories are part of the domain layer (complex aggregate creation logic)."
constraint: Factories must reside in domain package.
enforced_by: "AdvancedPatternRules#DCA-ADV-014"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-014",
    "Factories must reside in domain package",
    "Factories are part of the domain layer (complex aggregate creation logic)",
    arch ->
        classes()
            .that()
            .implement(Factory.class)
            .should()
            .resideInAnyPackage(layout.domainPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
