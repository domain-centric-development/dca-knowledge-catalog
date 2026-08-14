---
type: Recipe
title: "Add an anti-corruption layer"
tags: [recipe, strategic, anti-corruption-layer]
---

Protect your domain from a foreign model — another bounded context or an external system. An anti-corruption layer (ACL) is a translation boundary: your context speaks its own ubiquitous language, and the ACL adapter converts to and from the foreign contract so the foreign model never leaks inward.

## Step 0 — decide (do this first)

An ACL is the answer when the foreign model differs from yours and you must not conform to it. If the two contexts could instead share a small, jointly-owned model, weigh that trade-off — see [Shared kernel vs. duplication](/decision/shared-kernel-vs-duplication.md). Prefer an ACL over a shared kernel when the contexts evolve independently.

## Steps

1. **Consume through the provider's contract** — for a peer context, go through its Open Host Service (`@OpenHostService`), never its internals. For an external system, treat its API/wire format as the foreign contract.
2. **Define an output port** in your `application/shared/` in *your* terms (a `DomainGateway`-style interface); your use cases depend on this, not on the foreign types.
3. **Implement the ACL in an outgoing adapter** in an `acl` package under `adapter/outgoing/` — it calls the foreign contract and maps the foreign model to your domain types (and your requests to theirs). All translation lives here.
4. **For event-driven integration**, consume the other context's integration event in `adapter/incoming/messaging/`, translate it through the ACL, then invoke your own use case ([Publish a cross-context event](/recipe/publish-a-cross-context-event.md)).
5. **Keep the boundary one-directional** — foreign types stay inside the ACL; nothing foreign appears in your domain or application layer.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Anti-corruption layer components must be in acl packages](/rule/strategic/anti-corruption-layer-components-must-be-in-acl-packages.md)
- [Outgoing adapters accessing other contexts must only use OpenHostService classes (except allowed ACL patterns)](/rule/strategic/outgoing-adapters-accessing-other-contexts-must-only-use-openhostservice-classes-except-allowed-acl-patterns.md)
- [Event listeners consuming integration events should use an anti-corruption layer](/rule/strategic/event-listeners-consuming-integration-events-should-use-anti-corruption-layer.md)
- [Outgoing adapters may access Open Host Services from other contexts](/rule/hexagonal/outgoing-adapters-may-access-open-host-services-from-other-contexts.md)
- [Outgoing adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/outgoing-adapters-must-only-use-outbound-ports-not-infrastructure-implementations.md)

## Anchors

- Decision: [Shared kernel vs. duplication](/decision/shared-kernel-vs-duplication.md)
- Markers: [DomainGateway](/marker/tactical/domaingateway.md) · [@OpenHostService](/marker/strategic/openhostservice.md)
- Guide: [Integration patterns](/guide/readme/integration-patterns.md) · [Java package structure](/guide/readme/java-package-structure.md) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- To emit events across the boundary from the other side: [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
