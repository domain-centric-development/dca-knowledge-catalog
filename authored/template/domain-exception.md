---
type: Template
title: Domain exception skeleton
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/readme/rules.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **domain exception**: a business-rule violation expressed as an unchecked, framework-free exception in the domain package, named in the ubiquitous language. Two shapes cover most cases — `{Name}NotFound`, carrying the typed id that was asked for, and `{Rule}Violated`, carrying the facts the rule compared. The aggregate (or a domain service) throws it when an invariant would break; a use case throws the not-found variant when a lookup comes back empty; only the incoming adapter catches it and maps it to the transport — a 404 view, a `ProblemDetail`, a rejected message. Replace `{Name}` / `{Rule}` / `{name}` / `{context}` / `{basePackage}`. The domain layer is framework-free — no Spring, no HTTP status, no `@ResponseStatus`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-exception/java.md`](/template/domain-exception/java.md)

## Realizes / governed by

- Rules: [Domain classes must not use technical suffixes](/rule/naming/dca-nam-010.md) · [The Domain Model should be framework independent](/rule/onion/dca-oni-002.md)
- Guide: [Layer rules](/guide/readme/rules.md) (exception layer placement, exception flow pattern)
- Pitfall: [Framework leak in domain](/pitfall/framework-leak-in-domain.md)
- Related templates: [Aggregate root](/template/aggregate-root.md) · [Page controller](/template/page-controller.md) · [REST resource](/template/rest-resource.md)
