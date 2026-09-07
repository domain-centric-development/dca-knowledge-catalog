---
type: Rule
id: DCA-NAM-011
title: ViewModels must reside in adapter.incoming.web packages
rule: ViewModels are presentation concerns and must reside in incoming web adapter packages.
constraint: ViewModels must reside in adapter.incoming.web packages.
enforced_by: "NamingRules#DCA-NAM-011"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-011",
    "ViewModels must reside in adapter.incoming.web packages",
    "ViewModels are presentation concerns and must reside in incoming web adapter packages",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("ViewModel")
            .and()
            .resideInAnyPackage(layout.basePackage() + "..")
            .should()
            .resideInAnyPackage(incomingWebAdapterPatterns(arch))
            .allowEmptyShould(true))
```
