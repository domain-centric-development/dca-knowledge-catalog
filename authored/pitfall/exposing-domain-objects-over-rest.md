---
type: Pitfall
title: Exposing domain objects over REST
tags: [pitfall, adapter, rest, dto, domain, hexagonal]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-008.md, /rule/naming/dca-nam-007.md, /rule/usecase/dca-use-011.md, /marker/tactical/aggregateroot.md, /marker/tactical/entity.md, /guide/architecture-reference-guide/ports-and-adapters.md]
---

A REST controller that returns an aggregate or entity directly — `return orderRepository.findById(id)` serialized straight to JSON — or accepts one as a `@RequestBody`. The domain model becomes the wire contract. The tempting shortcut is that the `Order` already has all the fields the client wants, so why map it?

## Why it is wrong

- The internal model becomes a public API. Every field of the aggregate is now a published contract; renaming a domain field, hiding an invariant, or splitting an entity silently breaks external consumers.
- It leaks structure that shouldn't cross the edge — internal IDs, references, lazy relations, and fields the domain guards but the client should never set.
- Serialization pulls a domain type into the transport concern, coupling the aggregate to Jackson annotations, getter shapes, and framework quirks — the very framework leak the layering forbids.
- Deserializing a request body into an aggregate bypasses its constructor/factory guards, letting a client build an invalid domain object directly.

## What forbids it

- [HTTP response models must end with 'Response' and reside in adapter incoming package](/rule/usecase/dca-use-008.md) — the outbound wire type is a distinct `*Response` at the edge, not the domain object.
- [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md) — the request/response shapes are adapter concerns; the domain never holds them, and the reverse — the domain object never reaches the wire.
- [DTOs must not be used in the application layer](/rule/usecase/dca-use-011.md) — the use case speaks `Command`/`Query`/`Result`; the adapter maps `Result` → `Response`, so a domain type never has a legitimate path to the controller's return value.

## Do instead

Map at the edge. The use case returns a `Result` (application type, no domain objects); the controller converts it to a `*Response` record it owns and serializes that.

`GetOrderInputPort.execute(query)` → `OrderResult` → (controller mapper) → `OrderResponse` (JSON). Inbound: `OrderRequest` → `PlaceOrderCommand`, never straight into the aggregate.

- [Recipe: add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md) · [Template: REST resource](/template/rest-resource.md)

## Anchors

- Rules: [HTTP response models must end with 'Response'](/rule/usecase/dca-use-008.md) · [DTOs must reside in the adapter layer](/rule/naming/dca-nam-007.md) · [DTOs must not be used in the application layer](/rule/usecase/dca-use-011.md)
- Markers: [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Entity&lt;T, ID&gt;](/marker/tactical/entity.md)
- Guide: [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- Sibling pitfall: [DTO in the application layer](/pitfall/dto-in-application-layer.md)
