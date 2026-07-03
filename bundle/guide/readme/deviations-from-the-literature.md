---
type: Section
title: DEVIATIONS FROM THE LITERATURE
chapter: Domain-Centric Architecture
source: guide
resource: implementing-domain-centric-architecture/README.md
tags: [guide, section]
---

DCA deliberately deviates from classic DDD literature in a few places. The deviations are conscious decisions, not oversights:

### Repository Interfaces in the Application Layer

Classic DDD (Evans, Vernon, Millett/Tune) places repository interfaces in the domain layer. DCA places them in the application layer as **output ports**: the use case owns the contract for what it needs from the outside world, the domain stays free of persistence concerns entirely. This follows Hexagonal/Clean Architecture port ownership consistently. See [ADR-008 in the reference implementation](https://github.com/chbloemer/ai-architecture-sample/blob/main/docs/architecture/adr/adr-008-repository-interfaces-as-output-ports.md) for the full rationale and rejected alternatives.

### Repository vs. Store

The literature knows only the Repository (one per aggregate root). DCA refines this with a second output-port type, the **Store**, for operational data without aggregate lifecycle (value objects, technical state) — see [Repository vs. Store](#repository-vs-store).

### Pragmatic Domain-Layer Dependencies

"Framework-free domain" is enforced strictly for frameworks (Spring, JPA, Jackson, messaging), but compile-time-only conveniences without runtime coupling (Lombok, `commons-lang3`, JSpecify nullability annotations) are permitted. The boundary is behavioral coupling, not the import statement.

## Related markers

- [Repository<T, ID>](/marker/port-out/repository.md)

## Related ADRs

- [ADR-008: Repository Interfaces as Output Ports in Application Layer](/adr/adr-008-repository-interfaces-as-output-ports.md)
