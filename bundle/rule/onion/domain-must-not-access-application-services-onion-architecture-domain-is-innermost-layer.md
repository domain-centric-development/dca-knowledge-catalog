---
type: Rule
id: DCA-ONI-001
title: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)"
rule: Domain is the innermost layer in onion architecture and should not depend on application services.
constraint: "Domain must not access Application Services (Onion Architecture - Domain is innermost layer)."
enforced_by: "OnionRules#DCA-ONI-001"
status: enforced
rule_set: onion
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/OnionRules.java
tags: [onion, archunit]
---

```java
DcaRule.of(
    "DCA-ONI-001",
    "Domain must not access Application Services (Onion Architecture - Domain is innermost"
        + " layer)",
    "Domain is the innermost layer in onion architecture and should not depend on application"
        + " services",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(layout.domainPattern())
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage(layout.applicationPattern()))
```
