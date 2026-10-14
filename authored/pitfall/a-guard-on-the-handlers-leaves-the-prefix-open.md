---
type: Pitfall
title: A guard on the handlers leaves the prefix open
tags: [pitfall, security, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/rules.md, /decision/where-authorization-and-validation-live.md]
---

A protected area — everything under `/admin`, say — is protected by attaching the guard to its handlers: an authorize attribute on each controller, an annotation on each method, a check at the top of each handler. Every handler is guarded, and the area reads as closed. A catch-all handler for unknown addresses below the prefix, guarded the same way, seems to close the rest.

## Why it is wrong

- A guard attached to a handler runs only when that handler answers. A verb the handler does not take, or an address no handler serves, never reaches it: a `POST` below a prefix whose catch-all answers only `GET` is answered by the framework's default `404` or `405`, without the area's challenge.
- The defaults disclose the surface. An anonymous caller learns from `405` against `404` which addresses exist and which verbs they take, and a stranger and an authorized user get the same answer where one should be asked to authenticate first.
- The boundary is as complete as the most recently added handler. A new controller without the attribute opens a part of the area, and nothing at the prefix notices.

## What forbids it

- [Where authorization and validation live](/decision/where-authorization-and-validation-live.md) — a gate that only checks the caller's claims belongs at the incoming edge; the edge of an area is its prefix, not each handler inside it.

## Do instead

Protect the prefix, for every verb and every address below it: a path rule in the security configuration that matches the prefix and everything under it, a route group that carries the authorization requirement, or a middleware branch on the path — whatever the framework offers that runs before routing decides whether a handler exists. An unauthenticated request to any address below the prefix then receives the challenge first, and only an authorized caller learns whether the address exists. Guards on the handlers stay where they refine — a role one operation needs beyond the area's — never as the area's boundary.

Test the boundary where no handler is: one request per verb to an address below the prefix that nothing serves, each expected to be challenged.

- Related pitfalls: [Authenticated is not authorized](/pitfall/authenticated-is-not-authorized.md) · [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md)

## Anchors

- Guide: [Layer rules](/guide/rules.md)
- Decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
