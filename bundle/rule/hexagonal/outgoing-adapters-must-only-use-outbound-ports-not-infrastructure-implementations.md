---
type: Rule
id: DCA-HEX-005
title: "Outgoing Adapters must only use outbound ports (not infrastructure implementations)"
rule: "Outgoing adapters should only use outbound ports declared as interfaces (port.out), not infrastructure implementation details."
constraint: "Outgoing Adapters must only use outbound ports (not infrastructure implementations)."
enforced_by: "HexagonalRules#DCA-HEX-005"
status: enforced
rule_set: hexagonal
implementations: [java]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

```java
DcaRule.of(
    "DCA-HEX-005",
    "Outgoing Adapters must only use outbound ports (not infrastructure implementations)",
    "Outgoing adapters should only use outbound ports declared as interfaces (port.out), not"
        + " infrastructure implementation details",
    arch ->
        noClasses()
            .that()
            .resideInAPackage(layout.outgoingAdapterPattern())
            .should()
            .dependOnClassesThat(arch.infrastructureImplementation()))
```
