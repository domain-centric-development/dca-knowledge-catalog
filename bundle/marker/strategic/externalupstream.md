---
type: Marker
title: "@ExternalUpstream"
category: strategic
kind: annotation
signature: "public @interface ExternalUpstream"
package: dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships
methods: ["String name()", "Upstream.Translation translation()", "Interaction interaction()", "String[] contractPackages() default {}", "String protocol() default \"\"", "String exchanges() default \"\"", "String rationale() default \"\"", "Upstream.Status status() default Upstream.Status.IMPLEMENTED"]
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/strategic/relationships/ExternalUpstream.java
tags: [strategic, marker]
---

Declares that this bounded context consumes an *external system* — one that lives outside
this codebase — as its upstream.

Like `m`, this is declared on the downstream side, because an external system has
no side in this codebase that could declare anything. The model dependency always points to the
external system, regardless of who initiates the exchange: a webhook the external system calls is
still *its* contract that this context conforms to or translates.

`interaction()` names who initiates — which is also where the edge sits and where an
Anti-Corruption Layer must live. Protocol details (webhook, queue, SFTP batch, polling cadence)
belong in `rationale()`; polling an external API is `OUTBOUND`, no matter how
event-like its semantics.

**Usage:**

```java
@ExternalUpstream(
    name = "Payment Service Provider",
    translation = Upstream.Translation.ANTI_CORRUPTION_LAYER,
    interaction = ExternalUpstream.Interaction.OUTBOUND,
    rationale = "Synchronous payment operations behind the caller-owned PaymentProvider port")
package com.acme.shop.checkout;
```

**Architectural rules** (enforced by `ContextMapArchUnitTest`):

- Only packages annotated with `t` may
declare `@ExternalUpstream`
- `name` must not be blank and must not collide with an internal context's name
- `(name, interaction)` must be unique per declaring context
- `ANTI_CORRUPTION_LAYER`: types from `contractPackages()` appear only in the
adapter matching the interaction (outgoing for `OUTBOUND`, incoming for `INBOUND`)
- `CONFORMIST`: types from `contractPackages()` never reach the domain layer

Without `contractPackages()` (plain HTTP, no vendor SDK) the translation rules have
nothing to check — the declaration then documents the relationship and feeds the generated
context map.
