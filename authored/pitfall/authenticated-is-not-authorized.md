---
type: Pitfall
title: "Authenticated is not authorized: a filter that enriches every request"
tags: [pitfall, security, adapter, application, infrastructure]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-out/outputport.md]
---

An authentication filter or middleware that resolves an identity for *every* request — minting an anonymous one for a first-time visitor so the cart survives — sitting under a blanket rule such as `anyRequest().authenticated()` or a globally applied authorize attribute. The rule reads like a gate and is treated as one: the endpoints behind it carry no check of their own.

## Why it is wrong

- An anonymous identity **is** an authentication. The blanket rule is satisfied by everybody, so it guards nothing; it excludes only a request that somehow reaches the pipeline with no identity object at all, which — given the filter — is no request.
- Nothing announces the mistake. The configuration looks locked down, the tests pass, and the endpoints are open. It is usually found by reading the filter, not by reading the routes.
- The failure is silent in the worst direction. Listing every customer's cart, fetching a stranger's order, creating a catalogue entry as an unauthenticated caller — all answer `200`.
- Enriching every request is itself the right design (an expired session must not cost the visitor their identity, and a page decides for itself who may see it). The defect is not the filter; it is believing the filter authorizes.

## What forbids it

- [Where authorization and validation live](/decision/where-authorization-and-validation-live.md) — authorization is a decision about *this caller and this resource*, taken where those are known, never a side effect of the identity being resolved.

## Do instead

Say what the filter does in its own documentation: *it enriches, it does not gate.* Then place each guard where its inputs are — ownership checks in the use case, with the caller as part of the command; a claims-only role gate at the incoming adapter if the operation is legitimately reachable without an end user. Keep the blanket rule if it still earns its place, but stop reading it as authorization.

Test the refusals, not only the successes: for every guarded operation, one case per role that must be turned away. A test that only exercises the happy path passes just as happily against an open endpoint.

- Related pitfalls: [Resource id without an owner](/pitfall/resource-id-without-an-owner.md) · [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md) · [CSRF-exempt API that accepts cookie authentication](/pitfall/csrf-exempt-api-that-accepts-cookies.md)

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md)
- Decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
