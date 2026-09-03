---
type: Rule
id: DCA-ADV-003
title: "Domain Events should be immutable (final or records)"
rule: "Domain events should be immutable (final classes or records)."
constraint: "Domain Events should be immutable (final or records)."
enforced_by: "AdvancedPatternRules#DCA-ADV-003"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-003",
    "Domain Events should be immutable (final or records)",
    "Domain events should be immutable (final classes or records)",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(arch.allDomainPatterns())
            .and()
            .implement(DomainEvent.class)
            .and()
            .areNotInterfaces()
            .and()
            .areNotEnums()
            .and()
            .areNotRecords()
            .should()
            .haveModifier(JavaModifier.FINAL)
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainEvent](/marker/tactical/domainevent.md)
