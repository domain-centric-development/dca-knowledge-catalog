---
type: Template
title: "Event consumer skeleton (incoming adapter, transactional listener) — Java"
parent: /template/event-consumer.md
tags: [template, adapter, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/integration-patterns/reacting-to-an-event.md, /guide/spring-modulith/module-communication.md, /marker/port-in/inputport.md, /marker/tactical/integrationevent.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-007.md, /rule/strategic/dca-str-010.md, /guide/integration-patterns.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Event consumer skeleton (incoming adapter, transactional listener)](/template/event-consumer.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}EventConsumer.java` — the consumer

```java
package {basePackage}.{context}.adapter.incoming.event;

import {basePackage}.{context}.application.{usecasename}.{Name}Command;
import {basePackage}.{context}.application.{usecasename}.{Name}InputPort;
import org.springframework.modulith.events.ApplicationModuleListener;
import org.springframework.stereotype.Component;

/** Incoming event adapter: reacts to an event — own or foreign — by driving the {Name} use case. */
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
lives behind the input port. The same skeleton consumes this context's own domain
event (`{Trigger}` is then the domain event type) — the registry captures it like any
other publication. Without Spring Modulith, `@TransactionalEventListener` alone is
not this kind: it runs after the commit but nothing records that it is due; use the
project's outbox and its worker instead.
