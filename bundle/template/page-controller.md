---
type: Template
title: "Page controller skeleton (server-rendered web adapter)"
tags: [template, adapter, spring, use-case, security]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/naming/dca-nam-005.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-011.md, /rule/hexagonal/dca-hex-012.md, /rule/naming/dca-nam-011.md, /rule/usecase/dca-use-008.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a **page controller**: a primary (incoming) adapter that drives use cases from a server-rendered browser page. It lives in `adapter/incoming/web/`, is named `{Name}PageController`, and depends only on **input port interfaces** — never on a repository, a use-case class or a domain service. Reads are `@GetMapping` methods that map a query `*Result` to a page-specific [ViewModel](/template/view-model.md); every state change is a `@PostMapping` on a form record that answers with a `redirect:` (POST–redirect–GET). The page works without JavaScript: plain HTML forms, a CSRF token in each of them, validation messages rendered by the server. Replace `{Name}` / `{name}` / `{usecasename}` / `{context}` / `{basePackage}`.

This is the browser sibling of the [REST resource](/template/rest-resource.md): the same input ports, the same rule that the adapter converts at the edge and decides nothing, but the edge types are a form record and a ViewModel instead of a `*Request`/`*Response` pair.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`page-controller/java.md`](/template/page-controller/java.md)

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Rules: [Controller classes must end with 'Controller'](/rule/naming/dca-nam-005.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) · [Incoming Adapters must depend on input port interfaces, not on use case classes](/rule/hexagonal/dca-hex-011.md) · [Incoming Adapters must not depend on domain services](/rule/hexagonal/dca-hex-012.md) · [ViewModels must reside in adapter.incoming.web packages](/rule/naming/dca-nam-011.md) · [HTTP Response Models must end with 'Response' and reside in adapter incoming package](/rule/usecase/dca-use-008.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Guide: [Layer rules](/guide/rules.md) (input adapter rules, exception flow) · [Port placement](/guide/quick-reference/port-placement.md)
- Pitfalls: [State-changing GET endpoint](/pitfall/state-changing-get-endpoint.md) · [Business logic in adapter](/pitfall/business-logic-in-adapter.md)
- Related templates: [ViewModel](/template/view-model.md) · [Domain exception](/template/domain-exception.md) · [REST resource](/template/rest-resource.md)
