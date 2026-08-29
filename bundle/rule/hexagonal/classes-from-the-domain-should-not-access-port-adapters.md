---
type: Rule
id: DCA-HEX-001
title: Classes from the domain should not access port adapters
rule: "Domain should not depend on adapters (ports and adapters pattern)."
constraint: Classes from the domain should not access port adapters.
enforced_by: "HexagonalRules#DCA-HEX-001"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-001",
    "Classes from the domain should not access port adapters",
    "Domain should not depend on adapters (ports and adapters pattern)",
    arch ->
        noClasses()
            .that()
            .resideInAPackage(layout.domainModelPattern())
            .should()
            .dependOnClassesThat()
            .resideInAPackage(layout.adapterPattern()))
```
