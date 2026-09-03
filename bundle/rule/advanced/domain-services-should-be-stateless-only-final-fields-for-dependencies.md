---
type: Rule
id: DCA-ADV-012
title: "Domain Services should be stateless (only final fields for dependencies)"
rule: "Domain services should be stateless (only final fields for dependencies)."
constraint: "Domain Services should be stateless (only final fields for dependencies)."
enforced_by: "AdvancedPatternRules#DCA-ADV-012"
status: enforced
rule_set: advanced
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/AdvancedPatternRules.java
tags: [advanced, archunit]
---

```java
DcaRule.of(
    "DCA-ADV-012",
    "Domain Services should be stateless (only final fields for dependencies)",
    "Domain services should be stateless (only final fields for dependencies)",
    arch ->
        classes()
            .that()
            .implement(DomainService.class)
            .and()
            .resideInAnyPackage(arch.allDomainPatterns())
            .should()
            .haveOnlyFinalFields()
            .allowEmptyShould(true))
```

## Applies to markers

- [DomainService](/marker/tactical/domainservice.md)
