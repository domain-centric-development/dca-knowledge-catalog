---
type: Decision
title: Group use cases into features or split the bounded context
tags: [decision, strategic, bounded-context, package-structure, feature, application]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/usecase/dca-use-014.md, /rule/cycles/dca-cyc-005.md, /guide/readme/java-package-structure.md, /rule/cycles/dca-cyc-002.md]
---

A bounded context's application layer has grown: a dozen or more use-case packages sit in one flat list under `application/`, and the list no longer reads as anything. Two moves relieve that — **group the use cases into features** inside the context, or **split the context** — and they answer different questions. A feature is a navigation and cohesion boundary below the layer; a bounded context is a language and model boundary. Choosing the package move when the real problem is the model (or the reverse) leaves the problem in place.

## The discriminator

Ask, in order:

1. **Is the language still one language?** If every use case in the long list uses the same words for the same things — one `CheckoutSession`, one meaning of "confirm" — the context is intact and the list is a **package-pressure** problem: **group**. If a core term has started to mean two things, the fault line is linguistic and no folder fixes it: **split** (see [New bounded context or extend an existing one](/decision/new-context-vs-extend-existing.md)).
2. **Does one aggregate serve all of them?** If the use cases are different intentions against the same model with the same invariants, they belong together and the model must stay whole: **group**, and never mirror the domain per feature. If the aggregate is being bent to carry state and rules for two masters, the boundary is inside the model: **split**, or at least revisit the aggregate ([Aggregate boundary and size](/decision/aggregate-boundary-size.md)).
3. **Who owns it, and at what rhythm?** One team, one change rhythm, one deployment: **group**. Two teams blocking each other, different release cadences, different scaling or compliance needs: **split** — and then decide how far ([Modulith or microservice extraction](/decision/modulith-vs-microservice-extraction.md)).
4. **What would the grouped tree look like?** If the natural groups have names from the ubiquitous language (`session`, `cartrecovery`, `checkoutcompletion`), grouping is honest. If the only names you find are technical (`commands`, `queries`, `handlers`) there is no cohesion to expose — leave the list flat and look for a better cut. If a group wants its *own* domain folder, it is not a feature; it is a module, and probably a context.

When the answers are mixed, group first. A grouping is one move per context and fully reversible; a split introduces `api`/`events` contracts, integration events and an anti-corruption layer that are expensive to take back.

## Options

### Group the use cases into features

Introduce the optional fourth scale — `system → bounded context → layer → feature → use case` — by moving every use-case package of the context under a domain-named feature package: `application/{feature}/{usecase}/`. The use cases are untouched inside; the domain, `application/shared`, `api`, `events` and the outgoing adapters stay as they are. Incoming adapters may mirror the features *below* their protocol (`adapter/incoming/web/{feature}`).

- **When:** one language, one model, one team; the flat list has become hard to navigate and the groups have domain names.
- **Rules:** one form per context — flat or grouped, never both after the migration ([Use case packages within a module must use one consistent depth](/rule/usecase/dca-use-014.md)); the feature packages must not form cycles ([Feature and use case packages within a module's application layer must not have cyclic dependencies](/rule/cycles/dca-cyc-005.md)); repositories and stores stay in `application/shared` — there is no `application/{feature}/shared`.
- **Not this:** a vertical slice `{context}/{feature}/{domain,application,adapter}`. The layer segment below the feature makes every slice a structural module of its own, and the isolation rules then rightly forbid one slice reaching into another's domain. Do not weaken them to let a shared aggregate span slices.
- Build it: [Add a use case](/recipe/add-a-use-case.md) — placement in a flat or grouped context.

### Split the bounded context

Carve the diverged part out as a context of its own, with its own model and glossary, and let the two talk through published contracts (`api`, `events`), an anti-corruption layer where the languages differ.

- **When:** a core term has changed meaning, the aggregate serves two masters, or ownership and rhythm have diverged.
- **Cost:** contracts, integration events, translation, an entry on the context map — and a boundary you cannot remove cheaply.
- Build it: [Add a bounded context](/recipe/add-a-bounded-context.md) · [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md) · [Publish a cross-context event](/recipe/publish-a-cross-context-event.md)

### Leave the list flat

If the context is small, or the only groups you can name are technical, do nothing. A flat list of eight self-contained use-case folders is a legitimate end state; the "about ten entries" guidance is a prompt to evaluate, not a law.

## What a feature is not

A feature is not a layer, not a module, not an aggregate owner, not a deployment unit and not a participant of the context map. Nothing in the rule library infers a bounded context or aggregate ownership from a feature package, and no marker or annotation declares one — the package convention is the whole mechanism. Whether a feature name is truly a term of the ubiquitous language is decided by people and the glossary, not by a rule.

## Anchors

- Guide: [Java package structure](/guide/readme/java-package-structure.md) — the canonical grouped tree and the eight rules of the feature scale
- Related decisions: [New bounded context or extend an existing one](/decision/new-context-vs-extend-existing.md) · [Aggregate boundary and size](/decision/aggregate-boundary-size.md) · [Modulith or microservice extraction](/decision/modulith-vs-microservice-extraction.md)
- Rules: [One consistent use-case depth per module](/rule/usecase/dca-use-014.md) · [No cycles between feature or use-case packages](/rule/cycles/dca-cyc-005.md) · [Application layer must not have cyclic dependencies](/rule/cycles/dca-cyc-002.md)
