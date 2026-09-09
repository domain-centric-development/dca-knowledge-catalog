---
type: Pitfall
title: Operational module marked as a bounded context
tags: [pitfall, strategic, context-map, bounded-context]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/contextmap/dca-map-001.md, /marker/strategic/boundedcontext.md, /marker/strategic/openhostservice.md]
---

A cross-cutting module — an admin shell, a "common" module, a reporting surface that only reformats other contexts' data — declared as a bounded context because that is how every other module in the code base is declared. It gets the context marker, appears on the context map, and acquires upstream declarations towards half the system.

**The test is the language, not the role.** A module that operates the running system may well be a bounded context: if *event publication*, *completion*, *retry* mean something specific inside it and nothing outside, it owns a model — a generic subdomain, the kind one would rather buy than build, but a context. What this pitfall is about is the module whose every term is borrowed.

## Why it is wrong

- A bounded context is a **boundary around a model and its language**. The module this pitfall describes has neither: it owns no concept, no invariant, no term that means something different inside it than outside. What it owns is a *view* of other people's concepts.
- On the context map it is noise that looks like signal. It has an arrow to nearly everything, so it makes the map denser without telling a reader anything about the domain, and it drowns out the relationships that do carry meaning (which context is upstream of which, and through what).
- Its "upstream" declarations are not relationships in the strategic sense. Nobody negotiates a contract with the backoffice; it reads what is already published. Recording that as Customer/Supplier or Conformist puts a governance vocabulary on a technical convenience.
- It invites real domain logic to accumulate there. Once it is a context it may reasonably hold a model — and then admin pages start deciding pricing rules, because that is where the operator's screen lives.

## How to spot it

Ask what its ubiquitous language is, and answer with the terms — not with the module's purpose. If every term belongs to another context (*order*, *price*, *stock level*, only rearranged for a screen), it is not a context. If some term is its own and means nothing outside (*event publication*, *retry*, *tenant provisioning*), it is one, however unglamorous its subdomain.

A second tell, for the borrowed-language case: it would never be extracted into its own service on its own, because there would be nothing in it.

## What forbids it

- [Upstream, ExternalUpstream and Partnership may only be declared on bounded-context packages](/rule/contextmap/dca-map-001.md) — the map's relationship vocabulary is reserved for contexts, so a module that is not one must not carry it.
- [New context vs. extend existing](/decision/new-context-vs-extend-existing.md) — the same question asked before a context is created at all.

## Do instead

**Borrowed language — leave the marker off.** Such a module is an ordinary module: it consumes other contexts' published interfaces through their Open Host Services like any other consumer, it has no context declaration, and it stays off the context map — the same treatment as the composition root and the web host, which nobody is tempted to declare either. Say so where the module is declared, in one sentence, so the omission reads as a decision rather than as an oversight: *this module serves cross-cutting operational concerns; it owns no language of its own and is therefore no bounded context.*

**Its own language — declare it, and say which subdomain.** Then it is a context like any other and belongs on the map, typically as a generic subdomain and typically Separate Ways: it reads what others have already published and negotiates no contract, so it declares no upstream relationships. The tactical style follows the subdomain, so a transaction script over a `Store` is legitimate and it may have no `domain/` package at all.

**Admin screens that belong to a context stay in it.** Editing a price is Pricing's business and belongs in Pricing, behind whatever route the operator navigates to. Only what belongs to no *business* context — the cross-cutting dashboard, the operator's navigation, the publication log — belongs in the operational one.

**Watch what it is allowed to reach.** Either way it is no licence to import other contexts' internals: it consumes published interfaces exactly as a context would.

- Related decisions: [New context vs. extend existing](/decision/new-context-vs-extend-existing.md) · [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)

## Anchors

- Markers: [BoundedContext](/marker/strategic/boundedcontext.md) · [OpenHostService](/marker/strategic/openhostservice.md)
- Rules: [Upstream, ExternalUpstream and Partnership may only be declared on bounded-context packages](/rule/contextmap/dca-map-001.md)
