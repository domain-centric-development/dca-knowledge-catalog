---
type: Marker
title: "Repository<T, ID>"
category: port-out
kind: interface
signature: "public interface Repository<T extends AggregateRoot<T, ID>, ID extends Id> extends OutputPort"
extends: [OutputPort]
methods: ["Optional<T> findById(ID id)", "T save(T aggregate)", "void deleteById(ID id)"]
resource: ai-architecture-sample/src/main/java/de/sample/aiarchitecture/sharedkernel/marker/port/out/Repository.java
tags: [port-out, marker]
---

Base interface for Repositories.

## Extends

- [OutputPort](/marker/port-out/outputport.md)

## Governed by

- [Controllers and Resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Repository Implementations must reside in portadapter.outgoing package](/rule/hexagonal/repository-implementations-must-reside-in-portadapter-outgoing-package.md)
- [sharedkernel.application.port should only contain interfaces (Outbound Ports)](/rule/layered/sharedkernel-application-port-should-only-contain-interfaces-outbound-ports.md)
- [Repository Interfaces must end with 'Repository'](/rule/naming/repository-interfaces-must-end-with-repository.md)
- [The Domain Model should be framework independent and should not use 3rd party libraries when possible](/rule/onion/the-domain-model-should-be-framework-independent-and-should-not-use-3rd-party-libraries-when-possible.md)
- [Aggregate Roots must not hold references to Repositories or other Output Ports](/rule/tactical/aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)
- [Repository Interfaces must reside in application output port package](/rule/tactical/repository-interfaces-must-reside-in-application-output-port-package.md)
- [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/repository-interfaces-should-extend-repository-marker-interface.md)
- [Repository methods must return Aggregate Roots](/rule/tactical/repository-methods-must-return-aggregate-roots.md)
- [Use cases that save an aggregate must publish its domain events](/rule/usecase/use-cases-that-save-an-aggregate-must-publish-its-domain-events.md)

## Referenced by ADRs

- [ADR-002: Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- [ADR-003: Aggregate Reference by Identity Only](/adr/adr-003-aggregate-reference-by-id.md)
- [ADR-004: Persistence-Oriented Repository Pattern](/adr/adr-004-persistence-oriented-repository.md)
- [ADR-007: Hexagonal Architecture with Explicit Port/Adapter Separation](/adr/adr-007-hexagonal-architecture.md)
- [ADR-008: Repository Interfaces as Output Ports in Application Layer](/adr/adr-008-repository-interfaces-as-output-ports.md)
- [ADR-011: Bounded Context Isolation via Package Structure](/adr/adr-011-bounded-context-isolation.md)
- [ADR-013: Specification Pattern for Business Rules](/adr/adr-013-specification-pattern.md)
- [ADR-015: ArchUnit for Architecture Governance](/adr/adr-015-archunit-governance.md)
- [ADR-016: Shared Kernel Pattern for Cross-Context Value Objects](/adr/adr-016-shared-kernel-pattern.md)
- [ADR-019: Open Host Service Pattern for Cross-Context Communication](/adr/adr-019-open-host-service-pattern.md)
- [ADR-026: Transactional Outbox for Integration Events](/adr/adr-026-transactional-outbox-integration-events.md)

## Discussed in

- [Step 5: Adapter Layer - Repository](/book/03-getting-started/step-5-adapter-layer-repository.md)
- [Repository Interfaces](/book/06-application-layer/repository-interfaces.md)
- [In-Memory Repository](/book/15-persistence-patterns/in-memory-repository.md)
- [JPA Repository Implementation](/book/15-persistence-patterns/jpa-repository-implementation.md)
- [Repository Pattern](/book/15-persistence-patterns/repository-pattern.md)
- [Custom Annotations Placement](/guide/architecture-reference-guide/custom-annotations-placement.md)
- [Framework Annotations Rules](/guide/architecture-reference-guide/framework-annotations-rules.md)
- [Core Rule Categories](/guide/archunit-governance/core-rule-categories.md)
- [ELEMENTS](/guide/readme/elements.md)
- [RULES](/guide/readme/rules.md)
