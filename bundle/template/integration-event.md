---
type: Template
title: "Integration event skeleton (record implementing IntegrationEvent + outgoing publisher)"
tags: [template, adapter, integration-event]
---

Domain-free skeleton for an integration event: the versioned, published-language representation of a fact that crosses a bounded-context boundary. It is **not** a domain event — it carries an `Event` suffix, has a `version` field for backward compatibility, and lives in the publishing context's `events/` package (its published language), created by an outgoing event adapter from an internal domain event. This separation is an Anti-Corruption Layer between your domain model and external consumers. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`.

## `{Name}{PastTense}Event.java` — the integration event

```java
package {basePackage}.{context}.events;

import {basePackage}.sharedkernel.marker.tactical.IntegrationEvent;
import java.time.Instant;
import java.util.UUID;

/** Cross-context published-language DTO. "Event" suffix + version for compatibility. */
public record {Name}{PastTense}Event(
        UUID eventId,
        {Name}Id {name}Id,
        // stable, consumer-facing fields (primitives or shared-kernel value objects)
        Instant occurredOn,
        int version)
        implements IntegrationEvent {

    /** Built from the internal domain event by the outgoing adapter. */
    public static {Name}{PastTense}Event now({Name}Id {name}Id /*, data */) {
        return new {Name}{PastTense}Event(UUID.randomUUID(), {name}Id, Instant.now(), 1);
    }
}
```

`IntegrationEvent` requires `eventId()`, `occurredOn()`, and `version()`. Bump
`version` when the schema changes so downstream consumers stay compatible.

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
a transaction boundary, see [ADR-026](/adr/adr-026-transactional-outbox-integration-events.md).

## Realizes / governed by

- Markers: [IntegrationEvent](/marker/tactical/integrationevent.md) · [DomainEvent](/marker/tactical/domainevent.md)
- Rules: [Integration Events must have a version field](/rule/advanced/integration-events-must-have-a-version-field.md) · [Integration Events must be in events or adapter outgoing event packages](/rule/strategic/integration-events-must-be-in-events-or-adapter-outgoing-event-packages.md) · [Integration Events should be immutable records](/rule/strategic/integration-events-should-be-immutable-records.md) · [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)
- ADRs: [ADR-026 Transactional Outbox for Integration Events](/adr/adr-026-transactional-outbox-integration-events.md) · [ADR-024 Interface Inversion for Spring Modulith Listeners](/adr/adr-024-interface-inversion-spring-modulith.md)
- Book: [Events & Integration — Integration Events](/book/14-events-integration/integration-events.md) · [Domain Events vs. Integration Events](/book/14-events-integration/domain-events-vs-integration-events.md)
- Decision: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Recipe: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md) · [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
