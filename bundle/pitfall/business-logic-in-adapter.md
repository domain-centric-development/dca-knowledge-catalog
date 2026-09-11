---
type: Pitfall
title: Business logic in an adapter
tags: [pitfall, hexagonal, layered, adapter, application, domain]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-001.md, /rule/layered/dca-lay-004.md, /rule/layered/dca-lay-002.md, /marker/port-in/inputport.md, /marker/port-in/usecase.md, /guide/quick-reference/port-placement.md]
---

A controller (or a repository implementation) that does more than translate and delegate — it validates a business rule, computes a price, decides a state transition, or orchestrates several steps. The classic shape: `OrderResource.placeOrder(...)` reads the request, checks stock, applies a discount, sets the order status, and only then calls a repository. The rule lives in the adapter; the use case and aggregate are hollow.

## Why it is wrong

- The adapter is the wrong layer for policy. Its job is translation at the edge (HTTP/JSON/JDBC ⇄ application types) and delegation to an input port. Business decisions there are invisible to the domain and untestable without the framework.
- Rules leak and duplicate. A rule enforced in the REST controller is not enforced when the same operation is reached from an event consumer, an MCP tool, or a scheduled job — each adapter re-implements it, and they drift.
- It bypasses the transaction boundary. Orchestration and transactions are an application-layer responsibility; running them from a controller or a repository impl puts the atomic unit in the wrong place.
- It hollows out the domain. Logic that belongs on the aggregate (`order.ship()`) instead sits in the adapter, producing the [anemic domain model](/pitfall/anemic-domain-model.md) as a side effect.

## What forbids it

- [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) — a controller must drive the application through an input port, not reach past it; the moment it does, it has taken on orchestration that isn't its job.
- [Classes from the domain should not access port adapters](/rule/hexagonal/dca-hex-001.md) — the dependency arrow points inward; adapters are the outermost ring and hold no rules the inner rings depend on.
- [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md) — orchestration that opens a transaction cannot live in an incoming adapter.
- [Domain must not have dependencies on Infrastructure](/rule/layered/dca-lay-002.md) — the inversion that keeps rules framework-free; violating it usually means the rule migrated outward into the adapter.

## Do instead

Keep the adapter thin: map the request to a `Command`/`Query`, call the input port, map the `Result` back. Put invariants on the aggregate and orchestration in the `*UseCase`.

`OrderResource` → `PlaceOrderInputPort.execute(command)` → `PlaceOrderUseCase` (loads aggregate, calls `order.place()`, saves) — the controller decides nothing.

- [Recipe: add a use case](/recipe/add-a-use-case.md) · [Template: use case](/template/use-case.md)
- Decision: [Where does the logic live?](/decision/where-does-the-logic-live.md)

## Anchors

- Rules: [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) · [Classes from the domain should not access port adapters](/rule/hexagonal/dca-hex-001.md) · [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Guide: [Port placement](/guide/quick-reference/port-placement.md)
- Sibling pitfall: [Anemic domain model](/pitfall/anemic-domain-model.md) · [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md)
