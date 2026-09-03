---
type: Rule
id: DCA-HEX-006
title: "Port adapters (incoming and outgoing) must not communicate directly with each other within the same context"
rule: "Port adapters should communicate through application services, not directly (event consumers are the exception)."
constraint: "Port adapters (incoming and outgoing) must not communicate directly with each other within the same context."
enforced_by: "HexagonalRules#DCA-HEX-006"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-006",
    "Port adapters (incoming and outgoing) must not communicate directly with each other"
        + " within the same context",
    "Port adapters should communicate through application services, not directly (event"
        + " consumers are the exception)",
    arch ->
        noClasses()
            .that()
            .resideInAnyPackage(arch.allIncomingAdapterPatterns())
            .and()
            .resideOutsideOfPackage(eventConsumerPattern())
            .should()
            .dependOnClassesThat()
            .resideInAnyPackage(arch.allOutgoingAdapterPatterns()))
```
