---
type: Template
title: Domain exception skeleton
tags: [template, domain, naming]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainexception.md, /marker/application/portexception.md, /marker/application/inputportexception.md, /marker/application/usecaseexception.md, /marker/application/outputportexception.md, /marker/application/refusal.md, /rule/errors/dca-err-001.md, /rule/errors/dca-err-002.md, /rule/errors/dca-err-003.md, /rule/errors/dca-err-008.md, /rule/errors/dca-err-005.md, /rule/naming/dca-nam-010.md, /rule/onion/dca-oni-002.md, /guide/rules.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for the failures the inner layers raise, each with the base class its layer owns. `{Rule}Violated` extends `DomainException` and lives in the domain package: the aggregate (or a domain service) raises it when a behaviour method would break an invariant, and it carries the facts the rule compared. `{Name}NotFound` extends `UseCaseException` and lives beside the use case: the request addressed something that is not there, which is a statement about the request, not about the model. `Duplicate{Name}` extends `OutputPortException` and lives beside the output port whose contract declares it: the adapter throws it, the use case catches it. Replace `{Name}` / `{Rule}` / `{name}` / `{operation}` / `{context}` / `{basePackage}`. No type carries a framework annotation, a status code or a message shape.

The hierarchy: `DomainException` and the abstract `PortException` extend the platform's runtime exception; under `PortException` sit the abstract `InputPortException` — declared by an input port, caught by its caller, with `UseCaseException` under it, thrown only by a use case — and the abstract `OutputPortException`, declared by an output port, thrown by its adapter, caught by the use case.

A concrete use-case failure extends `UseCaseException`, never `InputPortException` directly, and no incoming adapter catches `PortException` or `InputPortException` generically. A failure of the system's own infrastructure — its database lost the connection, its broker timed out — is no `OutputPortException`; it stays the platform's exception. A foreign system behind an output port — an external system on the context map — that refuses, times out or cannot be reached is: the port declares `{System}UnavailableException` as an `OutputPortException`, the adapter throws it, and the use case answers it as a refusal — its own use-case exception where the context throws, a case of its result where it returns.

An expected refusal travels one of two equal ways, chosen per bounded context. **Thrown:** `{Name}NotFound` is the use-case exception above, the model's `{Rule}Violated` passes through, and the context's exception handler answers both. **Returned:** `{Rule}Violated` stays as it is, the use case catches it once and returns its case; `{Name}NotFound` is no exception but a case of the use case's sealed result, marked `Refusal` — see [Return expected refusals as a sealed result](/recipe/return-expected-refusals-as-a-sealed-result.md). The Java node shows both.

An argument guard is none of this: a null check or a range check on a value only code passes states a contract for the caller, and the platform's own argument exception stays correct there. A value built from input refuses null and its bounds with the rule's named failure instead — the origin of the value decides. The test for a domain exception is the name — if a domain expert has a word for the failure, it is one.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-exception/java.md`](/template/domain-exception/java.md)

## Realizes / governed by

- Markers: [DomainException](/marker/tactical/domainexception.md) · [PortException](/marker/application/portexception.md) · [InputPortException](/marker/application/inputportexception.md) · [UseCaseException](/marker/application/usecaseexception.md) · [OutputPortException](/marker/application/outputportexception.md) · [Refusal](/marker/application/refusal.md)
- Rules: [Exceptions declared in the domain layer must extend DomainException](/rule/errors/dca-err-001.md) · [Domain and port exceptions reside in the layer whose failure they name](/rule/errors/dca-err-002.md) · [Exceptions declared in the application layer must extend UseCaseException or OutputPortException](/rule/errors/dca-err-003.md) · [Diagnostic: closed use-case results without a case marked as a refusal](/rule/errors/dca-err-008.md) · [Exception names must stay in the language of their layer](/rule/errors/dca-err-005.md) · [The Domain Model should be framework independent](/rule/onion/dca-oni-002.md)
- Guide: [Layer rules](/guide/rules.md) (exception layer placement, exception flow pattern)
- Pitfall: [Framework leak in domain](/pitfall/framework-leak-in-domain.md) · [A business rule reported as an argument error](/pitfall/business-rule-reported-as-an-argument-error.md)
- Decision: [Failure channel: exception or a case of the use case's result](/decision/failure-channel-exception-or-result.md)
- Recipe: [Return expected refusals as a sealed result](/recipe/return-expected-refusals-as-a-sealed-result.md)
- Related templates: [Aggregate root](/template/aggregate-root.md) · [Page controller](/template/page-controller.md) · [REST resource](/template/rest-resource.md)
