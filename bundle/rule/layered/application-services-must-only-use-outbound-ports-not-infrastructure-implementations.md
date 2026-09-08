---
type: Rule
id: DCA-LAY-003
title: "Application Services must only use outbound ports (not infrastructure implementations)"
rule: "Application services should only use outbound ports declared as interfaces (port.out), not infrastructure implementation details."
constraint: "Application Services must only use outbound ports (not infrastructure implementations)."
selects: "Classes in <module>.application.. of every module root."
checks: "No dependency on a class residing in the global infrastructure package or in any isolated module's own infrastructure package, sub-packages included, with an exact segment boundary. Dependencies on outgoing adapters are not checked here - only infrastructure packages count."
enforced_by: "LayeredRules#DCA-LAY-003"
status: enforced
rule_set: layered
implementations: [java, dotnet]
resource: dca-java/dca-archunit/src/main/java/dev/domaincentric/dca/archunit/rules/LayeredRules.java
tags: [layered, archunit]
---

## Selection

Classes in <module>.application.. of every module root.

## Check

No dependency on a class residing in the global infrastructure package or in any isolated module's own infrastructure package, sub-packages included, with an exact segment boundary. Dependencies on outgoing adapters are not checked here - only infrastructure packages count.

## .NET reading

**Selection.** Types in <module>.Application of every module root.

**Check.** No dependency on a type residing in the global infrastructure namespace or in any isolated module's own infrastructure namespace, sub-namespaces included, with an exact segment boundary. Dependencies on outgoing adapters are not checked here - only infrastructure namespaces count.

## Implementation

```java
DcaRule.of(
        "DCA-LAY-003",
        "Application Services must only use outbound ports (not infrastructure implementations)",
        "Application services should only use outbound ports declared as interfaces (port.out), not"
            + " infrastructure implementation details",
        arch ->
            noClasses()
                .that()
                .resideInAnyPackage(arch.allApplicationPatterns())
                .should()
                .dependOnClassesThat(arch.infrastructureImplementation())
                .allowEmptyShould(true))
    .selecting("Classes in <module>.application.. of every module root.")
    .checking(
        "No dependency on a class residing in the global infrastructure package or in any"
            + " isolated module's own infrastructure package, sub-packages included, with an"
            + " exact segment boundary. Dependencies on outgoing adapters are not checked"
            + " here - only infrastructure packages count.")
```

## Architecture queries

[DcaArchitecture](/reference/architecture.md) methods the rule relies on: `allApplicationPatterns()`, `infrastructureImplementation()` - how they resolve packages is described there and in [DcaLayout](/reference/layout.md).

## Configured by

- [DcaArchitecture](/reference/architecture.md)
- [DcaLayout](/reference/layout.md)
