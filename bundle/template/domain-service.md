---
type: Template
title: "Domain Service skeleton (stateless multi-aggregate domain logic)"
tags: [template, domain, domain-service]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainservice.md, /rule/advanced/dca-adv-009.md, /rule/advanced/dca-adv-010.md, /rule/advanced/dca-adv-011.md, /rule/advanced/dca-adv-012.md, /guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md, /guide/architecture-reference-guide/framework-annotations-rules.md, /guide/readme/elements.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **Domain Service**: a stateless operation in the domain layer that expresses domain logic which doesn't naturally belong to a single Entity or Value Object — typically because it spans multiple aggregates or value objects. It implements the `DomainService` marker, carries **no** Spring annotation, holds no state (only `final` fields for injected collaborators), and is instantiated by an application service / use case. Name it after the activity in the ubiquitous language (`{Name}Calculator`, `{Name}Policy`, `{Name}Validator`), never `{Name}Manager`/`Helper`/`Service` as a technical bucket. Replace `{Name}` / `{context}` / `{basePackage}` and the value-object types.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-service/java.md`](/template/domain-service/java.md)

## Realizes / governed by

- Marker: [DomainService](/marker/tactical/domainservice.md)
- Rules: [Domain Services must implement DomainService Marker Interface and reside in domain.service](/rule/advanced/dca-adv-009.md) · [Domain Services must reside in domain package](/rule/advanced/dca-adv-010.md) · [Domain Services must not have Spring annotations](/rule/advanced/dca-adv-011.md) · [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/dca-adv-012.md)
- Guide: [Pure domain services](/guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md) · [Framework annotation rules](/guide/architecture-reference-guide/framework-annotations-rules.md) · [Layer elements](/guide/readme/elements.md)
- Decisions: [Where does the logic live](/decision/where-does-the-logic-live.md)
- Related template: [Domain Gateway](/template/domain-gateway.md) — when the service needs external facts
