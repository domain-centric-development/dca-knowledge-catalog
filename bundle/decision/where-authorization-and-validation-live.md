---
type: Decision
title: "Where authorization and validation live: adapter, use case, or aggregate"
tags: [decision, security, layered, adapter, application, domain]
---

You have a check to place that guards an operation, and "check" hides three different concerns that are routinely confused: **structural validation** (is the input well-formed?), **authorization** (may *this caller* perform this action?), and **business invariants** (is this action legal for the current state?). Each belongs on a different layer, and collapsing them is how you get controllers that enforce business rules, aggregates that know about roles, and duplicated guards that disagree. This decision sits alongside [Where does the logic live](/decision/where-does-the-logic-live.md) — that one places *behaviour*; this one places *guards*.

## The discriminator

Ask what the check actually depends on:

1. **Does it depend only on the shape of the request — required fields present, formats valid, sizes in range, no obviously hostile content?** Then it is **structural validation** at the **adapter edge**. Bean Validation (`@Valid`), format checks, and input sanitisation run before anything is mapped to a command. It needs no domain state and no identity.
2. **Does it depend on *who is calling* — their identity, roles, or ownership of the resource?** Then it is **authorization**, and it belongs in the **use case (application layer)**. The caller is resolved through an identity output port (an [OutputPort](/marker/port-out/outputport.md)) and arrives as part of the command or query; the use case decides "may this identity run this operation on this resource" *after* loading the aggregate and *before* invoking its behaviour. The one exception is drawn below.
3. **Does it depend on the aggregate's own state and express a rule of the business — a legal state transition, a quantity limit, a consistency guarantee?** Then it is an **invariant**, enforced **inside the aggregate**, with no knowledge of the caller. `order.cancel()` refuses a shipped order regardless of who asks.

A quick tell: if removing the check would let malformed JSON through → adapter. If it would let the *wrong person* through → use case. If it would let the aggregate into an *illegal state* → domain.

Do **not** use "is it business or is it technical" as the discriminator. It splits nothing: a role name is part of the ubiquitous language, and an ownership check is an id comparison. Ask what the check *reads* instead.

### The one authorization check that may stay at the edge

Split authorization once more, by whether the check needs the **resource**:

- **It needs the aggregate** — is this cart the caller's, is this order theirs, may they see this invoice? Then it belongs to the *operation* and lives in the use case. It can never be a property of one exposure: no caller may act on a stranger's cart, through any adapter, ever. So the caller becomes part of the command (`GetCartByIdQuery(cartId, customerId)`), and the repository is asked a scoped question (`findByIdForCustomer`) rather than an open one plus an `if`.
- **It reads only the caller's claims** — does this token carry an operator role? Then it is a coarse gate on the *exposure*, and the incoming adapter is a legitimate home for it. The same use case may be perfectly reachable from a batch job or an operator console with no end user at all, and forcing an identity port into it to satisfy a rule about one HTTP route would make it unusable there.

**The decision belongs to the use case; its rendering belongs to the adapter.** Whether a refusal appears as `403` or as `404` is a protocol question — and it matters, because a `403` on a resource the caller does not own *confirms that the id exists*. The use case answers "nothing here for you"; the adapter chooses how to say it.

**A use case with no caller is not under-specified.** An event consumer completing a cart after a confirmed checkout acts on nobody's behalf, at least once, with no identity to check. Leave it unscoped and say so — otherwise the next reader "fixes" it.

## Options

| | Structural validation | Authorization | Business invariant |
|---|---|---|---|
| Question it answers | Is the input well-formed? | May this caller do this? | Is this legal for the state? |
| Lives in | adapter (incoming) | application (use case); a claims-only gate may stay in the adapter | domain (aggregate/VO) |
| Depends on | request shape only | caller identity, usually + the resource | aggregate state only |
| Reaches for | `@Valid`, sanitiser | identity output port, authorization policy | the aggregate's own fields |
| Knows the caller? | no | yes | **never** |
| On failure | 400 / rejected request | access denied | domain exception |

**Defense in depth, not duplication.** The layers are complementary, not redundant: the adapter rejects garbage so the use case never sees it; the use case rejects unauthorized callers so the aggregate is only ever invoked on behalf of someone allowed; the aggregate protects its invariants so no use case — authorized or not — can corrupt it. Each guards a distinct failure, so none is a substitute for another.

## Consequences

- **Authorization must not sink into the domain.** An aggregate that takes a `User` or checks a role is the [authorization-in-domain-layer](/pitfall/authorization-in-domain-layer.md) anti-pattern — it couples the domain to access control and, if it pulls in Spring Security, breaks domain framework-independence rules.
- **Business rules must not float up into the adapter.** A controller that decides whether an order may be cancelled is [business logic in an adapter](/pitfall/business-logic-in-adapter.md); the adapter validates *shape*, never *rules*.
- **Identity is an output port, never a domain type.** Only the application and adapter layers may resolve the current caller, and only through an identity output port — the interface in `application/shared/` (of the owning context, or of the shared kernel when several contexts need it), the implementation (JWT/session/API key) in an adapter.
- **A command that names a resource without naming whose it is, is incomplete.** "Check out cart X" does not say on whose behalf, so every adapter that builds it has to supply the missing guard, and one of them eventually will not. Look for the asymmetry: if some of a context's use cases already take the caller as input and others take only an id, the second group is where the holes are.
- **An Open Host Service inherits the same duty.** If another context may ask for a cart by id, it has to name the customer it is acting for; otherwise the ownership rule holds in the owning context but not across the boundary, and the consuming context re-implements it — or forgets to.
- **Structural validation is not a business invariant.** "Quantity is a positive integer within request bounds" can be an adapter check; "this order may hold at most 100 lines" is a domain invariant the aggregate must enforce even if a malicious client bypasses the edge.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Rules: [Domain Models must not have Spring/JPA annotations](/rule/onion/domain-models-must-not-have-spring-jpa-annotations.md) · [Domain must not have dependencies on Infrastructure](/rule/layered/domain-must-not-have-dependencies-on-infrastructure.md)
- Guide: [Cookie requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md)
- Recipe: [Add an identity port](/recipe/add-an-identity-port.md) — the port, the command field, the scoped repository question
- Related decision: [Where does the logic live](/decision/where-does-the-logic-live.md)
- Related pitfalls: [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md) · [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Authenticated is not authorized](/pitfall/authenticated-is-not-authorized.md) · [Resource id without an owner](/pitfall/resource-id-without-an-owner.md)
