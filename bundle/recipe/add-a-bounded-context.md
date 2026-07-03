---
type: Recipe
title: "Add a bounded context"
tags: [recipe, strategic, bounded-context]
---

Carve out a new top-level context package with its own domain / application / adapter layers and a hard boundary to every other context. A bounded context is the unit of ownership, isolation, and pattern choice — decide its subdomain type before you write a line of code.

## Step 0 — decide (do this first)

Classify the subdomain: **core** (full tactical set — rich model, ports & adapters), **supporting** (simpler layering, transaction script is legitimate), or **generic** (buy, don't build). The choice drives which rule subset applies — see [pattern style per subdomain](/decision/pattern-style-per-subdomain.md) and record it in an ADR ([ADR-025](/adr/adr-025-pattern-selection-per-subdomain.md), [How to write an ADR](/process/creating-an-adr.md)).

## Steps

1. **Create the package** `{boundedcontext}/` at the top level (a Spring Modulith module boundary) and annotate it with `@BoundedContext(name = "...", description = "...")`.
2. **Lay out the layers** inside it: `domain/`, `application/` (with `shared/` for output ports), `adapter/incoming/`, `adapter/outgoing/`, and an optional per-context `infrastructure/`. Package by domain concept, never by technical bucket (`entities/`, `util/`).
3. **Keep the domain framework-free** — no cross-context imports. Reference other contexts only through their Open Host Service ([Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)) or by reacting to their integration events ([Publish a cross-context event](/recipe/publish-a-cross-context-event.md)).
4. **Seed the first slice** — one aggregate ([Add an aggregate](/recipe/add-an-aggregate.md)), one use case ([Add a use case](/recipe/add-a-use-case.md)), one incoming adapter ([Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)).
5. **Record the decision** — add the context to the context map with its subdomain type and relationships; capture the pattern-style choice in an ADR.
6. **Verify** — `./gradlew test-architecture`; the isolation rules below run per context.

## Rules to satisfy (build-time checklist)

- [Bounded contexts must not directly access each other in the application layer (except allowed dependencies)](/rule/strategic/bounded-contexts-must-not-directly-access-each-other-in-application-layer-except-allowed-dependencies.md)
- [Incoming adapters must only access their own bounded context](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md)
- [Outgoing adapters accessing other contexts must only use OpenHostService classes](/rule/strategic/outgoing-adapters-accessing-other-contexts-must-only-use-openhostservice-classes-except-allowed-acl-patterns.md)
- [Shared Kernel must not have dependencies on any bounded context](/rule/strategic/shared-kernel-must-not-have-dependencies-on-any-bounded-context.md)
- [No technical bucket packages — package by domain concept](/rule/naming/no-technical-bucket-packages-package-by-domain-concept.md)
- [Domain packages must not have cyclic dependencies](/rule/cycles/domain-packages-must-not-have-cyclic-dependencies.md)

## Anchors

- Decision: [Pattern style per subdomain](/decision/pattern-style-per-subdomain.md)
- Markers: [@BoundedContext](/marker/strategic/boundedcontext.md) · [@SharedKernel](/marker/strategic/sharedkernel.md) · [@OpenHostService](/marker/strategic/openhostservice.md)
- ADRs: [ADR-011 Bounded Context Isolation](/adr/adr-011-bounded-context-isolation.md) · [ADR-025 Pattern Selection per Subdomain](/adr/adr-025-pattern-selection-per-subdomain.md) · [ADR-001 API/Web Package Separation](/adr/adr-001-api-web-package-separation.md)
- Book: [Identifying context boundaries](/book/10-bounded-contexts/identifying-context-boundaries.md) · [Subdomain types and pattern selection](/book/10-bounded-contexts/subdomain-types-and-pattern-selection.md) · [Cross-context communication](/book/10-bounded-contexts/cross-context-communication.md)
- Guide: [Java package structure](/guide/readme/java-package-structure.md)
- Then bootstrap the shared kernel and rule suite first if this is a greenfield app: [Bootstrap a new application](/recipe/bootstrap-a-new-application.md)
