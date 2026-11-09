---
type: Section
title: APPLICATION LAYER RULES
chapter: Rules
source: guide
resource: dca-guide/architecture/rules.md
tags: [guide, section]
---

### Use Case / Application Service Rules
- One use case class per business operation
- A use case is named after an operation of the glossary: its code word plus the term (`PlaceOrder`,
  `CancelOrder`); a verb the glossary does not name is a question, not a choice
- A use case is named after its effect, never after its trigger or its caller: `ArchiveEntry`, not
  `ArchiveEntryOnExpiry` or `ArchiveEntryAfterLogin`. When and by whom it runs is the business of the adapter or
  the consumer that calls it; the same effect reached from a second trigger is the same use case
- An operation speaks the domain, not data access. Neither a use case nor an operation of the context's published
  API is named after a field it writes (`setLimit`, `updateStatus`); it is named after what the change means
  (`RaiseLimit`, `GrantInitialLimit`), with the verb from the glossary
- Use case implements Input Port interface
- Use case orchestrates domain objects
- Use case is thin, delegates to domain
- A use case keeps no state between calls: what it holds is set once, by its constructor — the ports and services
  it is wired with. A field it writes while it runs is shared by every caller of the one instance
- Use case calls Output Ports for infrastructure
- Use case handles transaction boundaries
- Use case transforms DTOs to domain objects
- Use case transforms domain objects to DTOs
- Use case assembles the `*Result` (static factory, use-case body or `*Assembler`); a result carries values, never aggregate roots or entities (`DCA-USE-015`)
- Command results are small (ids, status, what the caller needs next); the view comes from a query or read model
- A use case that saves an aggregate publishes and clears its domain events after the save (`publishAndClearEvents`, `DCA-USE-009`) — unless the aggregate is proven never to register events
- A query use case carries no transaction and no publisher; it loads and assembles
- A read never creates. A query has no side effect: it does not create, save or publish, and when nothing exists
  it answers *none* — an empty value, not a refusal, where the caller asks whether there is one ("which one, if
  any"); a refusal only where it names a specific thing by id. Find-or-create is a command, called where the
  caller is about to change state; a page or an answer that only shows what exists asks the query
- A bulk operation (delete all, archive everything before a date) is a method on the port — the port is freely extensible beyond `findById`/`save`/`deleteById` — that the use case calls without loading or saving a single aggregate: no domain event, no publisher, a declarative transaction. If other contexts must learn about it, one integration event describes the bulk fact
- A number derived from a list (the count of open items on a list page) is a field of the list query's result, not a use case of its own and not a read model
- No business logic in use cases
- Use case tested with port mocks
- Use case knows nothing about presentation
- Use case knows nothing about persistence details

### Authorization Rules
- Authorization ("may *this caller* do this?") is decided in the use case; the caller arrives as a field of the Command/Query, resolved by the incoming adapter through the identity output port
- A use case that acts on a caller's resource asks the repository a scoped question (`findByIdForCustomer`), never an open lookup followed by a comparison
- A claims-only gate (a role on the token) may sit in the incoming adapter — it reads nothing but the caller
- Say the claims-only gate declaratively, on the route, in the framework's own form: an authorization annotation or
  attribute on the handler (`@PreAuthorize`, `@RolesAllowed`, `[Authorize(Roles = …)]`), or — where the stack has no
  annotations — an extractor in the handler's signature or a layer on its route. A branch on the caller's role inside
  the handler hides the gate from whoever reads the route and renders whatever status the branch writes, where the
  framework would tell an unauthenticated from an unauthorized caller. The project adds no marker of its own beside
  the framework's: the framework's declaration is the declaration. `DCA-HEX-020` (experimental, informational) lists
  an incoming adapter that asks for the caller's roles in its own code. The split is by input: a check that needs
  nothing but the caller sits on the route; a check that needs the stored data — is this yours? — is the use case's
- The domain never knows the caller: no `User` parameter on aggregate methods, no role checks in domain code — invariants only
- The identity port is a project-specific output port in `application/shared/` (context or shared kernel), implemented in the authenticating context's outgoing adapter; the authentication filter enriches every request and gates none
- A use case with no caller (event consumers, scheduled work) checks no caller, but it still loads an owned aggregate
  through the owner its trigger names — an event that asks for an effect on somebody's aggregate carries whose it is.
  Only a path that holds no owner to name uses the unscoped lookup, and documents it
- Ownership is the data-dependent half of authorization ("is this yours?"): it needs the stored aggregate, so it is
  the use case's, never a route annotation's — see *Owned aggregates* below

### Input Port Rules
- Input Port defines use case interface
- Input Port represents business operation
- One Input Port per use case
- Input Port uses domain language
- Input Port accepts Input Data/DTOs
- Input Port returns `<Operation>Result` — in a context that returns its refusals sealed, with one case per expected
  refusal, when the operation has one
- Input Port has no framework dependencies
- Input Port belongs to application layer

### Output Port Rules
- Output Port defines a capability the application needs but does not own — persistence, another context, an external system, messaging, the caller's identity — declared in the application's language and fulfilled by an adapter, in-memory or remote alike
- Output Port is called by a use case — or by an incoming adapter that translates request context into the project's language (the identity port); an interface that only serves adapter mechanics is not a port
- Output Port uses domain language and types
- Output Port implemented by adapters
- Output Port has no framework dependencies
- Output Port belongs to application layer
- Repository interfaces are Output Ports
- Event Publisher interfaces are Output Ports
- Not Output Ports: a transaction boundary (execution semantics), cookies, tokens and sessions (adapter mechanics), a question into the own context dressed as an output port (a query use case or the published API)

### Repository Interface Rules
- Repository interface in application layer
- Repository returns Aggregate Roots only
- One repository interface per Aggregate Root
- Repository provides collection-like interface
- Repository uses domain types, not DTOs
- Repository manages object lifecycle
- Repository implementation in adapter layer
- **Repository reads return copies, never the stored instance** — see below

#### A repository hands out copies

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

#### Owned aggregates

An aggregate that belongs to someone — a patient's record, a tenant's workspace, a visitor's draft — implements
`Owned<OwnerId>` (`IOwned<TOwnerId>` in C#, `impl Owned { type OwnerId = … }` in Rust), the type argument naming the
owner's id type. Its repository then declares a lookup by the aggregate's id **and** the owner's id —
`findByIdForOwner(id, ownerId)`, named in the context's language — and every use case acting for a caller loads the
aggregate through it. An object loaded by its id alone is reachable by anyone who knows or guesses the id: the
insecure direct object reference of broken access control, OWASP Top 10 **A01**. `DCA-TAC-026` (experimental) checks
the repository side — an owned aggregate whose repository offers only `findById` fails; whether the use case calls the
scoped lookup is a review question, and an aggregate nobody marked is not selected at all.

- **The owner may change, but only explicitly.** `Owned` says "has an owner", not "always the same owner". A
  visitor's draft taken over by the account they sign into changes owner through an operation of the aggregate
  (`takeOverBy(account)`), called after the use case proved the caller's right to it — for example that the guest
  identity named in the signed token is the draft's owner. That proof is use-case logic no marker can verify; its
  tests prove it. Before and after the change, both aggregates are found through their owner.
- **A guest is an owner.** A visitor given a pseudonymous identity on the first request owns what they create; the
  scoped lookup works the same for them. The identity is safe when it comes from a signed token and is not guessable —
  never a value the client names. Registering keeps the identity, so nothing moves.
- **Where `Owned` does not fit.** A system without any identity for guests, where the aggregate's id itself is the
  secret — a long random id in a link, "whoever holds it may" — has no owner to scope a lookup by. Such an aggregate is
  not `Owned`; its safety is the id's unguessability, and that is a deliberate choice, not an omission.

### Transaction Rules
- One transaction per use case execution
- Transaction boundaries managed by use case
- Transaction spans single aggregate modification
- Cross-aggregate changes use eventual consistency

## Related mentions (heuristic)

- [Repository<T, ID>](/marker/port-out/repository.md)
