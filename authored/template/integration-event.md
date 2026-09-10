---
type: Template
title: "Integration event skeleton (record implementing IntegrationEvent + outgoing publisher)"
tags: [template, adapter, integration-event]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/integration-patterns.md, /marker/tactical/integrationevent.md, /marker/tactical/domainevent.md, /rule/advanced/dca-adv-005.md, /rule/advanced/dca-adv-006.md, /rule/strategic/dca-str-007.md, /rule/strategic/dca-str-008.md, /rule/advanced/dca-adv-007.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an integration event: the versioned, published-language representation of a fact that crosses a bounded-context boundary. It is **not** a domain event — it carries an `Event` suffix, declares its schema version via `@IntegrationEventType` (a class property, never a data field), and lives in the publishing context's `events/` package (its published language), created by an outgoing event adapter from an internal domain event. This separation is an Anti-Corruption Layer between your domain model and external consumers. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`integration-event/java.md`](/template/integration-event/java.md)

## Realizes / governed by

- Markers: [IntegrationEvent](/marker/tactical/integrationevent.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Rules: [Integration Events must be annotated with IntegrationEventType](/rule/advanced/dca-adv-005.md) · [Integration Events must not have a version field](/rule/advanced/dca-adv-006.md) · [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/dca-str-007.md) · [Integration Events should be immutable records](/rule/strategic/dca-str-008.md) · [Domain Events that are not Integration Events must not have a version field](/rule/advanced/dca-adv-007.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Module communication](/guide/spring-modulith/module-communication.md)
- Decision: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Recipe: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) · [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
