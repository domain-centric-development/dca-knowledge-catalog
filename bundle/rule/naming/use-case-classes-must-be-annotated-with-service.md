---
type: Rule
id: DCA-NAM-002
title: "Use case classes must be annotated with @Service"
rule: Use case classes must be Spring-managed beans.
constraint: "Use case classes must be annotated with @Service."
enforced_by: "NamingRules#DCA-NAM-002"
status: enforced
rule_set: naming
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
not_applicable_dotnet: ".NET has no @Service stereotype — use cases are registered in the DI container by code, there is no attribute to check"
---

```java
DcaRule.of(
    "DCA-NAM-002",
    "Use case classes must be annotated with @Service",
    "Use case classes must be Spring-managed beans",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.applicationPattern())
            .and()
            .haveSimpleNameEndingWith(layout.useCaseSuffix())
            .and()
            .areNotInterfaces()
            .should()
            .beAnnotatedWith(layout.frameworkAnnotations().service())
            .allowEmptyShould(true))
```
