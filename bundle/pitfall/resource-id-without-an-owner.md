---
type: Pitfall
title: "Resource id without an owner: a command that says which, never whose"
tags: [pitfall, application, security, adapter, use-case]
---

A command or query that identifies a resource belonging to somebody — `CheckoutCartCommand(cartId)`, `GetOrderQuery(orderId)`, `DownloadInvoiceQuery(invoiceId)` — and says nothing about on whose behalf it runs. The id reaches the use case straight from the outside: a path segment, a hidden form field, a request parameter. The use case loads the aggregate by that id and acts on it.

The ownership check, if it exists at all, sits in one incoming adapter, which reads the aggregate first and compares.

## Why it is wrong

- The command is **incomplete**, not merely unguarded. "Check out cart X" does not say whose checkout this is, so the instruction cannot be carried out correctly without information the caller never supplied.
- The missing half has to be supplied by every adapter that builds the command, and one of them eventually will not. A REST resource may be audited carefully while a server-rendered form posting the same id goes unexamined — and a hidden field is no harder to change than a path segment.
- A second adapter on the same use case — a second protocol, a background console, another context calling through an Open Host Service — inherits nothing. The guard is attached to one exposure, and the operation is what needed protecting.
- It cannot be tested where it matters. A use-case test constructs the command directly and passes, because the check lives somewhere else entirely.

## How to spot it

Look for the **asymmetry inside one context**. Some use cases already take the caller as input (`CreateCartCommand(customerId)`, `GetActiveCartQuery(customerId)`); others take only an id. The second group is where the holes are, and the split is usually accidental — the customer-keyed ones were written first, the id-keyed ones came later for an adapter that "already knew" the caller.

## What forbids it

- [Where authorization and validation live](/decision/where-authorization-and-validation-live.md) — a check that depends on the resource belongs to the operation, not to one exposure of it.

## Do instead

Put the caller into the command, next to the id, and let the use case ask a **scoped** question rather than an open one plus an `if`:

- `GetCartByIdQuery(cartId, customerId)`, `CheckoutCartCommand(cartId, customerId)`.
- A repository method that cannot answer wrongly — `findByIdForCustomer(cartId, customerId)` beside the plain `findById`. A relational adapter expresses it as a single `WHERE id = ? AND customer_id = ?`; "not there" and "not yours" become the same answer, which is exactly what a caller should be told.
- Keep the unscoped `findById` for the paths that genuinely act on nobody's behalf, and say so where it is used.

**An Open Host Service inherits the duty.** If another context may fetch the resource by id, make it name the party it is acting for; otherwise the rule holds inside the owning context and evaporates at the boundary, and the consuming context re-implements it — or forgets to.

**A use case with no caller is fine.** An event consumer reacting to the system's own event acts on nobody's behalf, at least once, with no identity to check. Leave it unscoped and write down why, or the next reader will "fix" it.

**Render the refusal at the edge.** The use case answers "nothing here for you"; the adapter decides whether that is a `404` or a `403` — and for a resource the caller does not own it is a `404`, because a `403` confirms the id exists.

- Related pitfalls: [Authenticated is not authorized](/pitfall/authenticated-is-not-authorized.md) · [Authorization in the domain layer](/pitfall/authorization-in-domain-layer.md) · [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md)

## Anchors

- Markers: [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- Decision: [Where authorization and validation live](/decision/where-authorization-and-validation-live.md)
