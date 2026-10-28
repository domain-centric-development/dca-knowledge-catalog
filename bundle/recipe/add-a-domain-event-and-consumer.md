---
type: Recipe
title: Add a domain event and consumer
tags: [recipe, domain, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /guide/spring-modulith/module-communication.md, /rule/advanced/dca-adv-001.md, /rule/advanced/dca-adv-008.md, /rule/advanced/dca-adv-002.md, /rule/advanced/dca-adv-004.md, /rule/advanced/dca-adv-007.md, /marker/tactical/domainevent.md, /guide/rules.md]
---

Record that something meaningful happened in the domain, and let another part of the *same* context react to it. A past-tense record implementing `DomainEvent`, registered on the aggregate, published by the use case after save, consumed in-process. If the reaction crosses a context boundary, this is the wrong recipe.

## Step 0 — decide (do this first)

Does the consumer live in another bounded context or an external system? Then you need an integration event, not a raw domain event — see [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md) and [Publish a cross-context event](/recipe/publish-a-cross-context-event.md). Otherwise continue.

## Steps

1. **Define the event** as a record implementing `DomainEvent`, in the aggregate's `domain/` package. Name it past tense (`{Something}Happened`). Include the `occurredOn` timestamp; no `version` field (integration events declare their version via `@IntegrationEventType`, domain events have none).
2. **Register it on the aggregate** during the state change that causes it — never construct-and-forget. Generate from the [domain-event template](/template/domain-event.md).
3. **Publish after persistence** — the use case saves the aggregate, then publishes and clears the registered events (`publishAndClearEvents`, inside `@Transactional` or a `TransactionBoundary` block). No events escape before the transaction commits. On Spring the publisher is `SpringDomainEventPublisher` from the `dca-spring` dependency, auto-configured — nothing to write; check that a transaction manager exists, or the after-commit consumer is skipped silently ([pitfall](/pitfall/declarative-transaction-without-a-transaction-manager.md)).
4. **Consume in-context** — decide the listener kind first ([Reacting to an event](/decision/reacting-to-an-event.md)). A reaction that changes state or performs an external effect is a **transactional listener**: an incoming adapter in `adapter/incoming/event/` that maps the event to a command and calls an input port, delivered after the commit from the outbox (`@ApplicationModuleListener` with the event publication registry, or the project's own outbox and worker). Generate it from the [event consumer template](/template/event-consumer.md). The use case checks idempotency per event id. A synchronous listener (`@EventListener`) is only for what calls output ports — a translator, a metric. Depend on the event type, not the publishing use case; for Spring Modulith, invert the dependency so the listener owns the interface ([Module communication](/guide/spring-modulith/module-communication.md)).
5. **Keep the domain framework-free** — no Spring annotations on the event record itself.
6. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project).

## Rules to satisfy (build-time checklist)

- [Domain events must implement the DomainEvent marker and be records](/rule/advanced/dca-adv-001.md)
- [Domain events must have a timestamp field](/rule/advanced/dca-adv-008.md)
- [Domain events must reside in the domain package](/rule/advanced/dca-adv-002.md)
- [Domain events must not have Spring annotations](/rule/advanced/dca-adv-004.md)
- [Domain events that are not integration events must not have a version field](/rule/advanced/dca-adv-007.md)

## Anchors

- Templates: [Domain event skeleton](/template/domain-event.md) · [Event consumer skeleton](/template/event-consumer.md)
- Decisions: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md) · [Reacting to an event](/decision/reacting-to-an-event.md)
- Pitfalls: [A reaction in the raising transaction](/pitfall/reaction-in-the-raising-transaction.md) · [A stored domain event changed like code](/pitfall/stored-domain-event-changed-like-code.md)
- Marker: [DomainEvent](/marker/tactical/domainevent.md)
- Guide: [Layer rules](/guide/rules.md) · [Module communication](/guide/spring-modulith/module-communication.md) · [Integration patterns](/guide/integration-patterns.md)
- Events are raised inside an [aggregate](/recipe/add-an-aggregate.md); to cross a boundary use [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
