---
type: Recipe
title: Expose an Open Host Service
tags: [recipe, strategic, bounded-context, port-in]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/strategic/dca-str-005.md, /rule/hexagonal/dca-hex-007.md, /rule/hexagonal/dca-hex-004.md, /rule/strategic/dca-str-006.md, /rule/strategic/dca-str-003.md, /marker/strategic/openhostservice.md, /marker/port-out/outputport.md, /marker/port-in/usecase.md]
---

Publish the public, stable capabilities of a bounded context so *other* contexts can call in — the provider side of the Open Host Service (OHS) pattern. An OHS is an **incoming adapter**: it sits at your context's edge, delegates to your own use cases, and returns DTOs in a published language. It exists so consuming contexts have one sanctioned door instead of reaching into your domain. This recipe covers building the provider; the fork of *whether* two contexts should talk synchronously (OHS) or via events is decided in [Cross-context communication](/decision/cross-context-communication.md) — build an OHS only when a consumer genuinely needs an answer to proceed.

## Steps

1. **Confirm a synchronous call is right.** Run [Cross-context communication](/decision/cross-context-communication.md). An OHS is the provider half of the *synchronous* option — use it when a consumer needs your data to proceed (a price to total a cart, product identity to render a page). If consumers only need to know a fact happened, publish an integration event instead ([Publish a cross-context event](/recipe/publish-a-cross-context-event.md)).
2. **Place and annotate it.** An OHS is the *relationship* your context publishes, not a transport. In-process it lives in your context's published `api/` package (next to `events/`); over the network it is an incoming adapter — a REST resource in `adapter/incoming/api/`, gRPC, MCP — and the adapter's sub-package is your choice, no rule checks it. Annotate the class `@OpenHostService(context = "...", description = "...")` so it is discoverable and self-describing; add Spring's `@Service` to wire it.
3. **Depend on input ports, delegate to use cases.** Like a REST resource, an OHS injects your **input port interfaces** and calls `execute(...)` — it must never touch a repository or output port directly, and holds no business logic of its own. Generate the class from the [Open Host Service template](/template/open-host-service.md).
4. **Return DTOs in a published language — never domain objects.** Expose small records (e.g. a `ProductInfo` record) built from the use-case `Result`. Aggregates, entities, and internal value objects must not cross the boundary. Publish only what other contexts genuinely need; a narrow, intention-revealing contract is the whole point of an OHS.
5. **Tell consumers how to consume it.** A consuming context must **not** call your OHS from its use cases. It defines its *own* output port in its `application/shared/`, implemented by an outgoing adapter in `adapter/outgoing/{yourcontext}/` that calls your OHS (wrapping it in an anti-corruption layer if the models differ). Only that adapter changes if you later extract the provider into a separate service.
6. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project).

## Rules to satisfy (build-time checklist)

- [Open Host Services must be published: in the api package or as an incoming adapter](/rule/strategic/dca-str-005.md)
- [Incoming adapters must only access their own bounded context (event consumers and Open Host Services excepted)](/rule/hexagonal/dca-hex-007.md)
- [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md)
- [Outgoing adapters accessing other modules must only use their published api/ and events/ packages](/rule/strategic/dca-str-006.md) *(consumer side)*
- [Modules must not access each other in the application layer](/rule/strategic/dca-str-003.md)

## Anchors

- Template: [Open Host Service skeleton](/template/open-host-service.md)
- Marker: [@OpenHostService](/marker/strategic/openhostservice.md) · consumer port: [OutputPort](/marker/port-out/outputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Guide: [Integration Patterns](/guide/integration-patterns.md) · [Java package structure](/guide/package-structure.md)
- Decisions: [Cross-context communication](/decision/cross-context-communication.md)
- Consumer-side recipes: [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md) · [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)
- Sibling incoming adapter: [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
