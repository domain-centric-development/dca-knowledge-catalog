---
type: Recipe
title: Build a DCA application
tags: [recipe, bootstrap, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/index.md, /marker/index.md, /guide/package-structure.md, /guide/index.md]
---

The task router: maps what you are building to the recipe that covers it. Start
here when constructing anything in a Domain-Centric Architecture application —
each recipe carries ordered steps, the ArchUnit rules to satisfy while
generating, and the template to fill in.

## Route by task

| You want to… | Recipe |
|---|---|
| Start a fresh application (markers, skeleton, ArchUnit suite) | [Bootstrap a new application](/recipe/bootstrap-a-new-application.md) |
| Add a bounded context | [Add a bounded context](/recipe/add-a-bounded-context.md) |
| Add an aggregate (root entity + invariants) | [Add an aggregate](/recipe/add-an-aggregate.md) |
| Add a value object | [Add a value object](/recipe/add-a-value-object.md) |
| Add a use case (application service) | [Add a use case](/recipe/add-a-use-case.md) |
| Add a repository (output port + adapter impl) | [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) |
| Expose a use case over HTTP | [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md) |
| Expose a use case to an AI agent (MCP) | [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md) — see the [MCP tool provider skeleton](/template/mcp-tool-provider.md) |
| Raise and handle an in-context domain event | [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md) |
| Notify another bounded context | [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) |
| Integrate a foreign model without polluting the domain | [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md) |
| Test an aggregate (invariants, state, domain events) | [Test an aggregate](/recipe/test-an-aggregate.md) |
| Test a use case (Command/Query → Result, fake output ports) | [Test a use case](/recipe/test-a-use-case.md) |
| Move a repository adapter from in-memory to a database | [Swap in-memory for JPA](/recipe/swap-in-memory-for-jpa.md) |
| Add a read-optimized model for a query | [Add a read model](/recipe/add-a-read-model.md) |
| Expose a bounded context's API to other contexts | [Expose an open host service](/recipe/expose-an-open-host-service.md) |
| Persist operational data that has no aggregate of its own | [Add a store](/recipe/add-a-store.md) |
| Know who is calling — and keep ownership checks in the use case | [Add an identity port](/recipe/add-an-identity-port.md) |

## Decide first (design forks)

When the task sits on a fork, resolve the decision before picking the recipe:

**Modelling (tactical):**

- [Entity vs Value Object](/decision/entity-vs-value-object.md)
- [Aggregate boundary and size](/decision/aggregate-boundary-size.md)
- [Where does the logic live](/decision/where-does-the-logic-live.md) — aggregate, domain service, or use case
- [Factory vs constructor](/decision/factory-vs-constructor.md)
- [ID generation strategy](/decision/id-generation-strategy.md)
- [Specification vs query method](/decision/specification-vs-query-method.md)
- [Repository vs Store](/decision/repository-vs-store.md)

**Events & integration:**

- [Domain event vs integration event](/decision/domain-event-vs-integration-event.md)
- [Event delivery: sync, async, and the outbox](/decision/event-delivery-sync-async-and-outbox.md)
- [Cross-context communication](/decision/cross-context-communication.md) — sync call vs event, orchestration vs choreography

**Strategic & structure:**

- [New context vs extend an existing one](/decision/new-context-vs-extend-existing.md)
- [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md) — not every context needs the full tactical set
- [Shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md)
- [Read model vs domain query](/decision/read-model-vs-domain-query.md)
- [Modulith vs microservice extraction](/decision/modulith-vs-microservice-extraction.md)

## Build loop (every recipe)

1. **Decide** — resolve any design fork the recipe gates on.
2. **Generate** — emit from the linked template; satisfy the recipe's
   "Rules to satisfy" checklist *while* generating (each entry links a
   [rule](/rule/index.md) whose `constraint:` is the one-line precondition).
3. **Verify** — run the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project); the ArchUnit suite enforces
   what the checklist promised.
4. **Record** — a non-trivial pattern choice gets an ADR
   ([Creating an ADR](/process/creating-an-adr.md)).

## Anchors

- Contracts: [marker index](/marker/index.md) — the interfaces a new application implements
- Layer map: [Package structure](/guide/package-structure.md)
- What NOT to do: [pitfall index](/pitfall/index.md)
- Concepts in depth: [guide index](/guide/index.md)

## Verification by language

Java: the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project) (or the project Maven architecture-test target).
.NET: `dotnet test -c Debug` against the architecture-test project and all production assemblies.
Read the resolved framework preset; do not add Spring to a .NET or framework-neutral consumer.
