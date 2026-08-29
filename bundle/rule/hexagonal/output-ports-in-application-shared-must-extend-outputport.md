---
type: Rule
id: DCA-HEX-009
title: Output Ports in application.shared must extend OutputPort
rule: "Top-level interfaces in application.shared are output ports and must extend OutputPort to be part of the port hierarchy. Nested interfaces (e.g. IdentityProvider.Identity) are part of their enclosing port's contract, not ports themselves."
constraint: Output Ports in application.shared must extend OutputPort.
enforced_by: "HexagonalRules#DCA-HEX-009"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-009",
    "Output Ports in application.shared must extend OutputPort",
    "Top-level interfaces in application.shared are output ports and must extend OutputPort to"
        + " be part of the port hierarchy. Nested interfaces (e.g. IdentityProvider.Identity)"
        + " are part of their enclosing port's contract, not ports themselves",
    arch ->
        classes()
            .that()
            .resideInAPackage(layout.sharedOutputPortPattern())
            .and()
            .areInterfaces()
            .and()
            .areTopLevelClasses()
            .and()
            .haveSimpleNameNotEndingWith("package-info")
            .should()
            .beAssignableTo(OutputPort.class)
            .allowEmptyShould(true))
```

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
