---
type: Rule
id: DCA-TAC-022
title: Enriched Domain Models must be Value Object records
rule: Enriched domain models are immutable read projections and must be records implementing Value.
constraint: Enriched Domain Models must be Value Object records.
enforced_by: "TacticalPatternRules#DCA-TAC-022"
status: enforced
rule_set: tactical
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/TacticalPatternRules.java
tags: [tactical, archunit]
---

```java
DcaRule.of(
    "DCA-TAC-022",
    "Enriched Domain Models must be Value Object records",
    "Enriched domain models are immutable read projections and must be records implementing"
        + " Value",
    arch ->
        classes()
            .that()
            .haveSimpleNameStartingWith("Enriched")
            .and()
            .resideInAPackage(layout.domainModelPattern())
            .and()
            .doNotImplement(Factory.class)
            .should()
            .beRecords()
            .andShould()
            .beAssignableTo(Value.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [Factory](/marker/tactical/factory.md)
- [Value](/marker/tactical/value.md)
