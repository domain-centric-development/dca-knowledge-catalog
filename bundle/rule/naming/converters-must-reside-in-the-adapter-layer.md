---
type: Rule
id: DCA-NAM-008
title: Converters must reside in the adapter layer
rule: Converters/Mappers translate between layers and should be in adapters.
constraint: Converters must reside in the adapter layer.
enforced_by: "NamingRules#DCA-NAM-008"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-008",
    "Converters must reside in the adapter layer",
    "Converters/Mappers translate between layers and should be in adapters",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Converter")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAPackage(layout.adapterPattern())
            .allowEmptyShould(true))
```
