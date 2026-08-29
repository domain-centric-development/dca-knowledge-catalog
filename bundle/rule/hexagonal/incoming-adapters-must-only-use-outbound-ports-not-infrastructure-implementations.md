---
type: Rule
id: DCA-HEX-004
title: "Incoming Adapters must only use outbound ports (not infrastructure implementations)"
rule: "Incoming adapters should only use outbound ports declared as interfaces (port.out), not infrastructure implementation details."
constraint: "Incoming Adapters must only use outbound ports (not infrastructure implementations)."
enforced_by: "HexagonalRules#DCA-HEX-004"
status: enforced
rule_set: hexagonal
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-004",
    "Incoming Adapters must only use outbound ports (not infrastructure implementations)",
    "Incoming adapters should only use outbound ports declared as interfaces (port.out), not"
        + " infrastructure implementation details",
    arch ->
        noClasses()
            .that()
            .resideInAPackage(layout.incomingAdapterPattern())
            .should()
            .dependOnClassesThat(arch.infrastructureImplementation()))
```
