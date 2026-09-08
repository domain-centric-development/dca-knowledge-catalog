---
type: Rule
id: DCA-HEX-004
title: "Incoming Adapters must only use outbound ports (not infrastructure implementations)"
rule: "Incoming adapters should only use outbound ports declared as interfaces (port.out), not infrastructure implementation details."
constraint: "Incoming Adapters must only use outbound ports (not infrastructure implementations)."
selects: "Classes in <module>.adapter.incoming.. of every module root."
checks: "No dependency on a class in an infrastructure package: the global base.infrastructure or an isolated module's own <module>.infrastructure, the package itself or any sub-package with an exact segment boundary. The shared kernel's infrastructure package does not count as an infrastructure implementation. An empty selection passes."
enforced_by: "HexagonalRules#DCA-HEX-004"
status: enforced
rule_set: hexagonal
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/HexagonalRules.java
tags: [hexagonal, archunit]
---

## Selection

Classes in <module>.adapter.incoming.. of every module root.

## Check

No dependency on a class in an infrastructure package: the global base.infrastructure or an isolated module's own <module>.infrastructure, the package itself or any sub-package with an exact segment boundary. The shared kernel's infrastructure package does not count as an infrastructure implementation. An empty selection passes.

## .NET reading

**Selection.** Types in <module>.Adapter.Incoming of every module root.

**Check.** No dependency on a type in an infrastructure namespace: the global Root.Infrastructure or an isolated module's own <module>.Infrastructure, the namespace itself or any sub-namespace with an exact segment boundary. The shared kernel's infrastructure namespace does not count as an infrastructure implementation. An empty selection passes.

## Implementation

```java
DcaRule.of(
        "DCA-HEX-004",
        "Incoming Adapters must only use outbound ports (not infrastructure implementations)",
        "Incoming adapters should only use outbound ports declared as interfaces (port.out), not"
            + " infrastructure implementation details",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allIncomingAdapterPatterns())
                .should()
                .dependOnClassesThat(arch.infrastructureImplementation())
                .allowEmptyShould(true))
    .selecting("Classes in <module>.adapter.incoming.. of every module root.")
    .checking(
        "No dependency on a class in an infrastructure package: the global"
            + " base.infrastructure or an isolated module's own <module>.infrastructure, the"
            + " package itself or any sub-package with an exact segment boundary. The shared"
            + " kernel's infrastructure package does not count as an infrastructure"
            + " implementation. An empty selection passes.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allIncomingAdapterPatterns()`, `infrastructureImplementation()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
