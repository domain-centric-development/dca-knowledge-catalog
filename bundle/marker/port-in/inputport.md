---
type: Marker
title: InputPort
category: port-in
kind: interface
signature: public interface InputPort
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/in/InputPort.java
tags: [port-in, marker]
---

Marker interface for Input Ports (Hexagonal Architecture).

## Governed by

- [Application layer InputPort implementations must end with 'UseCase'](/rule/naming/application-layer-inputport-implementations-must-end-with-usecase.md)
- [InputPort interfaces must end with 'InputPort'](/rule/naming/inputport-interfaces-must-end-with-inputport.md)
- [Base InputPort interface must be in sharedkernel marker port in package](/rule/usecase/base-inputport-interface-must-be-in-sharedkernel-marker-port-in-package.md)

## Referenced by ADRs

- [ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation](/adr/adr-007-hexagonal-architecture.md)
- [ADR-011: Bounded Context Isolation via Package Structure](/adr/adr-011-bounded-context-isolation.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)

## Discussed in

- [Application Layer](/book/04-the-four-layers/application-layer.md)
- [Ports & Adapters](/book/06-application-layer/ports-adapters.md)
- [Base Port Interfaces](/book/11-shared-kernel/base-port-interfaces.md)
- [Ports & Adapters](/book/appendix-a-glossary/ports-adapters.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [ELEMENTS](/guide/readme/elements.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
