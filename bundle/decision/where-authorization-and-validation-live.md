---
type: Decision
title: "Where authorization and validation live: adapter, use case, or aggregate"
tags: [decision, security, layered, adapter, application, domain]
---

You have a check to place that guards an operation, and "check" hides three different concerns that are routinely confused: **structural validation** (is the input well-formed?), **authorization** (may *this caller* perform this action?), and **business invariants** (is this action legal for the current state?). Each belongs on a different layer, and collapsing them is how you get controllers that enforce business rules, aggregates that know about roles, and duplicated guards that disagree. This decision sits alongside [Where does the logic live](/decision/where-does-the-logic-live.md) — that one places *behaviour*; this one places *guards*.

## The discriminator

Ask what the check actually depends on:

1. **Does it depend only on the shape of the request — required fields present, formats valid, sizes in range, no obviously hostile content?** Then it is **structural validation** at the **adapter edge**. Bean Validation (`@Valid`), format checks, and input sanitisation run before anything is mapped to a command. It needs no domain state and no identity.
2. **Does it depend on *who is calling* — their identity, roles, or ownership of the resource?** Then it is **authorization**, and it belongs in the **use case (application layer)**. The caller is resolved through the [IdentityProvider](/marker/port-out/identityprovider.md) output port; the use case decides "may this identity run this operation on this resource" *after* loading the aggregate and *before* invoking its behaviour.
3. **Does it depend on the aggregate's own state and express a rule of the business — a legal state transition, a quantity limit, a consistency guarantee?** Then it is an **invariant**, enforced **inside the aggregate**, with no knowledge of the caller. `order.cancel()` refuses a shipped order regardless of who asks.

A quick tell: if removing the check would let malformed JSON through → adapter. If it would let the *wrong person* through → use case. If it would let the aggregate into an *illegal state* → domain.

## Options

| | Structural validation | Authorization | Business invariant |
|---|---|---|---|
| Question it answers | Is the input well-formed? | May this caller do this? | Is this legal for the state? |
| Lives in | adapter (incoming) | application (use case) | domain (aggregate/VO) |
| Depends on | request shape only | caller identity + resource | aggregate state only |
| Reaches for | `@Valid`, sanitiser | [IdentityProvider](/marker/port-out/identityprovider.md), authorization policy | the aggregate's own fields |
| Knows the caller? | no | yes | **never** |
| On failure | 400 / rejected request | access denied | domain exception |

**Defense in depth, not duplication.** The layers are complementary, not redundant: the adapter rejects garbage so the use case never sees it; the use case rejects unauthorized callers so the aggregate is only ever invoked on behalf of someone allowed; the aggregate protects its invariants so no use case — authorized or not — can corrupt it. Each guards a distinct failure, so none is a substitute for another.

## Consequences

- **Authorization must not sink into the domain.** An aggregate that takes a `User` or checks a role is the [authorization-in-domain-layer](/pitfall/authorization-in-domain-layer.md) anti-pattern — it couples the domain to access control and, if it pulls in Spring Security, breaks domain framework-independence rules.
- **Business rules must not float up into the adapter.** A controller that decides whether an order may be cancelled is [business logic in an adapter](/pitfall/business-logic-in-adapter.md); the adapter validates *shape*, never *rules*.
- **Identity is an output port, never a domain type.** Only the application and adapter layers may resolve the current caller, and only through `IdentityProvider` — the interface in the shared kernel, the implementation (JWT/session/API key) in an adapter.
- **Structural validation is not a business invariant.** "Quantity is a positive integer within request bounds" can be an adapter check; "this order may hold at most 100 lines" is a domain invariant the aggregate must enforce even if a malicious client bypasses the edge.

## Anchors

- Markers: [IdentityProvider](/marker/port-out/identityprovider.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Rules: [Domain Models must not have Spring/JPA annotations](/rule/onion/domain-models-must-not-have-spring-jpa-annotations.md) · [Domain must not have dependencies on Infrastructure](/rule/layered/domain-must-not-have-dependencies-on-infrastructure.md)
- Guide: [Cookie requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md)
- Related decision: [Where does the logic live](/decision/where-does-the-logic-live.md)
- Related pitfalls: [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md) · [Business logic in an adapter](/pitfall/business-logic-in-adapter.md)
