---
type: Marker
title: "@IntegrationEventType"
category: tactical
kind: annotation
signature: "public @interface IntegrationEventType"
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
methods: ["String name()", "int version() default 1"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/IntegrationEventType.java
tags: [tactical, marker]
---

The mandatory contract identity every `t` carries: a stable logical type
name plus schema version, decoupled from the Java class name.

Decoupling name and version from the class means a breaking schema change ships as a new V2
class that keeps the old logical `name` in its annotation. A serializer keys `(name, version)` to the class and stamps both onto the wire envelope, so a remote consumer (outbox relay
or message broker) picks its translator from the message alone.

This annotation is the **single source of truth for an event's version** — integration
events carry no `version` data field on the instance.

**Example:**

```java
&#64;IntegrationEventType(name = "cart-checked-out", version = 1)
public record CartCheckedOutEvent(UUID eventId, Instant occurredOn, ...)
    implements IntegrationEvent {}
```
