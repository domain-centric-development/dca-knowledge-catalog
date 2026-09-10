---
type: Template
title: "ViewModel skeleton (page-specific, primitive-only presentation record)"
tags: [template, adapter, dto]
review: draft
owner: DCA catalog maintainers
evidence: [/guide/readme/java-package-structure.md, /guide/readme/rules.md, /rule/naming/dca-nam-007.md]
applies_to: [java]
framework: [framework-neutral]
---

Domain-free skeleton for a **ViewModel**: a page-specific record that transforms a domain read model (or a use-case `Result`) into **primitives only** for a server-rendered template. It lives in the adapter layer at `{context}/adapter/incoming/web/`, is named `{Page}PageViewModel`, and is built by a **static factory** that maps domain types (`Money`, `{Name}Id`, enriched models) to `String` / `BigDecimal` / `int` / `boolean`. Its job is to stop domain types leaking into templates and to keep presentation formatting out of the application layer. One ViewModel **per page**, carrying exactly that page's fields — not one reusable model shared across pages. Replace `{Page}` / `{context}` / `{basePackage}`.

This is the web/MVC sibling of the API `*Response` DTO in the [REST resource template](/template/rest-resource.md): both are edge DTOs mapped from a `Result`, but a `Response` serialises to JSON for an API client while a ViewModel feeds a template. Keep the three layers distinct: `Result` (application) → ViewModel (web adapter) → DTO/`Response` (api adapter).

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`view-model/java.md`](/template/view-model/java.md)

## Realizes / governed by

- Guide: [Java package structure](/guide/readme/java-package-structure.md) · [Layer rules](/guide/readme/rules.md)
- Rule: [DTOs must reside in the adapter layer, not in domain or application](/rule/naming/dca-nam-007.md)
- Related templates: [Enriched domain model](/template/enriched-domain-model.md) · [REST resource](/template/rest-resource.md)
- Related decision: [Plain query use case or a dedicated read model](/decision/read-model-vs-domain-query.md)
