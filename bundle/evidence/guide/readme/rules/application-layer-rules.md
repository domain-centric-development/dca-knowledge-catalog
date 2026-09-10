---
type: Reference
title: RULES — APPLICATION LAYER RULES
tags: [reference]
evidence_for: "/guide/readme/rules.md#application-layer-rules"
---

[Full node and context](/guide/readme/rules.md#application-layer-rules). This is an evidence excerpt; retain the parent selection and caveats.

### APPLICATION LAYER RULES

#### Use Case / Application Service Rules
- One use case class per business operation
- Use case implements Input Port interface
- Use case orchestrates domain objects
- Use case is thin, delegates to domain
- Use case calls Output Ports for infrastructure
- Use case handles transaction boundaries
- Use case transforms DTOs to domain objects
- Use case transforms domain objects to DTOs
- Use case assembles the `*Result` (static factory, use-case body or `*Assembler`); a result carries values, never aggregate roots or entities (`DCA-USE-015`)
- Command results are small (ids, status, what the caller needs next); the view comes from a query or read model
- A use case that saves an aggregate publishes and clears its domain events after the save (`publishAndClearEvents`, `DCA-USE-009`) — unless the aggregate is proven never to register events
- A query use case carries no transaction and no publisher; it loads and assembles
- A bulk operation (delete all, archive everything before a date) is a method on the port — the port is freely extensible beyond `findById`/`save`/`deleteById` — that the use case calls without loading or saving a single aggregate: no domain event, no publisher, a declarative transaction. If other contexts must learn about it, one integration event describes the bulk fact
- A number derived from a list (the count of open items on a list page) is a field of the list query's result, not a use case of its own and not a read model
- No business logic in use cases
- Use case tested with port mocks
- Use case knows nothing about presentation
- Use case knows nothing about persistence details

#### Authorization Rules
- Authorization ("may *this caller* do this?") is decided in the use case; the caller arrives as a field of the Command/Query, resolved by the incoming adapter through the identity output port
- A use case that acts on a caller's resource asks the repository a scoped question (`findByIdForCustomer`), never an open lookup followed by a comparison
- A claims-only gate (a role on the token) may sit in the incoming adapter — it reads nothing but the caller
- The domain never knows the caller: no `User` parameter on aggregate methods, no role checks in domain code — invariants only
- The identity port is a project-specific output port in `application/shared/` (context or shared kernel), implemented in the authenticating context's outgoing adapter; the authentication filter enriches every request and gates none
- A use case with no caller (event consumers, scheduled work) stays unscoped and documents it

#### Input Port Rules
- Input Port defines use case interface
- Input Port represents business operation
- One Input Port per use case
- Input Port uses domain language
- Input Port accepts Input Data/DTOs
- Input Port has no framework dependencies
- Input Port belongs to application layer

#### Output Port Rules
- Output Port defines infrastructure need
- Output Port uses domain language and types
- Output Port implemented by adapters
- Output Port has no framework dependencies
- Output Port belongs to application layer
- Repository interfaces are Output Ports
- Event Publisher interfaces are Output Ports

#### Repository Interface Rules
- Repository interface in application layer
- Repository returns Aggregate Roots only
- One repository interface per Aggregate Root
- Repository provides collection-like interface
- Repository uses domain types, not DTOs
- Repository manages object lifecycle
- Repository implementation in adapter layer
- **Repository reads return copies, never the stored instance** — see below

##### A repository hands out copies

This is where the collection metaphor stops. A `Map`-backed adapter that returns `store.get(id)`
hands out the instance it holds, so a caller who mutates an aggregate has already changed the store
and `save()` is decoration. Against a database the same code loses the change silently, because
loading a row constructs a new object — so the in-memory adapter has been hiding a missing `save()`
in exactly the tests meant to catch it.

Every adapter therefore maps back through the aggregate's `reconstitute` factory: the JDBC/JPA one
because a row leaves it no choice, the in-memory one on purpose (copy on write *and* on read).
Registered-but-unpublished domain events are not carried over — a stored aggregate is a fact, and
re-reading it must not replay what the writer already published.

Keep the adapters honest with a **contract test on the port** that every implementation runs,
including the assertion that an unsaved mutation is invisible to the next reader.

#### Transaction Rules
- One transaction per use case execution
- Transaction boundaries managed by use case
- Transaction spans single aggregate modification
- Cross-aggregate changes use eventual consistency
