---
type: ADR
title: "ADR-011: Bounded Context Isolation via Package Structure"
adr: 11
status: accepted
pattern: "Each Bounded Context resides in its own top-level package with strict isolation rules:."
resource: ai-architecture-sample/docs/architecture/adr/adr-011-bounded-context-isolation.md
tags: [adr, package-structure, strategic]
---

Each Bounded Context resides in its own top-level package with strict isolation rules:.

**Consequences:** Clear Ownership · Independent Evolution · Team Organization · Reduced Coupling · Scalability · None identified

## Applies to markers

- [InputPort](/marker/port-in/inputport.md)
- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [AggregateRoot<T, ID>](/marker/tactical/aggregateroot.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
