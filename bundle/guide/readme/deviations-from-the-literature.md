---
type: Section
title: DEVIATIONS FROM THE LITERATURE
chapter: Domain-Centric Architecture
source: guide
resource: dca-guide/README.md
tags: [guide, section]
---

DCA deliberately deviates from classic DDD literature in a few places. The deviations are conscious decisions, not oversights:

### Repository Interfaces in the Application Layer

Classic DDD (Evans, Vernon, Millett/Tune) places repository interfaces in the domain layer. DCA places them in the application layer as **output ports**: the use case owns the contract for what it needs from the outside world, the domain stays free of persistence concerns entirely. This follows Hexagonal/Clean Architecture port ownership consistently.

The rejected alternative is worth naming: keeping the interface in the domain layer means the domain declares what it wants from persistence, which reads as independence but is not. The signature — what can be looked up, by what, returning what — is shaped by the use cases that call it, so the domain would be declaring a contract on someone else's behalf and would have to change whenever a use case's needs change.

### Repository vs. Store

The literature knows only the Repository (one per aggregate root). DCA refines this with a second output-port type, the **Store**, for operational data without aggregate lifecycle (value objects, technical state) — see [Repository vs. Store](#repository-vs-store).

### Results Instead of Output Ports, Assembled on the Application Side

Clean Architecture (Martin) lets the interactor hand its output data to a presenter through an output port; the presenter builds the view model. DCA returns the result: `UseCase<INPUT, OUTPUT>` yields a `*Result`, and the incoming adapter maps it to a `*Response` or `*ViewModel`. Two mapping steps, one direction of call, no callback interface per use case.

Vernon (*Implementing DDD*, "Rendering Domain Objects") offers the **Domain Payload Object** — handing whole aggregates to an in-process UI — and the **Mediator** (double dispatch into a rendering interface) as alternatives to a DTO assembler. DCA takes neither, not even for an in-process UI: every adapter gets the same result model, REST and MCP are remote anyway, and a result that carries an aggregate root or entity is a rule violation (`DCA-USE-015`). What the literature agrees on is kept: no entity crosses the use-case boundary, the application layer assembles the business result (Fowler's *Assembler* is the name for the class when a static factory no longer suffices), and the incoming adapter formats without deriving business facts.

The restriction is deliberately asymmetric. An incoming adapter reads and formats what a result delivers — including the own queries of a delivered value or read model — and operates no domain object; it obtains no domain service (`DCA-HEX-012`), constructs nothing and combines nothing into a new business fact. An outgoing adapter — a repository, a persistence mapper — necessarily constructs and reconstitutes domain objects while implementing an output port; it restores state and makes no new business decision.

### Pragmatic Domain-Layer Dependencies

"Framework-free domain" is enforced strictly for frameworks (Spring, JPA, Jackson, messaging), but compile-time-only conveniences without runtime coupling (Lombok, `commons-lang3`, JSpecify nullability annotations) are permitted. The boundary is behavioral coupling, not the import statement.

## Related markers

- [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- [Repository<T, ID>](/marker/port-out/repository.md)
