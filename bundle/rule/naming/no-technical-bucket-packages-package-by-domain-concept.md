---
type: Rule
id: DCA-NAM-009
title: No technical bucket packages - package by domain concept
rule: "Packages are named after domain concepts from the ubiquitous language, not technical patterns."
constraint: No technical bucket packages - package by domain concept.
enforced_by: "NamingRules#DCA-NAM-009"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-009",
    "No technical bucket packages - package by domain concept",
    "Packages are named after domain concepts from the ubiquitous language, not technical"
        + " patterns",
    arch ->
        noClasses()
            .that()
            .resideInAPackage(layout.basePackage() + "..")
            .should()
            .resideInAnyPackage(
                "..entities..", "..valueobjects..", "..helpers..", "..util..", "..utils..")
            .allowEmptyShould(true))
```
