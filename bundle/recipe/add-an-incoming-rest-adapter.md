---
type: Recipe
title: "Add an incoming REST adapter"
tags: [recipe, adapter, rest]
---

Expose a use case to the outside world through a primary (driving) adapter. A `*Resource` for a REST API, a `*PageController` for server-rendered web. The adapter is a thin edge: it calls an input port and maps the `Result` to a transport DTO — no business logic, no repository access.

## Steps

1. **Place it in `adapter/incoming/`** — REST resources under the api package, web controllers under the web package (they are separated on purpose — [Java package structure](/guide/readme/java-package-structure.md)).
2. **Name by role** — a REST endpoint class ends with `Resource`; an MVC class ends with `Controller` (a `*PageController`).
3. **Depend on the input port only** — inject the `{Name}InputPort`, build the `{Name}Command`/`{Name}Query` from the request, call `execute`. Never inject a repository or another adapter. Generate from the [REST resource template](/template/rest-resource.md).
4. **Map at the edge** — translate the use case `{Name}Result` into a `*Response` DTO (or a view model for web) in the adapter; DTOs and view models live here, never in domain or application. Handle an empty `Optional` result as the not-found case.
5. **Stay in your context** — an incoming adapter accesses only its own bounded context (event consumers and Open Host Services are the sanctioned exceptions).
6. **Verify** — `./gradlew test-architecture`.

## Rules to satisfy (build-time checklist)

- [REST controllers must end with `Resource`](/rule/naming/rest-controllers-must-end-with-resource-rest-best-practice.md)
- [Controller classes must end with `Controller`](/rule/naming/controller-classes-must-end-with-controller.md)
- [HTTP response models must end with `Response` and reside in the adapter incoming package](/rule/usecase/http-response-models-must-end-with-response-and-reside-in-adapter-incoming-package.md)
- [Controllers and resources must never access repositories directly](/rule/hexagonal/controllers-and-resources-must-never-access-repositories-directly.md)
- [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/incoming-adapters-must-only-use-outbound-ports-not-infrastructure-implementations.md)
- [Incoming adapters must only access their own bounded context](/rule/hexagonal/incoming-adapters-must-only-access-their-own-bounded-context-except-event-consumers-and-open-host-services.md)
- [DTOs must reside in the adapter package, not in domain or application](/rule/naming/dtos-must-reside-in-the-adapter-layer-not-in-domain-or-application.md)
- [View models must reside in adapter.incoming.web packages](/rule/naming/viewmodels-must-reside-in-adapter-incoming-web-packages.md)

## Anchors

- Pitfalls: [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md) · [CSRF-exempt API that accepts cookies](/pitfall/csrf-exempt-api-that-accepts-cookies.md)
- Template: [REST resource skeleton](/template/rest-resource.md) · AI-facing sibling: [MCP tool provider skeleton](/template/mcp-tool-provider.md)
- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Layer rules](/guide/readme/rules.md) · [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- The use case this adapter drives: [Add a use case](/recipe/add-a-use-case.md)
- Pitfalls: [Business logic in an adapter](/pitfall/business-logic-in-adapter.md) · [Exposing domain objects over REST](/pitfall/exposing-domain-objects-over-rest.md)
