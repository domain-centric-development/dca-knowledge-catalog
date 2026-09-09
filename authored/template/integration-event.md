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

## `{Name}{PastTense}Event.java` — the integration event

```java
package {basePackage}.{context}.events;

import dev.domaincentric.dca.buildingblocks.ddd.tactical.IntegrationEvent;
import dev.domaincentric.dca.buildingblocks.ddd.tactical.IntegrationEventType;
import java.time.Instant;
import java.util.UUID;

/** Cross-context published-language DTO. "Event" suffix; version lives in the annotation. */
@IntegrationEventType(name = "{name}-{pasttense}", version = 1)
public record {Name}{PastTense}Event(
        UUID eventId,
        {Name}Id {name}Id,
        // stable, consumer-facing fields (primitives or shared-kernel value objects)
        Instant occurredOn)
        implements IntegrationEvent {

    /** Built from the internal domain event by the outgoing adapter. */
    public static {Name}{PastTense}Event now({Name}Id {name}Id /*, data */) {
        return new {Name}{PastTense}Event(UUID.randomUUID(), {name}Id, Instant.now());
    }
}
```

`IntegrationEvent` requires `eventId()` and `occurredOn()`. The contract identity —
stable logical `name` + schema `version` — is declared in `@IntegrationEventType`
([Integration patterns](/guide/readme/integration-patterns.md)): bump `version` on a
breaking change; ship it as a new class keeping the old `name`.

## `{Name}{PastTense}EventPublisher.java` — outgoing adapter

```java
package {basePackage}.{context}.adapter.outgoing.event;

import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

/** Listens for the internal domain event and publishes the cross-context integration event. */
@Component
public class {Name}{PastTense}EventPublisher {

    private final ApplicationEventPublisher publisher;

    public {Name}{PastTense}EventPublisher(final ApplicationEventPublisher publisher) {
        this.publisher = publisher;
    }

    @EventListener
    public void on(final {Name}{PastTense} domainEvent) {
        publisher.publishEvent({Name}{PastTense}Event.now(domainEvent.{name}Id() /*, data */));
    }
}
```

The publisher lives in the adapter layer (`adapter/outgoing/event/`) and does the
domain→integration translation; the integration event record itself is the
context's published language in `{context}.events`. A consumer in another context
receives it — see the event-consumer template. For at-least-once delivery across
a transaction boundary, see [Integration patterns](/guide/readme/integration-patterns.md).

## Realizes / governed by

- Markers: [IntegrationEvent](/marker/tactical/integrationevent.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Rules: [Integration Events must be annotated with IntegrationEventType](/rule/advanced/dca-adv-005.md) · [Integration Events must not have a version field](/rule/advanced/dca-adv-006.md) · [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/dca-str-007.md) · [Integration Events should be immutable records](/rule/strategic/dca-str-008.md) · [Domain Events that are not Integration Events must not have a version field](/rule/advanced/dca-adv-007.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Module communication](/guide/spring-modulith/module-communication.md)
- Decision: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Recipe: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) · [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
