---
type: ADR
title: "ADR-016: Shared Kernel Pattern for Cross-Context Value Objects"
adr: 16
status: accepted
pattern: "Implement the Shared Kernel pattern with a dedicated `sharedkernel` package for universal value objects and DDD marker interfaces used across multiple bounded contexts."
resource: ai-architecture-sample/docs/architecture/adr/adr-016-shared-kernel-pattern.md
tags: [adr, strategic, value-object]
---

Implement the Shared Kernel pattern with a dedicated `sharedkernel` package for universal value objects and DDD marker interfaces used across multiple bounded contexts.

**Consequences:** Consistency · Reduced Duplication · Clear Boundaries · Enforced Isolation · Better Communication · Scalability · Coupling · Mitigation

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@BoundedContext](/marker/strategic/boundedcontext.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)
- [DomainEvent](/marker/tactical/domainevent.md)
- [DomainService](/marker/tactical/domainservice.md)
- [Factory](/marker/tactical/factory.md)
- [Specification<T>](/marker/tactical/specification.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
