---
type: Rule
id: DCA-ONI-003
title: Domain Models must not have Spring/JPA annotations
rule: "Domain models must be framework-independent (no Spring or JPA annotations)."
constraint: Domain Models must not have Spring/JPA annotations.
enforced_by: "OnionRules#DCA-ONI-003"
status: enforced
rule_set: onion
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

```java
DcaRule.of(
    "DCA-ONI-003",
    "Domain Models must not have Spring/JPA annotations",
    "Domain models must be framework-independent (no Spring or JPA annotations)",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(layout.domainModelPattern(), layout.sharedKernelDomainPattern())
            .should()
            .beAnnotatedWith(layout.frameworkAnnotations().component())
            .orShould()
            .beAnnotatedWith(layout.frameworkAnnotations().service())
            .orShould()
            .beAnnotatedWith("jakarta.persistence.Entity")
            .orShould()
            .beAnnotatedWith("jakarta.persistence.Table"))
```
