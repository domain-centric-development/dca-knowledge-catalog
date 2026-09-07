---
type: Rule
id: DCA-LAY-002
title: Domain must not have dependencies on Infrastructure
rule: "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)."
constraint: Domain must not have dependencies on Infrastructure.
enforced_by: "LayeredRules#DCA-LAY-002"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

```java
DcaRule.of(
    "DCA-LAY-002",
    "Domain must not have dependencies on Infrastructure",
    "Domain should not depend on infrastructure concerns (Dependency Inversion Principle)",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(arch.allDomainPatterns())
            .should()
            .dependOnClassesThat()
            // The global infrastructure package and every module's own one.
            .resideInAnyPackage(arch.allInfrastructurePatterns())
            // A context may legitimately have no domain layer at all - a supporting or generic
            // subdomain in transaction-script style. An absent domain is not a violation.
            .allowEmptyShould(true))
```
