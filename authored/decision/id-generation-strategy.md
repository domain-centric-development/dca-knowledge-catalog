---
type: Decision
title: Where an identifier comes from
tags: [decision, tactical, value-object, aggregate, entity, factory, port-out]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/factory.md, /guide/elements.md, /marker/port-out/outputport.md, /guide/spring-modulith/shared-kernel-in-spring-modulith.md, /marker/tactical/aggregateroot.md, /marker/tactical/entity.md]
---

When you create something that has identity, its `Id` has to come from somewhere. The fork is the **source** of that identifier: the **domain generates** it, a **factory assigns** it during complex creation, it is an **externally-owned identity** you receive (the current user, a foreign system's key), or — the anti-pattern — you let the **database** hand back a generated number after the insert. The default in DCA is that identity is a first-class domain concern, minted before persistence, and modelled as a typed Value Object rather than a raw `Long` or `String`.

## The discriminator

Ask, in order:

1. **Is this an aggregate/entity you create, or an actor/subject you're handed?** If your code brings the thing into existence (an order, a cart), the domain owns its identity — go to question 2. If the identifier is *someone else's* — the authenticated user, an external system's record — it is an **externally-sourced identity**; you receive it, you don't mint it (for the current user, from an identity output port; for a foreign system, through an anti-corruption layer).
2. **Is creation simple or complex?** A straightforward creation mints the id in the typed ID's `generate()` factory method (`UUID.randomUUID()` behind a `record ...Id implements Value`). If creation is complex, involves assembling the id with other invariants, or raises creation events, move id generation into a **[Factory](/marker/tactical/factory.md)**.
3. **Does a meaningful natural key already exist?** Occasionally the domain already has a stable, unique, immutable business identifier (an ISBN, a country code). It can *be* the typed id — but only if it truly never changes; anything mutable must not be an identity.
4. **Are you tempted to let the DB assign it?** If the only reason an id would come from the database is "that's how JPA does it," stop — a DB-generated surrogate forces the aggregate to exist in a half-built, id-less state before save and pushes toward an anemic `Long id` with setters. Prefer a domain-minted typed id.

## Options

### Domain-generated typed id (default)

A typed ID Value Object with a `generate()` factory: `record ProductId(UUID value) implements Value { static ProductId generate() { return new ProductId(UUID.randomUUID()); } }`. The aggregate is fully valid the moment it is constructed, before it ever touches a repository. Type safety prevents mixing one context's ids with another's.

- **When:** the common case — your context creates the aggregate and nothing external owns its identity.
- Ground: [Layer elements](/guide/elements.md)

### Factory-assigned id

The same domain-minted id, but generated inside a `Factory` because creation is complex, must stay consistent with other fields, or raises a creation event. Keeps id generation and the creation invariants in one framework-free place.

- **When:** complex aggregate creation, or creation that emits events.
- Ground: [Factory](/marker/tactical/factory.md) · [Add an aggregate](/recipe/add-an-aggregate.md)

### Externally-sourced identity

The identifier belongs to someone else. For the acting user, read it from an identity output port (an [OutputPort](/marker/port-out/outputport.md), e.g. `identityProvider.getCurrentIdentity().userId()`) — the security infrastructure supplies it; the domain never fabricates a user id. For a foreign system's key, bring it in through an anti-corruption layer so the foreign identifier is translated to your domain type at the boundary.

- **When:** the id is the current user (auth context) or a key owned by another system/context.
- Ground: [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)

**Default:** **the domain mints a typed id before persistence** — via the ID Value Object's `generate()`, or via a Factory when creation is complex. Use a natural key only when a business identifier is genuinely stable and immutable. Receive, never generate, an identity that another party owns (the user, a foreign system). Avoid DB-generated surrogate keys: they defer identity to after the insert and erode the rich, always-valid domain model.

## Anchors

- Markers: [OutputPort](/marker/port-out/outputport.md) · [Factory](/marker/tactical/factory.md) · [AggregateRoot&lt;T, ID&gt;](/marker/tactical/aggregateroot.md) · [Entity&lt;T, ID&gt;](/marker/tactical/entity.md)
- Guide: [Layer elements](/guide/elements.md) · [Shared kernel](/guide/spring-modulith/shared-kernel-in-spring-modulith.md)
- Recipes: [Add an aggregate](/recipe/add-an-aggregate.md)
- Related decisions: [Entity or Value Object](/decision/entity-vs-value-object.md) · [Factory vs. constructor](/decision/factory-vs-constructor.md)
