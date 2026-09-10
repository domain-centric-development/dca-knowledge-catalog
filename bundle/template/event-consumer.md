---
type: Template
title: "Event consumer skeleton (incoming adapter with @ApplicationModuleListener)"
tags: [template, adapter, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/spring-modulith/module-communication.md, /marker/port-in/inputport.md, /marker/tactical/integrationevent.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-007.md, /rule/strategic/dca-str-010.md, /guide/readme/integration-patterns.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an event consumer: a primary (incoming) adapter that reacts to a cross-context event by driving a use case. It lives in `adapter/incoming/event/`, is named `{Name}EventConsumer`, and handles events with Spring Modulith's `@ApplicationModuleListener` — which runs each handler in its own transaction after the publishing transaction commits, giving one-aggregate-per-transaction consistency. It depends only on an **input port**, never on a repository or the domain. Replace `{Name}` / `{usecasename}` / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`event-consumer/java.md`](/template/event-consumer/java.md)

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Rules: [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md) · [Incoming adapters must only access their own bounded context (except event consumers and open host services)](/rule/hexagonal/dca-hex-007.md) · [Event listeners consuming integration events should use an Anti-Corruption Layer](/rule/strategic/dca-str-010.md)
- Guide: [Module communication](/guide/spring-modulith/module-communication.md) · [Integration patterns](/guide/readme/integration-patterns.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
