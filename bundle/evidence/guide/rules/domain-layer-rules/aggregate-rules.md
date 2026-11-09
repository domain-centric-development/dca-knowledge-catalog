---
type: Reference
title: DOMAIN LAYER RULES — Aggregate Rules
tags: [reference]
evidence_for: "/guide/rules/domain-layer-rules.md#aggregate-rules"
---

[Full node and context](/guide/rules/domain-layer-rules.md#aggregate-rules). This is an evidence excerpt; retain the parent selection and caveats.

### Aggregate Rules
- Access external objects only through Aggregate Root
- Aggregate Root is an Entity
- Aggregate defines transactional boundary
- Aggregate maintains invariants at all times
- Small aggregates preferred
- Reference other aggregates by ID only, not object reference
- One transaction modifies one aggregate only
- Eventual consistency between aggregates
- Delete aggregate deletes all contained entities
- Never inject repositories or remote services into aggregates. Use cases retrieve facts; domain services calculate over supplied snapshots. A callback parameter does not make external-data responsibility belong on the aggregate.
- Every change of state is a method of the root, named after what it means (`complete()`, `reopen()`). No adapter
  writes a lifecycle field — a status, a delivered flag, an applied mark — straight into storage: such a change has no
  guard and raises no event, and the state now has two ways in. The repository's adapter writes only what the
  aggregate holds. A store whose port takes a status to set is the same lifecycle without its aggregate
- A decision asks the aggregate. A copy of its state — a read model, a list of accepted words, a prefix check on a
  stored field — answers for display only and never decides: it decides the same thing a second time and drifts
  from the aggregate the first time a rule changes
- Two factories, two purposes: `create(...)` enforces creation invariants and registers the creation event; `reconstitute(...)` rebuilds a stored aggregate from persisted state and registers nothing. Persistence adapters use only the latter — rebuilding through `create` publishes a phantom creation on the next save
- Domain events leave the aggregate through one call, `DomainEventPublisher.publishAndClearEvents(aggregate)`, after the save: dispatch everything, clear only when every listener returned. Iterating `domainEvents()` and calling `publish` per event is not the sanctioned form
- Protect against lost updates with optimistic concurrency: version field on the root, incremented per state change; persistence rejects saves with a stale expected version
