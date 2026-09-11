---
type: Template
title: "Open Host Service skeleton (provider-side cross-context API) — Java"
parent: /template/open-host-service.md
tags: [template, strategic, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/openhostservice.md, /rule/strategic/dca-str-005.md, /rule/strategic/dca-str-006.md, /guide/integration-patterns.md, /guide/package-structure.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Open Host Service skeleton (provider-side cross-context API)](/template/open-host-service.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Context}Service.java` — Open Host Service (in-process, published `api/` package)

```java
package {basePackage}.{context}.api;

import {basePackage}.{context}.application.get{thing}byid.Get{Thing}ByIdInputPort;
import {basePackage}.{context}.application.get{thing}byid.Get{Thing}ByIdQuery;
import dev.domaincentric.dca.buildingblocks.ddd.strategic.relationships.OpenHostService;
import java.util.Optional;
import org.springframework.stereotype.Service;

/**
 * Open Host Service for the {Context} context.
 *
 * <p>Incoming adapter that exposes {Context} capabilities to other bounded
 * contexts. Delegates to input ports (use cases) and returns DTOs — never domain
 * objects. Consuming contexts define their own output ports rather than calling
 * this directly.
 */
@OpenHostService(
    context = "{Context}",
    description = "Provides {what this context publishes} for other bounded contexts.")
@Service
public class {Context}Service {

    private final Get{Thing}ByIdInputPort get{Thing}ByIdInputPort;

    public {Context}Service(final Get{Thing}ByIdInputPort get{Thing}ByIdInputPort) {
        this.get{Thing}ByIdInputPort = get{Thing}ByIdInputPort;
    }

    /** DTO for cross-context communication — carries only data this context owns. */
    public record {Thing}Info({Thing}Id id, String name) {}

    public Optional<{Thing}Info> get{Thing}Info(final {Thing}Id id) {
        final var result = get{Thing}ByIdInputPort.execute(new Get{Thing}ByIdQuery(id.value()));
        return result.found()
            ? Optional.of(new {Thing}Info(id, result.name()))
            : Optional.empty();
    }
}
```

`@Service` makes it a wired bean; `@OpenHostService` documents the published
contract and its owning context. The service calls **input ports** (it is on the
incoming edge), maps results into its own DTO records, and never returns or leaks
a domain object across the boundary. Anything the context does not own (a price
owned by Pricing, stock owned by Inventory) belongs to that context's OHS, not
this one.

## Consumer side (in the *other* context)

The consumer does **not** import this class into its use cases. It declares an
output port in its own `application/shared/`, and an outgoing adapter in
`adapter/outgoing/{context}/` implements that port by delegating to this OHS —
the single, explicit point of coupling. Only the adapter changes if the provider
later moves to a separate service. Build that side with the [cross-context
decision](/decision/cross-context-communication.md) and, when the foreign model
differs from yours, an [anti-corruption layer](/recipe/add-an-anti-corruption-layer.md).
