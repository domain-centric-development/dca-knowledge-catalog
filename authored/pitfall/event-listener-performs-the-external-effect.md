---
type: Pitfall
title: An event listener performs the external effect itself
tags: [pitfall, hexagonal, strategic, adapter, events, integration-event, anti-corruption-layer]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/hexagonal/dca-hex-006.md, /rule/hexagonal/dca-hex-004.md, /rule/strategic/dca-str-010.md, /rule/layered/dca-lay-004.md, /marker/port-out/outputport.md, /guide/integration-patterns.md]
---

A listener receives an integration event and calls the outside world in the same method: deserialise the message, build an HTTP request, send the mail, post to the ERP. The class is usually named for the event it consumes (`OrderConfirmedListener`) and reads as one honest unit of work — which is why it survives review. The trigger and the effect have been fused into one object.

## Why it is wrong

- **Consuming and effecting are opposite directions.** Receiving a contract is arriving traffic and belongs to an incoming adapter; calling a partner system is an outgoing adapter behind an output port. One class doing both crosses the hexagon twice and is reachable from neither side's tests.
- **There is no use case.** The decision *whether* to send, with which content, under which policy, has nowhere to live: it ends up as `if` statements between a deserialiser and an HTTP client. Nothing about it can be tested without a broker and a partner endpoint.
- **The retry policies fuse.** Message redelivery and partner-call retry become one loop with one backoff, so a failing partner replays the message and a redelivered message repeats the partner call. Neither system's semantics survive.
- **The event becomes the destination.** An integration event is a statement that something happened, not an instruction to call anybody. A listener that treats it as a command reintroduces exactly the coupling the contract was published to avoid.

## What forbids it

- [Incoming port adapters must not depend directly on outgoing port adapters within the same context](/rule/hexagonal/dca-hex-006.md) — the listener reaching the partner client is this dependency, in the one direction the rule names.
- [Incoming Adapters must only use outbound ports (not infrastructure implementations)](/rule/hexagonal/dca-hex-004.md) — reaching an HTTP client or a broker template configured in infrastructure is the same violation one layer down.
- [Event Listeners consuming integration events should use Anti-Corruption Layer](/rule/strategic/dca-str-010.md) — the listener's job is translation into this context's language; a rule the suite cannot assert, and therefore a review duty.
- [Transaction boundaries belong to the application layer](/rule/layered/dca-lay-004.md) — an effect that must be atomic with local state cannot be driven from an adapter.

## Do instead

Split it into the two things it already is:

- **the subscription** — an incoming adapter: receive the contract, translate it through the anti-corruption layer, call an input port. It stores nothing and calls no partner.
- **the effect** — a use case that decides, and an outgoing adapter named after the partner (`adapter/outgoing/email/`, `adapter/outgoing/erp/`) behind an output port the use case declares.

The event triggers the effect; it is not its destination. Each side then keeps its own failure handling: message redelivery against the subscription, bounded retry with backoff against the partner call, and an idempotency key so a repeated delivery cannot duplicate the external effect.

## Anchors

- Rules: [Incoming port adapters must not depend directly on outgoing port adapters](/rule/hexagonal/dca-hex-006.md) · [Incoming Adapters must only use outbound ports](/rule/hexagonal/dca-hex-004.md) · [Event Listeners consuming integration events should use Anti-Corruption Layer](/rule/strategic/dca-str-010.md)
- Markers: [OutputPort](/marker/port-out/outputport.md)
- Guide: [Integration patterns](/guide/integration-patterns.md)
- Sibling pitfall: [Business logic in an adapter](/pitfall/business-logic-in-adapter.md)
