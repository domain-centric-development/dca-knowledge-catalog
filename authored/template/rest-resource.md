---
type: Template
title: "REST resource skeleton (incoming adapter injecting input ports)"
tags: [template, adapter, rest]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/port-in/inputport.md, /marker/port-in/usecase.md, /rule/naming/dca-nam-006.md, /rule/hexagonal/dca-hex-003.md, /rule/hexagonal/dca-hex-004.md, /rule/naming/dca-nam-007.md, /guide/architecture-reference-guide/ports-and-adapters.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a REST resource: a primary (incoming) adapter that exposes use cases over HTTP. It lives in `adapter/incoming/api/`, is named `{Name}Resource`, depends only on **input port interfaces** (never on repositories or the domain directly), and maps each use case `Result` to a `*Response` record at the adapter edge. Request/response DTOs stay in the adapter package. Replace `{Name}` / `{usecasename}` / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`rest-resource/java.md`](/template/rest-resource/java.md)

## Realizes / governed by

- Markers: [InputPort](/marker/port-in/inputport.md) · [UseCase<INPUT, OUTPUT>](/marker/port-in/usecase.md)
- Rules: [REST controllers must end with 'Resource'](/rule/naming/dca-nam-006.md) · [Controllers and Resources must never access repositories directly](/rule/hexagonal/dca-hex-003.md) · [Incoming adapters must only use outbound ports, not infrastructure implementations](/rule/hexagonal/dca-hex-004.md) · [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Guide: [Ports and adapters](/guide/architecture-reference-guide/ports-and-adapters.md)
- Recipe: [Add an incoming REST adapter](/recipe/add-an-incoming-rest-adapter.md)
