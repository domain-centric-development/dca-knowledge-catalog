---
type: Pitfall
title: Raw cross-context import
tags: [pitfall, strategic, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/strategic/dca-str-003.md, /rule/hexagonal/dca-hex-007.md, /rule/strategic/dca-str-002.md, /marker/tactical/integrationevent.md, /guide/package-structure.md, /guide/integration-patterns.md, /marker/strategic/boundedcontext.md, /marker/strategic/openhostservice.md]
---

One bounded context reaching directly into another's internals — `import com.shop.ordering.domain.Order;` from inside the Shipping context, or a Shipping use case calling `OrderRepository` from Ordering. It compiles, it's the shortest path, and it silently fuses two contexts that were supposed to evolve independently.

## Why it is wrong

- It destroys context autonomy. The whole reason for bounded contexts is that each owns its model and can change it without breaking others. A raw import means Ordering can't rename or restructure `Order` without breaking Shipping.
- It leaks a foreign ubiquitous language. An `Order` means something specific *in Ordering*; imported into Shipping it drags in rules, states, and assumptions that don't belong there.
- It creates hidden coupling and cycles. Direct type dependencies across contexts are exactly what the cyclic-dependency and isolation rules exist to prevent.
- There is no translation boundary, so a change in one model ripples uncontrolled into the other.

## What forbids it

- [Modules must not access each other in the application layer](/rule/strategic/dca-str-003.md) — mechanically blocks the application-layer cross-context call.
- [Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)](/rule/hexagonal/dca-hex-007.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/dca-str-002.md) — you can't launder the coupling through the shared kernel either.

## Do instead

Integrate across the boundary through an explicit contract, not a shared object graph:

- **Asynchronously** — the source context publishes a versioned [IntegrationEvent](/marker/tactical/integrationevent.md); the consuming context translates it in an Anti-Corruption Layer into its own model. See [Recipe: publish a cross-context event](/recipe/publish-a-cross-context-event.md).
- **Synchronously** — call the other context's Open Host Service, and translate the response through an [Anti-Corruption Layer](/recipe/add-an-anti-corruption-layer.md) so no foreign type enters your model.

Either way the foreign model stops at the boundary; only a translated, owned representation crosses.

## Anchors

- Guide: [Java package structure](/guide/package-structure.md) · [Integration patterns](/guide/integration-patterns.md)
- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [IntegrationEvent](/marker/tactical/integrationevent.md) · [@OpenHostService](/marker/strategic/openhostservice.md)
- Related pitfall: [Cyclic module dependency](/pitfall/cyclic-module-dependency.md) — the structural failure when this raw import goes both ways between two contexts
- Related decision: [Shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md)
