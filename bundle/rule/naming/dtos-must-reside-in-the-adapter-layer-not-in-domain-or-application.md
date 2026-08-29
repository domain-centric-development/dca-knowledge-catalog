---
type: Rule
id: DCA-NAM-007
title: "DTOs must reside in the adapter layer, not in domain or application"
rule: "DTOs are adapter concerns (presentation or external API) - not in domain or application."
constraint: "DTOs must reside in the adapter layer, not in domain or application."
enforced_by: "NamingRules#DCA-NAM-007"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-007",
    "DTOs must reside in the adapter layer, not in domain or application",
    "DTOs are adapter concerns (presentation or external API) - not in domain or application",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Dto")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAPackage(layout.adapterPattern())
            .allowEmptyShould(true))
```
