---
type: Rule
id: DCA-HEX-008
title: "Classes named *Repository must reside in the outgoing adapter package"
rule: "Repository implementations are secondary adapters (outgoing ports)."
constraint: "Classes named *Repository must reside in the outgoing adapter package."
enforced_by: "HexagonalRules#DCA-HEX-008"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-008",
    "Classes named *Repository must reside in the outgoing adapter package",
    "Repository implementations are secondary adapters (outgoing ports)",
    arch ->
        classes()
            .that()
            .haveSimpleNameEndingWith("Repository")
            .and()
            .areNotInterfaces()
            .should()
            .resideInAPackage(layout.outgoingAdapterPattern())
            .allowEmptyShould(true))
```

## Applies to markers

- [Repository<T, ID>](/marker/port-out/repository.md)
