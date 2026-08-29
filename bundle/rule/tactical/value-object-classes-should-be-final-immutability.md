---
type: Rule
id: DCA-TAC-009
title: "Value Object classes should be final (immutability)"
rule: "Value objects should be immutable (final classes) - Vernon's DDD recommendation."
constraint: "Value Object classes should be final (immutability)."
enforced_by: "TacticalPatternRules#DCA-TAC-009"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-009",
    "Value Object classes should be final (immutability)",
    "Value objects should be immutable (final classes) - Vernon's DDD recommendation",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(layout.domainModelPattern(), layout.sharedKernelDomainPattern())
            .and()
            .implement(Value.class)
            .and()
            .areNotInterfaces()
            .and()
            .areNotRecords()
            .should()
            .haveModifier(JavaModifier.FINAL)
            .allowEmptyShould(true))
```

## Applies to markers

- [Value](/marker/tactical/value.md)
