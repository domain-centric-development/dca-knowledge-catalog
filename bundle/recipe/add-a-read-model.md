---
type: Recipe
title: "Add a read model"
tags: [recipe, application, cqrs, use-case, value-object]
---

Build a view for a query without going through the full aggregate write journey. A read model is *shaping data for a reader*, not modelling behaviour — so it deliberately sidesteps commands, invariants-that-mutate, and event publishing. This recipe binds two skeletons together: the [enriched domain model](/template/enriched-domain-model.md) (a Value Object that combines aggregate state with cross-context data and owns cross-context read rules) and the [ViewModel](/template/view-model.md) (a primitive-only presentation record at the adapter edge). It tells you **which to build, when, and in what order** — the *how the read is produced* question is decided first in [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md).

## Steps

1. **Decide the read strategy first.** Run [read-model-vs-domain-query](/decision/read-model-vs-domain-query.md). The default is a **plain query use case over the domain repository** — start there for every read. Escalate to a dedicated CQRS read side only on a proven read/write skew, reporting need, or multiple read representations, and even then pick the lowest CQRS level that solves it. This recipe covers the read *shape*; that decision covers the read *machinery*.
2. **Write the query use case.** An `application/{usecasename}/` folder with a `{Name}Query`, a `{Name}Result`, and a use case that loads via the aggregate's repository and maps to the result. Build it with [Add a use case](/recipe/add-a-use-case.md) on the read/`Query` path. Queries end with `Query`, results end with `Result`, both live in the application package.
3. **Does the read need data from another context?** If the view must show aggregate state *together with* data owned elsewhere (current price from Pricing, stock from Inventory), or must apply a business rule that spans contexts, build an **enriched domain model** from the [enriched-domain-model template](/template/enriched-domain-model.md): a `record Enriched{Name} implements Value` in `{context}.domain.model/`, assembled by a static factory that takes the aggregate plus a plain carrier of the external data. Fetch that external data through the consumer's **own output port** (never import the other context) — see [Cross-context communication](/decision/cross-context-communication.md). The enriched model has **no identity, no lifecycle, raises no events**; it owns only the cross-context read rules. If the read stays inside one context, skip this step — the plain `Result` is enough.
4. **Map to a ViewModel at the adapter edge.** For a server-rendered page, transform the `Result` (or the enriched model) into a `{Page}PageViewModel` of **primitives only** in `{context}/adapter/incoming/web/`, using the [ViewModel template](/template/view-model.md). For a REST API the sibling is a `*Response` DTO ([Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)). Domain types (`Money`, typed ids, the enriched model) must never reach a template.
5. **Wire the controller thin.** The controller calls the input port, receives the `Result`, converts it to the ViewModel, and hands primitives to the template — no formatting or cross-context logic beyond primitive mapping.
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [Queries must end with `Query` and reside in the application package](/rule/usecase/use-case-queries-must-end-with-query-and-reside-in-application-package.md)
- [Result models must end with `Result` and reside in the application package](/rule/usecase/use-case-result-models-must-end-with-result-and-reside-in-application-package.md)
- [Enriched domain models must be Value Object records](/rule/tactical/enriched-domain-models-must-be-value-object-records.md)
- [Value objects must not contain aggregate roots or entities](/rule/tactical/value-objects-must-not-contain-aggregate-roots-or-entities.md)
- [View models must reside in adapter.incoming.web packages](/rule/naming/viewmodels-must-reside-in-adapter-incoming-web-packages.md)
- [DTOs must reside in the adapter package, not in domain or application](/rule/naming/dtos-must-reside-in-portadapter-package-not-in-domain-or-application.md)

## Anchors

- Templates: [Enriched domain model](/template/enriched-domain-model.md) · [ViewModel](/template/view-model.md) · [REST resource](/template/rest-resource.md)
- Decisions: [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md) · [Cross-context communication](/decision/cross-context-communication.md)
- Markers: [Value](/marker/tactical/value.md) · [UseCase&lt;INPUT, OUTPUT&gt;](/marker/port-in/usecase.md) · [Repository&lt;T, ID&gt;](/marker/port-out/repository.md)
- ADRs: [ADR-021 Enriched Domain Model Pattern](/adr/adr-021-enriched-domain-model-pattern.md) · [ADR-022 ViewModel Pattern for Web Adapters](/adr/adr-022-viewmodel-pattern.md)
- Book: [When to Use CQRS](/book/16-cqrs-patterns/when-to-use-cqrs.md) · [CQRS Levels](/book/16-cqrs-patterns/cqrs-levels.md) · [Read Model Projections](/book/16-cqrs-patterns/read-model-projections.md) · [Common Patterns — Enriched Read Model](/book/10-bounded-contexts/common-patterns.md)
- Guide: [Integration Patterns](/guide/readme/integration-patterns.md)
- Related recipes: [Add a use case](/recipe/add-a-use-case.md) · [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
