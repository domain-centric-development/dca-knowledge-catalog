---
type: Decision
title: Register domain events nobody listens to yet?
tags: [decision, domain, domain-event, events, aggregate, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainevent.md, /marker/port-out/domaineventpublisher.md, /marker/tactical/baseaggregateroot.md, /rule/usecase/dca-use-009.md, /guide/readme/rules.md]
---

An aggregate's `create` and `complete` methods could register `{Name}Created` and `{Name}Completed` — but no listener exists in the context, and none is planned for this iteration. The fork is whether the aggregate **registers the events anyway** and the use case publishes into silence, or whether it **registers nothing** until a consumer appears. The publish call itself is not part of the decision: a saving use case calls `publishAndClearEvents` in both cases, because the rule demands it whenever `save` is called.

## The discriminator

**Is the fact meaningful in the domain language today?** If the domain experts say "a task is *completed*", "an order is *cancelled*", the event names a business fact that exists whether or not code reacts to it. If the change is a field edit nobody talks about as an event — "the description was updated", "the colour changed" — there is no fact to record, only a mutation.

Two secondary questions:

1. **Does the event carry information the aggregate would otherwise forget?** A `TaskCompleted` with the completion instant and who completed it preserves what the aggregate's current state alone may not show. That argues for registering it now, since adding it later means the fact was never captured.
2. **Would a consumer be in the same context?** If the only plausible reaction lies in another bounded context, the artefact that will eventually be needed is an integration event, not a domain event — see [Domain event or integration event](/decision/domain-event-vs-integration-event.md). Registering a domain event "in preparation" then prepares the wrong thing.

## Options

### Register anyway and publish

The aggregate registers `{Name}Created` in `create` and `{Name}Completed` in `complete`; the use case saves and calls `publishAndClearEvents`, which dispatches to zero listeners. Cost: one record per event and one `registerEvent` line per method — the publish call is required by the rule regardless. Benefit: the events document the business facts where the code lives, the event list of the aggregate becomes a readable summary of its lifecycle, and a consumer plugs in later without touching the aggregate.

- **When:** the fact has a name in the ubiquitous language; the domain model is a core or supporting subdomain where events are expected to grow.
- Build it: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md) (stop before the consumer step)

### Register nothing yet

The aggregate mutates state and registers no event; the use case still saves and calls `publishAndClearEvents`, which publishes nothing and clears nothing. When a consumer appears, the event record and the `registerEvent` call are added together with it.

- **When:** the change is CRUD-shaped and nobody names it as a fact; a supporting context with transaction-script style where events would be ceremony.
- Watch: the fact is not captured retroactively — an aggregate completed before the event existed never produced `{Name}Completed`.

**Default:** **register anyway** for facts the domain names — created, completed, cancelled, shipped, expired. **Register nothing** for pure CRUD-ish changes such as editing a description or reordering a list. Never skip the `publishAndClearEvents` call to save a line: the rule fails the use case, and the next developer who adds an event would have to remember the publish as well.

## Anchors

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) · [BaseAggregateRoot](/marker/tactical/baseaggregateroot.md)
- Rules: [Use cases that save an aggregate must publish its domain events](/rule/usecase/dca-use-009.md)
- Guide: [Layer rules](/guide/readme/rules.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
- Related decisions: [Domain event or integration event](/decision/domain-event-vs-integration-event.md) · [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Templates: [Aggregate root skeleton](/template/aggregate-root.md) · [Domain event](/template/domain-event.md)
