---
type: Pitfall
title: "Authorization in the domain layer: aggregates that decide who may act"
tags: [pitfall, domain, application, security]
---

An aggregate method takes the caller as a parameter and branches on their role or permissions — `order.cancel(user)` that throws `AccessDeniedException` unless `user.hasRole(ADMIN)`. The domain now knows about users, roles, and access control. Authorization ("*may this caller* do this?") has leaked inward, where only invariants ("*is this action legal* for this state?") belong.

## Why it is wrong

- It couples the domain to concepts that are not part of the ubiquitous language of the business rule. `Order.cancel()` protects the invariant *a shipped order cannot be cancelled*; whether *this particular user* is allowed to cancel is a separate, cross-cutting concern that has nothing to do with the order's state.
- Identity is an **output-port abstraction**, not a domain type. The current caller is reached through an identity output port (the reference implementation calls it `IdentityProvider`) — an [OutputPort](/marker/port-out/outputport.md) whose implementation lives in an adapter (JWT, session, API key). An aggregate that needs a `User`/roles either imports that infrastructure concern or duplicates a shadow identity model in the domain.
- It scatters the access-control policy. When authorization lives on aggregates, the same "who may do what" logic is smeared across many entities instead of sitting at the one boundary — the use case — that already owns the operation, its transaction, and its command/query model.
- It makes the domain untestable in isolation. A pure invariant test (`cancel a shipped order → rejected`) now has to construct a user with the right roles just to exercise a business rule that does not depend on the user.

## What forbids it

There is no ArchUnit rule that counts a `User` parameter, so authorization-on-an-aggregate is primarily a **design smell** — but the moment it reaches for real access-control machinery it also breaks mechanical rules:

- [Domain Models must not have Spring/JPA annotations](/rule/onion/domain-models-must-not-have-spring-jpa-annotations.md) — a `@PreAuthorize` on a domain method fails here.
- [The Domain Model should be framework independent and should not use 3rd party libraries when possible](/rule/onion/the-domain-model-should-be-framework-independent-and-should-not-use-3rd-party-libraries-when-possible.md) — importing Spring Security's `SecurityContextHolder`/`AccessDeniedException` into the domain is a framework leak.
- [Domain must not have dependencies on Infrastructure](/rule/layered/domain-must-not-have-dependencies-on-infrastructure.md) — identity resolution is infrastructure, reached only via an output port.

## Do instead

Keep the three responsibilities on their own layers:

- **Domain** enforces the *invariant* with no knowledge of the caller: `order.cancel()` refuses when `status == SHIPPED`, full stop — no `User` parameter.
- **Use case** performs the *authorization* check before delegating: resolve the caller via `IdentityProvider`, decide whether they may run this operation on this resource, then call the parameter-free aggregate method.
- **Adapter** handles *authentication* and structural input validation at the edge.

For the full layer split of validation vs. authorization vs. invariants, see [Where authorization and validation live](/decision/where-authorization-and-validation-live.md); for the port itself and how the caller travels as a command field, follow [Add an identity port](/recipe/add-an-identity-port.md).

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md)
- Rules: [Domain Models must not have Spring/JPA annotations](/rule/onion/domain-models-must-not-have-spring-jpa-annotations.md) · [The Domain Model should be framework independent](/rule/onion/the-domain-model-should-be-framework-independent-and-should-not-use-3rd-party-libraries-when-possible.md) · [Domain must not have dependencies on Infrastructure](/rule/layered/domain-must-not-have-dependencies-on-infrastructure.md)
- Guide: [Cookie requirements](/guide/jwt-implementation-guide/7-cookie-requirements.md)
- Decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
- Recipe: [Add an identity port](/recipe/add-an-identity-port.md)
- Related pitfalls: [Framework leak in the domain](/pitfall/framework-leak-in-domain.md) · [Anemic domain model](/pitfall/anemic-domain-model.md)
