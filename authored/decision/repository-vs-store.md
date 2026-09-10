---
type: Decision
title: "Repository or Store: which output port persists this"
tags: [decision, tactical, port-out, repository, persistence]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/repository.md, /marker/port-out/store.md, /marker/port-out/outputport.md, /marker/tactical/aggregateroot.md, /rule/tactical/dca-tac-016.md, /rule/tactical/dca-tac-017.md, /rule/tactical/dca-tac-013.md, /rule/tactical/dca-tac-014.md]
---

You need to persist something and reach for an output port. DCA offers two, and they are not interchangeable: a **Repository** persists an Aggregate Root with identity and a lifecycle; a **Store** records operational data that has no aggregate of its own. Both `extend OutputPort`, but the name is a promise to the reader about what lives behind it — pick wrong and you either invent a fake aggregate or hide a real one behind a `record()` call.

## The discriminator

Ask, in order:

1. **Does the thing you persist have identity and a lifecycle?** Do you load it by ID, mutate it, and save it back? Yes → **Repository**. The object is a managed Aggregate Root.
2. **Are you appending records and aggregating over them?** `record(...)`, `count(...)`, `exists(...)` rather than `findById` / `save` / `delete`? → **Store**. The data is recorded, not managed — login attempts, audit trail, metric snapshots, technical state.
3. **Is the stored thing a Value Object or a `record` by nature?** No mutable identity worth retrieving individually → almost always a **Store**.

Rule of thumb straight from the guidance: *need `findById()`? Repository. Need `record()` or `count()`? Store.*

## Options

| | Repository | Store |
|---|---|---|
| What it persists | an **Aggregate Root** | Value Object / event / operational data |
| Identity & lifecycle | yes — `findById`, `save`, `deleteById` | no — `record`, `count`, `exists` |
| Marker | `extends Repository<T, ID>` | `extends Store` |
| One per | Aggregate Root | concern (login attempts, audit trail, …) |
| Return type | the Aggregate Root | answers about recorded data, not a managed entity |

A hard constraint sits under this fork: **a Repository may only exist for an Aggregate Root**, and its methods must return that root. So the choice is not free — if the data is not an aggregate, you *cannot* correctly model its port as a Repository; it must be a Store. The `EventStore` of Event Sourcing is a specialization of Store, not a Repository.

## Consequences

- A Repository whose target type does not implement `AggregateRoot` fails the ArchUnit check "Repositories must only exist for Aggregate Roots" (see anchors). This is the mechanical guard against faking aggregates just to get persistence.
- Both markers keep persistence out of the domain: the *interface* lives in the application layer's output-port package, the *implementation* in `adapter.outgoing`. That direction holds for Store and Repository alike.
- Name the port for its role. A reader must know from `LoginProtectionStore` vs `OrderRepository` — without opening the implementation — whether they are dealing with recorded operational data or a managed Aggregate Root.

## Anchors

- Markers: [Repository&lt;T, ID&gt;](/marker/port-out/repository.md) · [Store](/marker/port-out/store.md) · [OutputPort](/marker/port-out/outputport.md) · [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md)
- Rules: [Repositories must only exist for Aggregate Roots](/rule/tactical/dca-tac-016.md) · [Repository methods must not return non-root Entities](/rule/tactical/dca-tac-017.md) · [Repository Interfaces should extend Repository Marker Interface](/rule/tactical/dca-tac-013.md) · [Repository Interfaces must reside in application output port package](/rule/tactical/dca-tac-014.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Deviations from the literature](/guide/readme/deviations-from-the-literature.md) · [Layer elements](/guide/readme/elements.md)
- Recipes: [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md) · [Add an aggregate](/recipe/add-an-aggregate.md)
- Rules enforcing the Store side: [extends the Store marker](/rule/tactical/dca-tac-018.md) · [interface in application.shared](/rule/tactical/dca-tac-019.md) · [implementation in adapter.outgoing](/rule/tactical/dca-tac-020.md) · [no findById/save](/rule/tactical/dca-tac-021.md)
