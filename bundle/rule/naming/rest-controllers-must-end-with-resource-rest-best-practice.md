---
type: Rule
id: DCA-NAM-006
title: "REST Controllers must end with 'Resource' (REST best practice)"
rule: "@RestController annotated classes should end with 'Resource' following RESTful naming conventions."
constraint: "REST Controllers must end with 'Resource' (REST best practice)."
enforced_by: "NamingRules#DCA-NAM-006"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-006",
    "REST Controllers must end with '"
        + layout.restControllerSuffix()
        + "' (REST best practice)",
    "@RestController annotated classes should end with '"
        + layout.restControllerSuffix()
        + "' following RESTful naming conventions",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.incomingAdapterPattern())
            .and()
            .areAnnotatedWith(layout.frameworkAnnotations().restController())
            .should()
            .haveSimpleNameEndingWith(layout.restControllerSuffix())
            .allowEmptyShould(true))
```
