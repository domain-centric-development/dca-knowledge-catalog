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
            .resideInAnyPackage(layout.domainPattern())
            .should()
            .dependOnClassesThat()
            .resideInAPackage(layout.infrastructurePattern()))
```
