---
type: Rule
id: DCA-HEX-011
title: "Incoming Adapters must depend on input port interfaces, not on use case classes"
rule: "A driving adapter drives the application through its port. Injecting the concrete implementation instead couples the adapter to one realisation of the use case, defeats the Dependency Inversion Principle the port exists for, and makes the adapter untestable without the real use case and everything it depends on."
constraint: "Incoming Adapters must depend on input port interfaces, not on use case classes."
enforced_by: "HexagonalRules#DCA-HEX-011"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-011",
    "Incoming Adapters must depend on input port interfaces, not on use case classes",
    "A driving adapter drives the application through its port. Injecting the concrete"
        + " implementation instead couples the adapter to one realisation of the use case,"
        + " defeats the Dependency Inversion Principle the port exists for, and makes the"
        + " adapter untestable without the real use case and everything it depends on",
    arch ->
        noClasses()
            .that()
            .resideInAPackage(layout.incomingAdapterPattern())
            .should()
            .dependOnClassesThat(useCaseImplementations())
            .allowEmptyShould(true))
```
