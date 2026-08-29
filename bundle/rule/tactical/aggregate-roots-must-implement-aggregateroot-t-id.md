---
type: Rule
id: DCA-TAC-001
title: "Aggregate Roots must implement AggregateRoot<T, ID>"
rule: "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)."
constraint: "Aggregate Roots must implement AggregateRoot<T, ID>."
enforced_by: "TacticalPatternRules#DCA-TAC-001"
status: enforced
rule_set: tactical
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-001",
    "Aggregate Roots must implement AggregateRoot<T, ID>",
    "Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern)",
    arch ->
        classes()
            .that()
            .resideInAnyPackage(layout.domainModelPattern(), layout.sharedKernelDomainPattern())
            .and()
            .haveSimpleNameEndingWith("AggregateRoot")
            .and()
            .areNotInterfaces()
            .and()
            .doNotHaveSimpleName("AggregateRoot")
            .should()
            .implement(AggregateRoot.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
