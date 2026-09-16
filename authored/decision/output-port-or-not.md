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
- An **output port** is a capability a use case needs from something outside the process boundary of the use case: persistence, another bounded context, an external system, messaging. A use case is the caller of every output port.

## The discriminator

Ask, in order:

1. **Does a use case call it?** If only adapters or infrastructure depend on the interface, the application has no need to express. It is an adapter collaborator; move it next to its caller and drop the marker.
2. **Does it stand for something outside the process?** A transaction boundary defines how several port calls run together; it reaches nothing outside. That is execution semantics, not a port.
3. **Is it request context?** Who the current caller is belongs to the request, not to a downstream system. It travels as a field of the Command or Query, filled by the incoming adapter from the authenticated request. A use case never asks a port who is calling.
4. **Is it protocol mechanics?** Cookies, tokens, sessions and response headers belong to the incoming adapter that owns the protocol. An interface for them may exist inside the adapter package; it is no port.
5. **Which direction does the question travel?** When a component asks its *own* bounded context whether an account exists or an order is open, the call points inward. That is a query use case or the context's published API, not an output port.

## Options

| Candidate | Verdict | Where it lives |
|---|---|---|
| Repository, Store, event publisher, another context's data, a payment or mail provider | output port | `application/shared/` or the use-case package; implemented in `adapter/outgoing/` |
| Transaction boundary, unit of work | not a port — execution semantics | building blocks' `application` package; implementation in infrastructure |
| Current caller / identity | not a port — request context | a Command/Query field the incoming adapter fills |
| Cookie, token, session handling | not a port — adapter mechanics | a class in the incoming adapter package, no marker |
| "Does this account exist?" asked by a filter into its own context | not an output port — inbound | a query use case or the published API |
| Plugin registry with `register`/`unregister` next to `find` | mixed | `find` is the port capability; registration is composition-time wiring and belongs to infrastructure |

**Default:** when in doubt, the interface is not a port. A port is a claim about the application's dependencies on the outside world; a claim nobody can verify against a use case weakens every other port. The test in one sentence: *does this interface stand for something outside the process that a use case needs?*

## Consequences

- Every `OutputPort` subtype has at least one dependent in the application layer. This is **checkable**: a rule could flag an output port with no application-side dependent ("port without an application-side caller") by inspecting dependents statically. No such rule exists yet; the catalog records the candidate.
- Adapter-only interfaces lose the marker and move into the adapter package, which keeps [Incoming Adapters must only use outbound ports](/rule/hexagonal/dca-hex-004.md) about what it is about: an incoming adapter reaches no infrastructure, and what it needs from the application it gets through a use case.
- The transaction rules keep a short allowed list — [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md) names the real transactional resources — because nothing that is not a port sits on it.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [InputPort](/marker/port-in/inputport.md) · [TransactionBoundary](/marker/application/transactionboundary.md)
- Rules: [Incoming Adapters must only use outbound ports](/rule/hexagonal/dca-hex-004.md) · [Declaratively transactional use cases must not call remote-capable output ports](/rule/usecase/dca-use-013.md)
- Guide: [Layer elements](/guide/elements.md) · [Layer rules](/guide/rules.md) · [Dependency structure](/guide/dependency-structure.md)
- Related pitfall: [Transaction boundary modelled as an output port](/pitfall/transaction-boundary-modelled-as-an-output-port.md)
- Related decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
