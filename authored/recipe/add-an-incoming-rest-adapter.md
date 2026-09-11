---
type: Recipe
title: Add an incoming REST adapter
tags: [recipe, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/package-structure.md, /rule/naming/dca-nam-006.md, /rule/naming/dca-nam-005.md, /rule/usecase/dca-use-008.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-004.md, /rule/hexagonal/dca-hex-007.md, /rule/naming/dca-nam-007.md]
---

Expose a use case to the outside world through a primary (driving) adapter. A `*Resource` for a REST API, a `*PageController` for server-rendered web. The adapter is a thin edge: it calls an input port and maps the `Result` to a transport DTO — no business logic, no repository access.

## Steps

1. **Place it in `adapter/incoming/`** — REST resources under the api package, web controllers under the web package (they are separated on purpose — [Java package structure](/guide/package-structure.md)).
2. **Name by role** — a REST endpoint class ends with `Resource`; an MVC class ends with `Controller` (a `*PageController`).
3. **Depend on the input port only** — inject the `{Name}InputPort`, build the `{Name}Command`/`{Name}Query` from the request, call `execute`. Never inject a repository or another adapter. Generate from the [REST resource template](/template/rest-resource.md).
4. **Map at the edge** — translate the use case `{Name}Result` into a `*Response` DTO (or a view model for web) in the adapter; DTOs and view models live here, never in domain or application. Handle an empty `Optional` result as the not-found case.
5. **Stay in your context** — an incoming adapter accesses only its own bounded context (event consumers and Open Host Services are the sanctioned exceptions).
6. **Verify** — the project's architecture suite (`./gradlew test-architecture`, or `dotnet test -c Debug` against the architecture-test project).

## Server-rendered page instead of REST

The same recipe with a different edge. A `{Name}PageController` in `adapter/incoming/web/` depends on the same input ports; what changes is the shape of what goes in and out:

- **View models instead of `*Response`** — the controller maps the `{Name}Result` to a view model that carries exactly what the template renders (formatted amounts, labels, flags), placed next to the controller ([ViewModel](/template/view-model.md)). Templates never see a `Result`, let alone an aggregate.
- **POST + redirect for every state change** — a command use case is reached only from a form submitted with `POST`; the handler redirects to a `GET` page afterwards. A link that changes state is the pitfall [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md).
- **Form records validated in the adapter** — the request binds to a `{Name}Form` record with bean-validation annotations; the adapter checks it, re-renders the page with errors on failure, and builds the `{Name}Command` from it on success. Business rules still live in the domain — the form validates shape, not meaning.
- **Name and place** — the class ends with `Controller`, lives under the web package, and never touches a repository. Generate from the [page controller template](/template/page-controller.md).

## Rules to satisfy (build-time checklist)

- [REST controllers must end with `Resource`](/rule/naming/dca-nam-006.md)
- [Controller classes must end with `Controller`](/rule/naming/dca-nam-005.md)
- [HTTP response models must end with `Response` and reside in the adapter incoming package](/rule/usecase/dca-use-008.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md)
- [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md)
- [Incoming adapters must only access their own bounded context](/rule/hexagonal/dca-hex-007.md)
- [DTOs must reside in the adapter package, not in domain or application](/rule/naming/dca-nam-007.md)
- [View models must reside in adapter.incoming.web packages](/rule/naming/dca-nam-011.md)

## Anchors

- Pitfalls: [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md) · [CSRF-exempt API that accepts cookies](/pitfall/csrf-exempt-api-that-accepts-cookies.md)
- Template: [REST resource skeleton](/template/rest-resource.md) · web sibling: [Page controller](/template/page-controller.md) with [ViewModel](/template/view-model.md) · AI-facing sibling: [MCP tool provider skeleton](/template/mcp-tool-provider.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Guide: [Java package structure](/guide/package-structure.md) · [Layer rules](/guide/rules.md) · [Port placement](/guide/quick-reference/port-placement.md)
- The use case this adapter drives: [Add a use case](/recipe/add-a-use-case.md)
- Pitfalls: [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Exposing domain objects over REST](/pitfall/exposing-domain-objects-over-rest.md)
