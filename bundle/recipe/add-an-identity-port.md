---
type: Recipe
title: Add an identity port
tags: [recipe, application, adapter, security, shared-kernel]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/outputport.md, /guide/elements.md, /rule/layered/dca-lay-002.md, /rule/layered/dca-lay-003.md, /rule/hexagonal/dca-hex-010.md, /rule/hexagonal/dca-hex-009.md, /rule/hexagonal/dca-hex-011.md, /rule/onion/dca-oni-002.md]
---

Give the application a way to learn *who is calling* without letting authentication leak into use cases or the caller leak into the domain. The identity port is a project-specific [OutputPort](/marker/port-out/outputport.md) — deliberately **not** a building block: its contract returns the project's own identifier type and encodes the project's notion of anonymous vs. registered, and a marker only earns its place once a rule needs it. Write it per project, cut as below.

## Steps

1. **Declare the port in `application/shared/`** — of the shared kernel when several contexts need it, of one context otherwise ([Elements — Shared Kernel](/guide/elements.md)). It `extends OutputPort`, exposes one method such as `getCurrentIdentity()`, and returns an `Identity` built from the project's types (user id, roles, an extensible identity type). No token, cookie or header vocabulary in the contract.
2. **Implement it as an outgoing adapter of the authenticating context** — `adapter/outgoing/security/` reads the security context the framework populated and maps it to the port's `Identity`. Everything else sees only the interface; swapping JWT for sessions or API keys touches this class alone.
3. **Let the authentication filter enrich, never gate** — it attaches an identity or nothing and the request always proceeds; an anonymous visitor *is* an identity. Do not place a blanket "must be authenticated" rule at the token boundary — authorization is decided per operation, not per token ([Where authorization and validation live](/decision/where-authorization-and-validation-live.md)).
4. **Put the caller into the command** — a use case that acts on someone's resource takes the caller as a field (`GetCartByIdQuery(cartId, customerId)`, `StartCheckoutCommand(cartId, customerId)`). The incoming adapter resolves the caller through the port and fills the field; the use case does not call the identity port itself. The [use case template](/template/use-case.md) shows the command/query shape.
5. **Ask the repository a scoped question** — `findByIdForCustomer(cartId, customerId)` instead of `findById` plus an `if`. The ownership rule then holds for every adapter that can reach the use case, and a stranger's id simply yields nothing ([Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)).
6. **Leave claims-only gates at the edge** — "does this token carry the staff role?" reads nothing but the caller, so the REST resource or page controller may check it and refuse ([Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)). Anything that needs the resource belongs to the use case (step 4).
7. **Keep the domain caller-free** — no `User` parameter on an aggregate method, no role check in a value object. `cart.checkout()` guards its own invariants; the use case has already answered *who may* ([Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md)).
8. **Mark caller-less use cases** — an event consumer that completes a cart after a confirmed checkout acts on nobody's behalf; keep its command unscoped and say so in a comment, or the next reader adds a guard that can never be satisfied.
9. **Render refusals in the adapter** — the use case answers "nothing here for you"; whether that becomes `403` or `404` is the resource's protocol decision (a `403` on a stranger's id confirms the id exists).
10. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project); a unit test of the use case passes a foreign `customerId` and expects an empty result, with no identity infrastructure involved ([Test a use case](/recipe/test-a-use-case.md)).

## Rules to satisfy (build-time checklist)

- [Domain must not have dependencies on Infrastructure](/rule/layered/dca-lay-002.md) — identity resolution is infrastructure, reached only through the port
- [Application Services must only use outbound ports, not infrastructure implementations](/rule/layered/dca-lay-003.md)
- [Output ports must not reside in the domain layer](/rule/hexagonal/dca-hex-010.md)
- [Output Ports in application shared must extend OutputPort](/rule/hexagonal/dca-hex-009.md)
- [Incoming adapters must depend on input port interfaces, not on use case classes](/rule/hexagonal/dca-hex-011.md)
- [The Domain Model should be framework independent](/rule/onion/dca-oni-002.md) — no security framework types in the domain

No rule counts a `User` parameter on an aggregate or a missing `customerId` on a command — steps 4, 5 and 7 are design discipline, checked in review.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Guide: [Elements — Shared Kernel](/guide/elements.md) · [Java package structure](/guide/package-structure.md) · [Rules — Authorization Rules](/guide/rules.md)
- Decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
- Pitfalls: [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md) · [Authenticated is not authorized](/pitfall/authenticated-is-not-authorized.md) · [Resource id without an owner](/pitfall/resource-id-without-an-owner.md)
- Related recipes: [Add a use case](/recipe/add-a-use-case.md) · [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md) · [Add a repository with adapter](/recipe/add-a-repository-with-adapter.md)
