---
type: Template
title: "Open Host Service skeleton (provider-side cross-context API)"
tags: [template, strategic, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/openhostservice.md, /rule/strategic/dca-str-005.md, /rule/strategic/dca-str-006.md, /guide/readme/integration-patterns.md, /guide/readme/java-package-structure.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an **Open Host Service (OHS)**: the published, provider-side API a bounded context exposes so *other* contexts can consume its capabilities. It is a *relationship*, not a transport: in-process it lives in the context's published `api/` package (next to `events/`), over the network it is an incoming adapter (REST, gRPC, MCP — any sub-package). Either way other contexts "call into" this one, so it depends on **input ports (use cases)**, never on output ports/repositories directly, exactly like a REST controller. It is annotated `@OpenHostService(context, description)` and returns **DTOs (records) only, never domain objects**. Consumers must **not** call it from their use cases — they define their *own* output port in `application/shared/` and an outgoing adapter that delegates to this OHS (see the cross-context decision). Replace `{Context}` / `{context}` / `{basePackage}` and the DTO/use-case types.

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

## Realizes / governed by

- Marker: [@OpenHostService](/marker/strategic/openhostservice.md)
- Rules: [Open Host Services must be published: in the api package or as an incoming adapter](/rule/strategic/dca-str-005.md) · [Outgoing adapters accessing other modules must only use their published api/ and events/ packages](/rule/strategic/dca-str-006.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Java package structure](/guide/readme/java-package-structure.md)
- Decisions: [Cross-context communication: synchronous call or integration event](/decision/cross-context-communication.md)
- Recipe: [Expose an Open Host Service](/recipe/expose-an-open-host-service.md) · [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)
