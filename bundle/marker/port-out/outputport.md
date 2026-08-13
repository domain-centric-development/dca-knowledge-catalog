---
type: Marker
title: OutputPort
category: port-out
kind: interface
signature: public interface OutputPort
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/OutputPort.java
tags: [port-out, marker]
---

Marker interface for Output Ports (Hexagonal Architecture).

## Governed by

- [Output Ports in application.shared must extend OutputPort](/rule/hexagonal/output-ports-in-application-shared-must-extend-outputport.md)
- [Output ports must not reside in the domain layer](/rule/hexagonal/output-ports-must-not-reside-in-the-domain-layer.md)
- [sharedkernel.application.port should only contain interfaces (Outbound Ports)](/rule/layered/sharedkernel-application-port-should-only-contain-interfaces-outbound-ports.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)

## Referenced by ADRs

- [ADR-005: Domain Events Publishing Strategy](/adr/adr-005-domain-events-publishing.md)
- [ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation](/adr/adr-007-hexagonal-architecture.md)
- [ADR-011: Bounded Context Isolation via Package Structure](/adr/adr-011-bounded-context-isolation.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)
- [ADR-019: Open Host Service Pattern for Cross-Context Communication](/adr/adr-019-open-host-service-pattern.md)
- [ADR-027: Integration-Event Contract Identity via @IntegrationEventType](/adr/adr-027-integration-event-contract-identity.md)

## Discussed in

- [Ports & Adapters](/book/06-application-layer/ports-adapters.md)
- [Stores: persistence for non-aggregate data](/book/06-application-layer/stores-persistence-for-non-aggregate-data.md)
- [Base Port Interfaces](/book/11-shared-kernel/base-port-interfaces.md)
- [Ports & Adapters](/book/appendix-a-glossary/ports-adapters.md)
- [Layer Structure](/guide/architecture-reference-guide/layer-structure.md)
- [Key Differences](/guide/clean-architecture-comparison/key-differences.md)
- [ELEMENTS](/guide/readme/elements.md)
- [INTEGRATION PATTERNS](/guide/readme/integration-patterns.md)
- [JAVA PACKAGE STRUCTURE](/guide/readme/java-package-structure.md)
- [RULES](/guide/readme/rules.md)
