---
type: Template
title: "Event consumer skeleton (incoming adapter, transactional listener)"
tags: [template, adapter, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /guide/spring-modulith/module-communication.md, /marker/port-in/inputport.md, /marker/tactical/integrationevent.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-007.md, /rule/strategic/dca-str-010.md, /guide/integration-patterns.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an event consumer: an incoming adapter that reacts to an event by driving a use case. The event is a contract from another context or a domain event of this context — the shape is the same. It lives in `adapter/incoming/event/`, is named `{Name}EventConsumer`, and is a **transactional listener**: delivered after the publishing transaction commits, in a transaction of its own, from a publication the store captured in the publishing transaction. On Spring with the event publication registry that is `@ApplicationModuleListener`; elsewhere it is the project's own transactional listener kind over its outbox. It depends only on an **input port**, never on a repository, an outgoing adapter or the domain. Replace `{Name}` / `{usecasename}` / `{context}` / `{basePackage}`.

The consumer holds no decision. It maps the event to a command and calls the input port. A failure it does not catch leaves the publication due, so the outbox retries it up to its limit and then keeps it as failed for inspection. Idempotency per event id is the use case's job, because delivery is at least once.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`event-consumer/java.md`](/template/event-consumer/java.md)

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Rules: [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md) · [Incoming adapters must only access their own bounded context (except event consumers and open host services)](/rule/hexagonal/dca-hex-007.md) · [Event listeners consuming integration events should use an Anti-Corruption Layer](/rule/strategic/dca-str-010.md)
- Guide: [Module communication](/guide/spring-modulith/module-communication.md) · [Integration patterns](/guide/integration-patterns.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
- Decision: [Reacting to an event: one path, two listener kinds](/decision/reacting-to-an-event.md)
