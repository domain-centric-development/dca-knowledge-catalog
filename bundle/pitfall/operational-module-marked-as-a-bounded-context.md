---
type: Pitfall
title: "Operational module marked as a bounded context"
tags: [pitfall, strategic, context-map, bounded-context]
---

A cross-cutting module — an operations backoffice, an admin shell, a reporting or monitoring surface, a "common" module — declared as a bounded context because that is how every other module in the code base is declared. It gets the context marker, appears on the context map, and acquires upstream declarations towards half the system.

## Why it is wrong

- A bounded context is a **boundary around a model and its language**. This module has neither: it owns no concept, no invariant, no term that means something different inside it than outside. What it owns is a *view* of other people's concepts.
- On the context map it is noise that looks like signal. It has an arrow to nearly everything, so it makes the map denser without telling a reader anything about the domain, and it drowns out the relationships that do carry meaning (which context is upstream of which, and through what).
- Its "upstream" declarations are not relationships in the strategic sense. Nobody negotiates a contract with the backoffice; it reads what is already published. Recording that as Customer/Supplier or Conformist puts a governance vocabulary on a technical convenience.
- It invites real domain logic to accumulate there. Once it is a context it may reasonably hold a model — and then admin pages start deciding pricing rules, because that is where the operator's screen lives.

## How to spot it

Ask what its ubiquitous language is. If the answer is a list of other contexts' terms, it is not a context. Two more tells: it would never be extracted into its own service on its own, and removing it would cost the business no capability, only visibility.

## What forbids it

- [Upstream, ExternalUpstream and Partnership may only be declared on bounded-context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md) — the map's relationship vocabulary is reserved for contexts, so a module that is not one must not carry it.
- [New context vs. extend existing](/decision/new-context-vs-extend-existing.md) — the same question asked before a context is created at all.

## Do instead

Leave the marker off. An operational module is an ordinary module: it consumes other contexts' published interfaces through their Open Host Services like any other consumer, it has no context declaration, and it stays off the context map — the same treatment as the composition root and the web host, which nobody is tempted to declare either.

Say so where the module is declared, in one sentence, so the omission reads as a decision rather than as an oversight: *this module serves cross-cutting operational concerns; it is not a business bounded context.*

**Admin screens that belong to a context stay in it.** Editing a price is Pricing's business and belongs in Pricing, behind whatever route the operator navigates to. Only what belongs to *no* context — the cross-cutting dashboard, the operator's navigation, the publication log — belongs in the operational module.

**Watch what it is allowed to reach.** Not being a context is not a licence to import other contexts' internals; it consumes published interfaces exactly as a context would.

- Related decisions: [New context vs. extend existing](/decision/new-context-vs-extend-existing.md) · [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)

## Anchors

- Markers: [BoundedContext](/marker/strategic/boundedcontext.md) · [OpenHostService](/marker/strategic/openhostservice.md)
- Rules: [Upstream, ExternalUpstream and Partnership may only be declared on bounded-context packages](/rule/contextmap/upstream-externalupstream-and-partnership-may-only-be-declared-on-bounded-context-packages.md)
