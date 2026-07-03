---
type: ADR
title: "ADR-019: Open Host Service Pattern for Cross-Context Communication"
adr: 19
status: accepted
pattern: Implement the Open Host Service pattern with provider-side OHS and consumer-side output ports/adapters.
resource: ai-architecture-sample/docs/architecture/adr/adr-019-open-host-service-pattern.md
tags: [adr, strategic]
---

Implement the Open Host Service pattern with provider-side OHS and consumer-side output ports/adapters.

**Consequences:** Application layer isolation · Clear contracts · Interface segregation · Testability · Single point of coupling · Hexagonal compliance · Additional indirection · Mitigation

## Applies to markers

- [OutputPort](/marker/port-out/outputport.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
- [@OpenHostService](/marker/strategic/openhostservice.md)

## Decision process

- [How to write an ADR](/process/creating-an-adr.md)
