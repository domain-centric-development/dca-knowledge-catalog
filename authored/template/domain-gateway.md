---
type: Template
title: "Domain Gateway skeleton (domain-owned port to external capability)"
tags: [template, domain, gateway]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domaingateway.md, /guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md, /guide/domain-services-with-data-dependencies/archunit-governance.md]
applies_to: [java]
framework: [spring]
---

Domain-free skeleton for a **Domain Gateway**: an interface declared in the *domain layer* that the domain itself (an aggregate, entity, or domain service) uses to consult an external fact or delegate a technology-bound operation — without coupling the domain to framework or infrastructure types. The **interface** lives in `{context}/domain/gateway/` and is framework-free; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/`. It implements the `DomainGateway` marker. Distinct from an Output Port (which lives in the *application* layer and is used by use cases) and from a Repository (which persists aggregates): a Domain Gateway exposes an external *capability* (hashing, availability check, tax-rate lookup) consumed from inside the domain. Replace `{Name}` / `{context}` / `{basePackage}`.

## Languages

The code lives in one child node per language, so the prose below is written once and a
further language is one more file rather than a second copy of this node.

- Java — [`domain-gateway/java.md`](/template/domain-gateway/java.md)

## Realizes / governed by

- Marker: [DomainGateway](/marker/tactical/domaingateway.md) — a domain-layer port, no dedicated ArchUnit rule yet
- Book/Guide: [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md) · [ArchUnit Governance](/guide/domain-services-with-data-dependencies/archunit-governance.md)
- Decisions: [Cross-context communication: synchronous call or integration event](/decision/cross-context-communication.md) — the ACL / gateway option
- Pitfall: [Framework leak in domain](/pitfall/framework-leak-in-domain.md)
- Recipe: [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)
- Related template: [Domain Service](/template/domain-service.md) — pure domain logic without external facts
