---
type: Pitfall
title: "Cyclic module dependency"
tags: [pitfall, strategic, bounded-context, modulith]
---

Two bounded contexts that reference each other: Ordering depends on Shipping *and* Shipping depends on Ordering. Each direction may look reasonable in isolation — Ordering asks Shipping for a rate, Shipping reads the order to know what to ship — but together they close a loop. The modules can no longer be built, deployed, reasoned about, or tested independently, and `ApplicationModules.of(...).verify()` fails the build with a cycle between the two modules.

Where [raw cross-context import](/pitfall/raw-cross-context-import.md) is the *single-direction* smell — one context reaching into another's internals with no translation boundary — this pitfall is the **structural consequence when that reaching goes both ways**: a mutual dependency that Spring Modulith rejects outright. A raw import in one direction is already wrong; two of them facing each other is unbuildable.

## Why it is wrong

- It collapses the two contexts into one. The point of bounded contexts is independent evolution; a cycle means neither can change its model, release, or be understood without the other.
- Spring Modulith's `verify()` treats a cycle between modules as a hard failure — the architecture test goes red, so the problem surfaces at build time rather than silently rotting.
- Cycles defeat the Acyclic Dependencies Principle that the package-cycle rules enforce *within* a context; the same principle must hold *between* contexts.
- Event listeners are a common trap: module A listens to B's events and B listens to A's, quietly forming a runtime cycle even when no type is imported.

## What forbids it

- [Bounded contexts must not directly access each other in application layer (except allowed dependencies)](/rule/strategic/modules-must-not-access-each-other-in-the-application-layer.md) — the mechanical guard; a mutual dependency can't satisfy the `allowedDependencies` allow-list in both directions.
- The package-cycle rules apply the same acyclic principle inside each layer: [Domain Packages](/rule/cycles/domain-packages-must-not-have-cyclic-dependencies.md) · [Application Layer](/rule/cycles/application-layer-must-not-have-cyclic-dependencies.md) · [Incoming Adapter Packages](/rule/cycles/incoming-adapter-packages-must-not-have-cyclic-dependencies.md) · [Outgoing Adapter Packages](/rule/cycles/outgoing-adapter-packages-must-not-have-cyclic-dependencies.md).

## Do instead

Break the loop so the dependency flows one way, or not at all:

- **Invert with events.** Instead of both contexts calling each other, one publishes a versioned [IntegrationEvent](/marker/tactical/integrationevent.md) and the other consumes and translates it — decoupling the direct reference. When the cycle is specifically between event listeners, apply the Interface Inversion pattern ([Module communication](/guide/spring-modulith/module-communication.md)) to move the contract to a neutral abstraction.
- **Pick a direction and use an Open Host Service.** Let one context be the upstream that others call via its [@OpenHostService](/marker/strategic/openhostservice.md); the downstream translates the response through an Anti-Corruption Layer. Only one arrow, no loop.
- **Extract a shared upstream.** If both genuinely need the same concept, the shared part may belong in a third context (or the Shared Kernel) that both depend on — never on each other. See [shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md).

See [Recipe: publish a cross-context event](/recipe/publish-a-cross-context-event.md) for the asynchronous route.

## Anchors

- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Module communication](/guide/spring-modulith/module-communication.md)
- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [IntegrationEvent](/marker/tactical/integrationevent.md) · [@OpenHostService](/marker/strategic/openhostservice.md)
- Related pitfall: [Raw cross-context import](/pitfall/raw-cross-context-import.md) — the single-direction import this cycle is built from
- Related decision: [Shared kernel vs duplication](/decision/shared-kernel-vs-duplication.md)
