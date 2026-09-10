---
type: Template
title: "Event consumer skeleton (incoming adapter with @ApplicationModuleListener) — Java"
parent: /template/event-consumer.md
tags: [template, adapter, events]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/spring-modulith/module-communication.md, /marker/port-in/inputport.md, /marker/tactical/integrationevent.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-007.md, /rule/strategic/dca-str-010.md, /guide/readme/integration-patterns.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Event consumer skeleton (incoming adapter with @ApplicationModuleListener)](/template/event-consumer.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

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
