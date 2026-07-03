---
type: ADR
title: "ADR-008: Repository Interfaces as Output Ports in Application Layer"
adr: 8
status: accepted
pattern: "Repository interfaces MUST be defined as output ports in the application layer (`application/port/out`), with implementations in secondary adapters (`adapter/outgoing`)."
resource: ai-architecture-sample/docs/architecture/adr/adr-008-repository-interfaces-as-output-ports.md
tags: [adr, repository]
---

Repository interfaces MUST be defined as output ports in the application layer (`application/port/out`), with implementations in secondary adapters (`adapter/outgoing`).

**Consequences:** Dependency Inversion · Clear Output Ports · Framework Independence · Testability · Swappable Implementations · Ubiquitous Language · Clean Architecture · Separation of Concerns

## Applies to markers

- [DomainEventPublisher](/marker/port-out/domaineventpublisher.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [Id](/marker/tactical/id.md)

## Enforced by

- [Repository Implementations must reside in portadapter.outgoing package](/rule/hexagonal/repository-implementations-must-reside-in-portadapter-outgoing-package.md)
- [Repositories must only exist for Aggregate Roots](/rule/tactical/repositories-must-only-exist-for-aggregate-roots.md)
- [Repository Implementations must reside in adapter.outgoing package](/rule/tactical/repository-implementations-must-reside-in-adapter-outgoing-package.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
