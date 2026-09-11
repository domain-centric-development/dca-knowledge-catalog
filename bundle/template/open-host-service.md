---
type: Template
title: "Open Host Service skeleton (provider-side cross-context API)"
tags: [template, strategic, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/strategic/openhostservice.md, /rule/strategic/dca-str-005.md, /rule/strategic/dca-str-006.md, /guide/integration-patterns.md, /guide/package-structure.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for an **Open Host Service (OHS)**: the published, provider-side API a bounded context exposes so *other* contexts can consume its capabilities. It is a *relationship*, not a transport: in-process it lives in the context's published `api/` package (next to `events/`), over the network it is an incoming adapter (REST, gRPC, MCP — any sub-package). Either way other contexts "call into" this one, so it depends on **input ports (use cases)**, never on output ports/repositories directly, exactly like a REST controller. It is annotated `@OpenHostService(context, description)` and returns **DTOs (records) only, never domain objects**. Consumers must **not** call it from their use cases — they define their *own* output port in `application/shared/` and an outgoing adapter that delegates to this OHS (see the cross-context decision). Replace `{Context}` / `{context}` / `{basePackage}` and the DTO/use-case types.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`open-host-service/java.md`](/template/open-host-service/java.md)

## Realizes / governed by

- Marker: [@OpenHostService](/marker/strategic/openhostservice.md)
- Rules: [Open Host Services must be published: in the api package or as an incoming adapter](/rule/strategic/dca-str-005.md) · [Outgoing adapters accessing other modules must only use their published api/ and events/ packages](/rule/strategic/dca-str-006.md)
- Guide: [Integration patterns](/guide/integration-patterns.md) · [Java package structure](/guide/package-structure.md)
- Decisions: [Cross-context communication: synchronous call or integration event](/decision/cross-context-communication.md)
- Recipe: [Expose an Open Host Service](/recipe/expose-an-open-host-service.md) · [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)
