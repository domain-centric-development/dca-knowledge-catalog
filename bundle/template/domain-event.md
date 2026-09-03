---
type: Template
title: "Domain event skeleton (record implementing DomainEvent)"
tags: [template, domain, domain-event]
---

Domain-free skeleton for a domain event: an immutable fact about something that happened, internal to one bounded context. Model it as a Java `record` implementing `DomainEvent`, named in the **past tense**, with no `Event` suffix and no `version` field (that is reserved for integration events). The aggregate registers it; the use case publishes and clears it after persistence. Replace `{Name}` / `{context}` / `{name}` / `{basePackage}`. The domain layer is framework-free — no Spring annotations.

## `{Name}{PastTense}.java` — the domain event

```java
package {basePackage}.{context}.domain.{name};

import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainEvent;
import java.time.Instant;
import java.util.UUID;

/** Internal fact. Named in the past tense; stays in this context (no version field). */
public record {Name}{PastTense}(
        UUID eventId,
        {Name}Id {name}Id,
        // event-specific data (domain-typed fields)
        Instant occurredOn)
        implements DomainEvent {

    /** Factory stamps the event id and timestamp. */
    public static {Name}{PastTense} now({Name}Id {name}Id /*, data */) {
        return new {Name}{PastTense}(UUID.randomUUID(), {name}Id, Instant.now());
    }
}
```

`DomainEvent` requires exactly `eventId()` and `occurredOn()` — the record
components supply both. Name it for what happened (`{Name}Created`,
`{Name}Renamed`, `{Name}Deactivated`), not as a command.

## Registering it on the aggregate

```java
// inside the aggregate root (extends BaseAggregateRoot<{Name}, {Name}Id>)
public void change(/* args */) {
    // enforce invariants, mutate state
    registerEvent({Name}{PastTense}.now(this.id /*, data */));
}
```

`registerEvent(...)` (from `BaseAggregateRoot`) queues the event. The use case
then persists the aggregate and, only after a successful save, publishes and
clears its events — see [Event publishing rules](/guide/readme/rules.md). To
carry this fact to another context, an outgoing adapter translates it into an
integration event (see the integration-event template).

## Realizes / governed by

- Markers: [DomainEvent](/marker/tactical/domainevent.md) · [BaseAggregateRoot<T, ID>](/marker/tactical/baseaggregateroot.md)
- Rules: [Domain Events must implement DomainEvent Marker Interface and be records](/rule/advanced/domain-events-must-implement-domainevent-marker-interface-and-be-records.md) · [Domain Events must have a timestamp field](/rule/advanced/domain-events-must-have-a-timestamp-field.md) · [Domain Events must not have Spring annotations](/rule/advanced/domain-events-must-not-have-spring-annotations.md) · [Domain Events must reside in domain package](/rule/advanced/domain-events-must-reside-in-domain-package.md) · [Domain Events that are not Integration Events must not have a version field](/rule/advanced/domain-events-that-are-not-integration-events-must-not-have-a-version-field.md)
- Guide: [Layer rules](/guide/readme/rules.md) · [Integration patterns](/guide/readme/integration-patterns.md)
- Decision: [Domain event vs. integration event](/decision/domain-event-vs-integration-event.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
