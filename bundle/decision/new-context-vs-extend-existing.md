---
type: Decision
title: "New bounded context or extend an existing one"
tags: [decision, strategic, bounded-context, subdomain, package-structure]
---

A new feature has landed. The fork is whether it belongs **inside an existing bounded context** or deserves a **new context** of its own. Splitting too early scatters a single cohesive model across boundaries you then fight to cross; splitting too late lets one word mean three things and one team block another. The boundary is linguistic and organizational before it is technical.

## The discriminator

Ask, in order:

1. **Does a core term change meaning?** If the feature uses a word the existing context already owns but means something *different* by it ("Customer" as a buyer vs. "Customer" as a support ticket-holder), that linguistic fault line is the strongest signal for a **new context**. If the feature speaks the same ubiquitous language, it **extends** the existing one.
2. **Would it conflict with the existing model?** If the feature forces the existing aggregates to carry state and rules they otherwise wouldn't — bending invariants to fit two masters — it wants a **new context**. If it composes cleanly with the current aggregates and use cases, **extend**.
3. **Who owns it, and does it change on a different rhythm?** A different team, a different change frequency, or different scalability / security / compliance needs all point to a **new context** (they are the classic split indicators). Same team, same rhythm → **extend**.
4. **Is it a distinct business capability or subdomain?** A recognizably separate capability (pricing vs. catalog, shipping vs. orders) aligns with a **new context**; a refinement of an existing capability **extends** it.

If the answers are mixed, favor extending: a context you keep can always be split later along a boundary you now understand better, but a premature split is expensive to merge back.

## Options

### Extend an existing context

Add the aggregate, use case, or adapter into the current context's layers. The feature shares that context's ubiquitous language and rule set, and no new boundary or cross-context plumbing appears.

- **When:** same language, no model conflict, same ownership and change rhythm, a refinement of an existing capability.
- Build it: [Add a use case](/recipe/add-a-use-case.md) · [Add an aggregate](/recipe/add-an-aggregate.md)

### Create a new bounded context

Carve a new top-level package annotated with [@BoundedContext](/marker/strategic/boundedcontext.md), with its own `domain/`, `application/`, and `adapter/` layers and a hard boundary to every other context. Classify its subdomain type first (core / supporting / generic) — that choice drives which pattern set and rule strictness apply. Communication to other contexts goes only through their Open Host Service or their integration events.

- **When:** a term changes meaning, the model would conflict, a different team owns it, or it is a distinct capability/subdomain.
- Build it: [Add a bounded context](/recipe/add-a-bounded-context.md) · classify it: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)

**Neither, sometimes.** A module that owns no concept of its own — an operational backoffice, an admin shell, a reporting surface — is not a third option on this list; it is not a context at all. Give it no context marker and keep it off the map: [Operational module marked as a bounded context](/pitfall/operational-module-marked-as-a-bounded-context.md).

**Default:** **start together, split later.** Don't open with many contexts — keep features in one context (as separate packages) until a real boundary earns its own. Let it split when a term's meaning forks, the model starts fighting itself, or a second team needs to own and release a piece independently. When two contexts share a small stable model instead, weigh [Shared kernel vs. duplication](/decision/shared-kernel-vs-duplication.md) rather than merging them back.

## Anchors

- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [@SharedKernel](/marker/strategic/sharedkernel.md)
- Rules: [Bounded contexts must not directly access each other in the application layer](/rule/strategic/bounded-contexts-must-not-directly-access-each-other-in-application-layer-except-allowed-dependencies.md)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Context-specific rule sets](/guide/archunit-governance/context-specific-rule-sets.md)
- Recipes: [Add a bounded context](/recipe/add-a-bounded-context.md) · [Add a use case](/recipe/add-a-use-case.md)
- Related decisions: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md) · [Shared kernel vs. duplication](/decision/shared-kernel-vs-duplication.md)
- Related pitfall: [Operational module marked as a bounded context](/pitfall/operational-module-marked-as-a-bounded-context.md)
