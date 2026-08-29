---
type: Rule
id: DCA-NAM-005
title: Controller classes must end with 'Controller'
rule: "@Controller annotated classes should follow naming conventions."
constraint: Controller classes must end with 'Controller'.
enforced_by: "NamingRules#DCA-NAM-005"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-005",
    "Controller classes must end with 'Controller'",
    "@Controller annotated classes should follow naming conventions",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.incomingAdapterPattern())
            .and()
            .areAnnotatedWith(layout.frameworkAnnotations().controller())
            .should()
            .haveSimpleNameEndingWith("Controller")
            .allowEmptyShould(true))
```
