---
type: Template
title: "Domain event skeleton (record implementing DomainEvent) — Java"
parent: /template/domain-event.md
tags: [template, domain, domain-event]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /marker/tactical/domainevent.md, /marker/tactical/baseaggregateroot.md, /rule/advanced/dca-adv-001.md, /rule/advanced/dca-adv-008.md, /rule/advanced/dca-adv-004.md, /rule/advanced/dca-adv-002.md, /rule/advanced/dca-adv-007.md]
applies_to: [java]
framework: [framework-neutral]
---

The Java code of [Domain event skeleton (record implementing DomainEvent)](/template/domain-event.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
clears its events — see [Event publishing rules](/guide/rules.md). To
carry this fact to another context, an outgoing adapter translates it into an
integration event (see the integration-event template).
