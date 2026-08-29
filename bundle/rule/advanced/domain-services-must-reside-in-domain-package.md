---
type: Rule
id: DCA-ADV-010
title: Domain Services must reside in domain package
rule: "Domain services are part of the domain layer, not application layer."
constraint: Domain Services must reside in domain package.
enforced_by: "AdvancedPatternRules#DCA-ADV-010"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-010",
    "Domain Services must reside in domain package",
    "Domain services are part of the domain layer, not application layer",
    arch ->
        classes()
            .that()
            .implement(DomainService.class)
            .should()
            .resideInAnyPackage(layout.domainPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
