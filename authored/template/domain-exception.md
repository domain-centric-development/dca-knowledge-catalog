---
type: Template
title: Domain exception skeleton
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-005.md, /rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/rules.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for the two failures an inner layer raises, each with the base class its layer owns. `{Rule}Violated` extends `DomainException` and lives in the domain package: the aggregate (or a domain service) raises it when a behaviour method would break an invariant, and it carries the facts the rule compared. `{Name}NotFound` extends `UseCaseException` and lives beside the use case: the request addressed something that is not there, which is a statement about the request, not about the model. Only the incoming adapter catches either, and it alone decides the answer — a 404 view, a `ProblemDetail`, a rejected message. Replace `{Name}` / `{Rule}` / `{name}` / `{operation}` / `{context}` / `{basePackage}`. Neither type carries a framework annotation, a status code or a message shape.

An argument guard is none of this: a null check or a range check in a constructor states a contract for the caller, and the platform's own argument exception stays correct there. The test for a domain exception is the name — if a domain expert has a word for the failure, it is one.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-exception/java.md`](/template/domain-exception/java.md)

## Realizes / governed by

- Rules: [Exceptions declared in the domain layer must extend DomainException](/rule/errors/dca-err-001.md) · [Domain and use-case exceptions reside in the layer whose failure they name](/rule/errors/dca-err-002.md) · [Exceptions declared in the application layer must extend UseCaseException](/rule/errors/dca-err-003.md) · [Exception names must stay in the language of their layer](/rule/errors/dca-err-005.md) · [The Domain Model should be framework independent](/rule/onion/dca-oni-002.md)
- Guide: [Layer rules](/guide/rules.md) (exception layer placement, exception flow pattern)
- Pitfall: [Framework leak in domain](/pitfall/framework-leak-in-domain.md) · [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md)
- Decision: [Failure channel: exception or a closed set of result variants](/decision/failure-channel-exception-or-result.md)
- Related templates: [Aggregate root](/template/aggregate-root.md) · [Page controller](/template/page-controller.md) · [REST resource](/template/rest-resource.md)
