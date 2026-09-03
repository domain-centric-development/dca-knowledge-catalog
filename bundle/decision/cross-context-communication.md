---
type: Decision
title: "Cross-context communication: synchronous call or integration event"
tags: [decision, strategic, bounded-context, integration-event, events, anti-corruption-layer, port-out]
---

Two bounded contexts need to interact. The fork is **how**: a **synchronous call** to the provider (the consumer asks and blocks for an answer) or an **asynchronous integration event** (the provider announces a fact and the consumer reacts later). Get this wrong and you either couple two contexts into one distributed lockstep, or you build eventual-consistency machinery for a query that needed an answer *now*.

Whichever you pick, the boundary rules are non-negotiable: the consumer's use cases depend only on an output port defined in *their own* `application/shared/`; foreign types never reach past the adapter; and anything crossing the wire is a DTO or a versioned `IntegrationEvent`, never a domain object.

## The discriminator

Ask, in order:

1. **Does the consumer need an answer to proceed right now?** If the use case cannot continue without the provider's data (a price to total a cart, stock to validate a checkout), it is a **synchronous query**. If the consumer only needs to *know a fact happened* and can act on its own afterward (reserve stock after an order was placed), it is an **asynchronous event**.
2. **Who owns the timing — caller or event?** A caller that drives the interaction and waits is synchronous (request/response). A reaction triggered by something that already happened, with no caller waiting, is asynchronous (publish/subscribe).
3. **Can the two contexts tolerate eventual consistency?** If a short window where the consumer hasn't caught up is acceptable, prefer events — they decouple the two contexts' availability and release cycles. If the business demands immediate consistency, you need the synchronous call.
4. **For multi-step workflows: orchestration or choreography?** If one context must *coordinate* a sequence and knows the whole flow, an orchestrating use case making synchronous calls is clearer. If each context should react independently to facts, choreograph with events — no central coordinator.

## Options

### Synchronous call — Open Host Service + consumer output port

The provider publishes an **Open Host Service**: a REST API (an incoming adapter, e.g. `adapter/incoming/api/`, canonical) or, in a modulith, an in-process `@OpenHostService` in the context's published `api/` package — same relationship, different transport — that calls its own use cases and returns DTOs. The consumer defines its **own** output port in `application/shared/` stating exactly what it needs, and an outgoing adapter in `adapter/outgoing/{context}/` implements it against the OHS. Only the adapter changes when you later move the provider to a separate service — use cases and ports stay identical.

- **When:** the consumer needs data to proceed; immediate consistency; a query with a caller waiting for the answer.
- Provider marker: [@OpenHostService](/marker/strategic/openhostservice.md) · consumer port: [OutputPort](/marker/port-out/outputport.md)
- Governed by [Open Host Service pattern](/guide/readme/integration-patterns.md)

### Synchronous call through a domain gateway / anti-corruption layer

When the provider is an external system or a peer whose model differs from yours, wrap the synchronous call in an **anti-corruption layer**: the outgoing adapter (an `acl` package) translates the foreign contract to your domain types so nothing foreign leaks inward. The use case depends on a [DomainGateway](/marker/tactical/domaingateway.md)-style output port in your terms.

- **When:** synchronous, but the foreign model must not shape yours; conforming would corrupt your ubiquitous language.
- Build it: [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)

### Asynchronous integration event

The provider raises a `DomainEvent` internally; an ACL translates it to a versioned `IntegrationEvent` and captures it in a transactional outbox inside the publishing transaction; a relay sends it to the broker. The consumer receives it in `adapter/incoming/messaging/`, translates back through *its* ACL, and invokes its own use case.

- **When:** the consumer only needs to know a fact happened; eventual consistency is acceptable; you want the contexts decoupled in availability and deployment; choreographed workflows.
- Markers: [DomainEvent](/marker/tactical/domainevent.md) → [IntegrationEvent](/marker/tactical/integrationevent.md)
- Build it: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) · delivery details: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md)

**Default:** prefer the **asynchronous integration event** unless the consumer genuinely needs an answer to proceed — it keeps the two contexts independently deployable and available, which is the whole point of the boundary. Reach for the synchronous OHS call when a use case cannot continue without the provider's data. Never share a database between contexts and never let the application layer import another context directly — both collapse the boundary into hidden coupling.

## Anchors

- Markers: [@OpenHostService](/marker/strategic/openhostservice.md) · [OutputPort](/marker/port-out/outputport.md) · [DomainGateway](/marker/tactical/domaingateway.md) · [DomainEventPublisher](/marker/port-out/domaineventpublisher.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Rules: [Outgoing adapters accessing other modules must only use their published api/ and events/ packages](/rule/strategic/outgoing-adapters-accessing-other-modules-must-only-use-their-published-api-and-events-packages.md) · [Modules must not access each other in the application layer](/rule/strategic/modules-must-not-access-each-other-in-the-application-layer.md) · [Event listeners consuming integration events should use an ACL](/rule/strategic/event-listeners-consuming-integration-events-should-use-anti-corruption-layer.md)
- Guide: [Integration Patterns](/guide/readme/integration-patterns.md) · [Java package structure](/guide/readme/java-package-structure.md)
- Recipes: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) · [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)
- Related decisions: [Event delivery: sync, async, and when you need an outbox](/decision/event-delivery-sync-async-and-outbox.md) · [Domain event vs integration event](/decision/domain-event-vs-integration-event.md)
