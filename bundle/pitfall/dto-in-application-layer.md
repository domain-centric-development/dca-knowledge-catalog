---
type: Pitfall
title: Adapter DTO in the application layer
tags: [pitfall, use-case, application, dto]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-011.md, /rule/naming/dca-nam-007.md, /guide/rules.md, /guide/elements.md, /marker/port-in/usecase.md]
---

Passing a presentation or transport DTO — a REST request body, a JSON-bound `*Dto`, a form-backing object — straight into a use case as its input, or returning one as its output. The adapter's serialization type becomes the application's contract, so the boundary between "how data arrives" and "what the use case needs" collapses.

## Why it is wrong

- It couples the application to a delivery mechanism. A use case that accepts an `OrderRequestDto` is now tied to the HTTP/JSON shape; the same operation can't be driven from a scheduler, a message consumer, or a test without constructing a web DTO.
- DTOs are shaped by the wire, not the domain. They carry nullable strings, framework binding annotations, and fields the use case doesn't need — validation and intent get muddled.
- It smuggles adapter concerns inward, the same dependency-rule violation as a framework leak, one layer up.
- Output DTOs pull presentation formatting into the application, so the use case starts deciding how things are *displayed* instead of *what happened*.

## What forbids it

- [DTOs must not be used in the Application Layer](/rule/usecase/dca-use-011.md) — the direct, mechanical prohibition.
- [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md) — pins DTOs to the adapter layer where they belong.

## Do instead

Define the use case's input and output as its **own** models — immutable `Command` (writes) or `Query` (reads) records in, a `Result` record out. The incoming adapter maps its DTO to the command at the edge and maps the result back to a response; the mapping is an adapter responsibility.

`RESTResource` receives `OrderRequestDto` → maps to `PlaceOrderCommand` → `PlaceOrderUseCase.execute(...)` returns `PlaceOrderResult` → adapter maps to `OrderResponse`.

- [Recipe: add a use case](/recipe/add-a-use-case.md) · [Template: use case](/template/use-case.md)

## Anchors

- Guide: [Layer rules](/guide/rules.md) · [Layer elements](/guide/elements.md)
- Markers: [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Related pitfall: [Framework leak in the domain layer](/pitfall/framework-leak-in-domain.md)
