---
type: Pitfall
title: "Raw cross-context import"
tags: [pitfall, strategic, bounded-context]
---

One bounded context reaching directly into another's internals — `import com.shop.ordering.domain.Order;` from inside the Shipping context, or a Shipping use case calling `OrderRepository` from Ordering. It compiles, it's the shortest path, and it silently fuses two contexts that were supposed to evolve independently.

## Why it is wrong

- It destroys context autonomy. The whole reason for bounded contexts is that each owns its model and can change it without breaking others. A raw import means Ordering can't rename or restructure `Order` without breaking Shipping.
- It leaks a foreign ubiquitous language. An `Order` means something specific *in Ordering*; imported into Shipping it drags in rules, states, and assumptions that don't belong there.
- It creates hidden coupling and cycles. Direct type dependencies across contexts are exactly what the cyclic-dependency and isolation rules exist to prevent.
- There is no translation boundary, so a change in one model ripples uncontrolled into the other.

## What forbids it

- [Bounded contexts must not directly access each other in application layer (except allowed dependencies)](/rule/strategic/bounded-contexts-must-not-directly-access-each-other-in-application-layer-except-allowed-dependencies.md) — mechanically blocks the application-layer cross-context call.
- [Incoming adapters must only access their own bounded context (except event consumers and Open Host Services)](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md) — you can't launder the coupling through the shared kernel either.

## Do instead

Integrate across the boundary through an explicit contract, not a shared object graph:

- **Asynchronously** — the source context publishes a versioned [IntegrationEvent](/marker/tactical/integrationevent.md); the consuming context translates it in an Anti-Corruption Layer into its own model. See [Recipe: publish a cross-context event](/recipe/publish-a-cross-context-event.md).
- **Synchronously** — call the other context's Open Host Service, and translate the response through an [Anti-Corruption Layer](/recipe/add-an-anti-corruption-layer.md) so no foreign type enters your model.

Either way the foreign model stops at the boundary; only a translated, owned representation crosses.

## Anchors

- ADRs: [ADR-011 Bounded Context Isolation via Package Structure](/adr/adr-011-bounded-context-isolation.md) · [ADR-019 Open Host Service Pattern](/adr/adr-019-open-host-service-pattern.md)
- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [IntegrationEvent](/marker/tactical/integrationevent.md) · [@OpenHostService](/marker/strategic/openhostservice.md)
- Book: [Cross-Context Communication](/book/10-bounded-contexts/cross-context-communication.md) · [Bounded Contexts — Common Mistakes](/book/10-bounded-contexts/common-mistakes.md)
- Related decision: [Shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md)
