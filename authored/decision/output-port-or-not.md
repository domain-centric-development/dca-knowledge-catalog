---
type: Decision
title: "Output port or not: what a use case may call without a port"
tags: [decision, application, hexagonal, port-out, port, use-case]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/outputport.md, /marker/port-in/inputport.md, /marker/application/transactionboundary.md, /rule/hexagonal/dca-hex-004.md, /rule/usecase/dca-use-013.md, /guide/elements.md, /guide/rules.md, /guide/dependency-structure.md]
---

An interface sits in the application layer, an adapter implements it, and it carries the `OutputPort` marker. The fork is whether it *is* a port. Not everything a use case calls is one, and not every interface an adapter implements is one. Get this wrong and the word "port" stops meaning anything: every helper qualifies, the port rules have to special-case the helpers, and a reviewer can no longer read the application's real dependencies off its ports.

## The definitions

- An **input port** is what the application offers to its drivers: one interface per use case, called by an incoming adapter.
- An **output port** is a capability needed from something outside the process boundary of the use case: persistence, another bounded context, an external system, messaging, and the identity of the caller when it comes from an identity system. Use cases call output ports; an incoming adapter legitimately uses one — the identity port — to translate request context into the project's language before the caller becomes a field of the Command or Query.

## The discriminator

Ask, in order:

1. **Does it stand for something outside the process?** A transaction boundary defines how several port calls run together; it reaches nothing outside. That is execution semantics, not a port. The caller's identity, when an identity system issues it, does stand for something outside — the identity port is a port.
2. **Is it protocol mechanics?** Cookies, tokens, sessions and response headers belong to the incoming adapter that owns the protocol. An interface for them may exist inside the adapter package; it is no port, whoever implements it.
3. **Which direction does the question travel?** When a filter or adapter asks its *own* bounded context whether an account exists or an order is open, the call points inward. That is a query use case or the context's published API, not an output port.
4. **Who depends on it?** A use case, or the incoming adapter that resolves the caller through the identity port. An `OutputPort` with neither dependent expresses no need of the application; it is an adapter collaborator wearing a marker. Move it next to its caller and drop the marker.

## Options

| Candidate | Verdict | Where it lives |
|---|---|---|
| Repository, Store, event publisher, another context's data, a payment or mail provider | output port | `application/shared/` or the use-case package; implemented in `adapter/outgoing/` |
| Transaction boundary, unit of work | not a port — execution semantics | building blocks' `application` package; implementation in infrastructure |
| The caller's identity, issued by an identity system | output port — the identity port | `application/shared/` (context or shared kernel), used by the incoming adapter; the caller then travels as a Command/Query field |
| Cookie, token, session handling | not a port — adapter mechanics | a class in the incoming adapter package, no marker |
| "Does this account exist?" asked by a filter into its own context | not an output port — inbound question | a query use case or the published API |
| Plugin registry with `register`/`unregister` next to `find` | mixed | `find` is the port capability; registration is composition-time wiring and belongs to infrastructure |

**Default:** when in doubt, the interface is not a port. A port is a claim about the application's dependencies on the outside world; a claim nobody can verify against a dependent inside weakens every other port. The test in one sentence: *does this interface stand for something outside the process that the application needs?*

## Consequences

- Every `OutputPort` subtype has a dependent in the application layer, or it is the identity port an incoming adapter uses. This is **checkable**: a rule could flag an output port with no application-side dependent ("port without an application-side caller"), with the identity port declared as the one allowed exception, by inspecting dependents statically. No such rule exists yet; the catalog records the candidate.
- Adapter mechanics lose the marker and move into the adapter package, which keeps [Incoming Adapters must only use outbound ports](/rule/hexagonal/dca-hex-004.md) about what it is about: an incoming adapter reaches no infrastructure; it drives use cases and may resolve the caller through the identity port.
- The transaction rules keep a short allowed list — [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md) names the real transactional resources — because nothing that is not a port sits on it.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [InputPort](/marker/port-in/inputport.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Rules: [Incoming Adapters must only use outbound ports](/rule/hexagonal/dca-hex-004.md) · [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md)
- Guide: [Layer elements](/guide/elements.md) · [Layer rules](/guide/rules.md) · [Dependency structure](/guide/dependency-structure.md)
- Related pitfall: [Transaction boundary modelled as an output port](/pitfall/transaction-boundary-modelled-as-an-output-port.md)
- Related decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md) · Recipe: [Add an identity port](/recipe/add-an-identity-port.md)
