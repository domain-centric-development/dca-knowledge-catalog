---
type: Pitfall
title: "God port: one fat input port for many use cases"
tags: [pitfall, hexagonal, use-case, port]
---

A single wide input-port interface — `OrderService` with `placeOrder`, `cancelOrder`, `addItem`, `applyDiscount`, `reorder`, … — that every controller depends on. The interface grows with every feature, and every consumer is coupled to methods it never calls. This is the Interface Segregation Principle violated at the application boundary.

## Why it is wrong

- Consumers depend on the whole surface. A controller that only cancels orders still compiles against `placeOrder`, `applyDiscount`, and everything else — recompiled and re-reasoned about whenever any unrelated method changes.
- Use cases lose their boundaries. The input port is meant to be *one entry point for one use case*; a god port collapses many independent operations into one blob, so transaction scope, authorization, and input/output models blur together.
- It maps poorly onto the marker contract. [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md) models a single `execute(input)` — one command/query in, one result out. A fat interface with a dozen unrelated methods can't honour that shape.
- Testing and mocking bloat: every test double must stub the entire interface.

## What forbids it

No ArchUnit rule counts methods, so a god port is a **design smell the naming rules make visible** rather than a mechanically blocked construct. It is forbidden by the intent of:

- [InputPort interfaces must end with 'InputPort'](/rule/naming/inputport-interfaces-must-end-with-inputport.md) — each use case gets its *own* named `*InputPort`, not a shared service interface.
- [Application layer InputPort implementations must end with 'UseCase'](/rule/naming/application-layer-inputport-implementations-must-end-with-usecase.md) — one `*UseCase` implements one `*InputPort`, reinforcing one-operation-per-port.

## Do instead

One input port per use case, each extending `UseCase<Command|Query, Result>` with a single `execute`. A controller depends only on the ports for the operations it actually triggers.

`PlaceOrderInputPort`, `CancelOrderInputPort`, `AddItemInputPort` — each with its own `*UseCase` implementation, command/query, and result.

- [Recipe: add a use case](/recipe/add-a-use-case.md) · [Template: use case](/template/use-case.md)

## Anchors

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Guide: [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md) · [Layer rules](/guide/readme/rules.md) · [Layer elements](/guide/readme/elements.md)
