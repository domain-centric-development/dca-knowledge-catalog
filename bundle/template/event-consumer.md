---
type: Template
title: "Event consumer skeleton (incoming adapter with @ApplicationModuleListener)"
tags: [template, adapter, events]
---

Domain-free skeleton for an event consumer: a primary (incoming) adapter that reacts to a cross-context event by driving a use case. It lives in `adapter/incoming/event/`, is named `{Name}EventConsumer`, and handles events with Spring Modulith's `@ApplicationModuleListener` — which runs each handler in its own transaction after the publishing transaction commits, giving one-aggregate-per-transaction consistency. It depends only on an **input port**, never on a repository or the domain. Replace `{Name}` / `{usecasename}` / `{context}` / `{basePackage}`.

## `{Name}EventConsumer.java` — the consumer

```java
package {basePackage}.{context}.adapter.incoming.event;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import org.springframework.modulith.events.ApplicationModuleListener;
import org.springframework.stereotype.Component;

/** Incoming event adapter: reacts to a cross-context event by driving the {Name} use case. */
@Component
public class {Name}EventConsumer {

    private final {Name}InputPort {usecasename}InputPort;

    public {Name}EventConsumer(final {Name}InputPort {usecasename}InputPort) {
        this.{usecasename}InputPort = {usecasename}InputPort;
    }

    /**
     * Handles the incoming event in its own transaction (fired after the publisher commits).
     * Translates the event into a command and delegates to the input port — no logic here.
     */
    @ApplicationModuleListener
    void on(final {Trigger} event) {
        {usecasename}InputPort.execute(new {Name}Command(/* event.field(), ... */));
    }
}
```

`@ApplicationModuleListener` is `@Transactional` + `@Async` + transaction-bound, so
the handler observes only committed state and its own failure never rolls back the
producer. To avoid a package dependency on the producing context, prefer the
Interface Inversion pattern: define the trigger interface (`{Trigger}`) in *this*
context's `events/` package and let the producing context's integration event
implement it — see [Module communication](/guide/spring-modulith/module-communication.md).
Keep the consumer thin: map the event to a command and delegate; all behaviour
lives behind the input port.

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [IntegrationEvent](/marker/tactical/integrationevent.md)
- Rules: [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/incoming-adapters-must-only-use-outbound-ports-not-infrastructure-implementations.md) · [Incoming adapters must only access their own bounded context (except event consumers and open host services)](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md) · [Event listeners consuming integration events should use an Anti-Corruption Layer](/rule/strategic/event-listeners-consuming-integration-events-should-use-anti-corruption-layer.md)
- Guide: [Module communication](/guide/spring-modulith/module-communication.md) · [Integration patterns](/guide/readme/integration-patterns.md)
- Recipe: [Add a domain event and consumer](/recipe/add-a-domain-event-and-consumer.md)
