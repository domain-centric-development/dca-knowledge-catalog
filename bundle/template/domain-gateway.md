---
type: Template
title: "Domain Gateway skeleton (domain-owned port to external capability)"
tags: [template, domain, gateway]
---

Domain-free skeleton for a **Domain Gateway**: an interface declared in the *domain layer* that the domain itself (an aggregate, entity, or domain service) uses to consult an external fact or delegate a technology-bound operation — without coupling the domain to framework or infrastructure types. The **interface** lives in `{context}/domain/gateway/` and is framework-free; the **implementation** is a secondary (outgoing) adapter in `adapter/outgoing/`. It implements the `DomainGateway` marker. Distinct from an Output Port (which lives in the *application* layer and is used by use cases) and from a Repository (which persists aggregates): a Domain Gateway exposes an external *capability* (hashing, availability check, tax-rate lookup) consumed from inside the domain. Replace `{Name}` / `{context}` / `{basePackage}`.

## `{Name}.java` — domain gateway interface (domain layer)

```java
package {basePackage}.{context}.domain.gateway;

import {basePackage}.sharedkernel.marker.tactical.DomainGateway;

/**
 * Domain Gateway for {external capability, in the ubiquitous language}.
 *
 * <p>Owned by the domain and consulted by the aggregate / domain service to apply
 * a domain rule that needs an external fact or a technology-bound operation. The
 * interface is framework-free; the implementation lives in an outgoing adapter.
 */
public interface {Name} extends DomainGateway {

    {DomainResult} {operation}({DomainArgument} argument);
}
```

The contract speaks domain language and domain types only — no framework classes
in signatures. It is passed to the aggregate/domain service by the use case as a
typed parameter (DCA replaces the IDDD service-locator lookup with an explicit
argument), so the domain stays framework-free and unit-testable with a stub.

## `{Framework}{Name}.java` — outgoing adapter (implementation)

```java
package {basePackage}.{context}.adapter.outgoing.{technology};

import {basePackage}.{context}.domain.gateway.{Name};
import org.springframework.stereotype.Component;

/** Adapter implementing the domain gateway against {the concrete technology}. */
@Component
public class {Framework}{Name} implements {Name} {

    @Override
    public {DomainResult} {operation}(final {DomainArgument} argument) {
        // call the framework / external system, translate to domain types
    }
}
```

The Spring stereotype sits on the *adapter*, never on the domain interface. The
adapter is the only place framework and external-system types appear; letting any
of them into the domain interface is a [framework-leak-in-domain](/pitfall/framework-leak-in-domain.md).

## Realizes / governed by

- Marker: [DomainGateway](/marker/tactical/domaingateway.md) — a domain-layer port, no dedicated ArchUnit rule yet
- Book/Guide: [Ansatz 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/ansatz-1-domaingateway-pattern.md) · [ArchUnit Governance](/guide/domain-services-with-data-dependencies/archunit-governance.md)
- Decisions: [Cross-context communication: synchronous call or integration event](/decision/cross-context-communication.md) — the ACL / gateway option
- Pitfall: [Framework leak in domain](/pitfall/framework-leak-in-domain.md)
- Recipe: [Add an anti-corruption layer](/recipe/add-an-anti-corruption-layer.md)
- Related template: [Domain Service](/template/domain-service.md) — pure domain logic without external facts
