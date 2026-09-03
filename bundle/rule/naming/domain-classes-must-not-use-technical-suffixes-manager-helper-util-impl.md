---
type: Rule
id: DCA-NAM-010
title: "Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)"
rule: "Domain names come from the ubiquitous language - name services by their specialty, not by technical role."
constraint: "Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)."
enforced_by: "NamingRules#DCA-NAM-010"
status: enforced
rule_set: naming
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/NamingRules.java
tags: [naming, archunit]
---

```java
DcaRule.of(
    "DCA-NAM-010",
    "Domain classes must not use technical suffixes (Manager, Helper, Util, Impl)",
    "Domain names come from the ubiquitous language - name services by their specialty, not by"
        + " technical role",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(arch.allDomainPatterns())
            .should()
            .haveSimpleNameEndingWith("Manager")
            .orShould()
            .haveSimpleNameEndingWith("Helper")
            .orShould()
            .haveSimpleNameEndingWith("Util")
            .orShould()
            .haveSimpleNameEndingWith("Utils")
            .orShould()
            .haveSimpleNameEndingWith("Impl")
            .allowEmptyShould(true))
```
