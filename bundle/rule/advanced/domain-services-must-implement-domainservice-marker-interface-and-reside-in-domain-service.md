---
type: Rule
id: DCA-ADV-009
title: Domain Services must implement DomainService Marker Interface and reside in domain.service
rule: "Domain services implement DomainService marker and reside in domain.service packages (named descriptively, e.g., PricingService, CartTotalCalculator)."
constraint: Domain Services must implement DomainService Marker Interface and reside in domain.service.
enforced_by: "AdvancedPatternRules#DCA-ADV-009"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-009",
    "Domain Services must implement DomainService Marker Interface and reside in domain.service",
    "Domain services implement DomainService marker and reside in domain.service packages"
        + " (named descriptively, e.g., PricingService, CartTotalCalculator)",
    arch ->
        classes()
            .that()
            .implement(DomainService.class)
            .and()
            .areNotInterfaces()
            .should()
            .resideInAPackage(".." + layout.domainSubpackage() + ".service..")
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
