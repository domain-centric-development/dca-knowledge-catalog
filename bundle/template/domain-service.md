---
type: Template
title: "Domain Service skeleton (stateless multi-aggregate domain logic)"
tags: [template, domain, domain-service]
---

Domain-free skeleton for a **Domain Service**: a stateless operation in the domain layer that expresses domain logic which doesn't naturally belong to a single Entity or Value Object — typically because it spans multiple aggregates or value objects. It implements the `DomainService` marker, carries **no** Spring annotation, holds no state (only `final` fields for injected collaborators), and is instantiated by an application service / use case. Name it after the activity in the ubiquitous language (`{Name}Calculator`, `{Name}Policy`, `{Name}Validator`), never `{Name}Manager`/`Helper`/`Service` as a technical bucket. Replace `{Name}` / `{context}` / `{basePackage}` and the value-object types.

## `{Name}Calculator.java` — domain service (domain layer)

```java
package {basePackage}.{context}.domain.service;

import {basePackage}.{context}.domain.{concept}.{ValueObject};
import {basePackage}.sharedkernel.marker.tactical.DomainService;

/**
 * Domain Service for {activity phrased in the ubiquitous language}.
 *
 * <p>Encapsulates domain logic that spans multiple domain objects and does not
 * belong inside a single aggregate. Stateless and framework-free.
 */
public final class {Name}Calculator implements DomainService {

    public {ResultValueObject} calculate(final {ValueObject} first, final {ValueObject} second) {
        // pure domain logic over the passed-in value objects / aggregates;
        // no I/O, no persistence, no framework calls — return a domain result
    }
}
```

The class is `final`, has no `@Service`/`@Component`, and never reaches out to a
repository or the framework itself. If it needs data it doesn't own, the use case
resolves that data first and passes it in as value objects (the *pure domain
service* default), or the service consults a [DomainGateway](/template/domain-gateway.md)
whose implementation lives in an adapter. A domain service with only `final`
dependency fields stays stateless.

## Wiring — instantiated by the use case (application layer)

```java
// inside a *UseCase in {basePackage}.{context}.application.{usecase}:
private final {Name}Calculator calculator = new {Name}Calculator();

// or, if it has domain-gateway dependencies, construct it with them there.
```

The use case owns the service's lifecycle. Because the service carries no Spring
stereotype, it is created explicitly rather than injected — which keeps the whole
domain layer wireable without a container and unit-testable with plain `new`.

## Realizes / governed by

- Marker: [DomainService](/marker/tactical/domainservice.md)
- Rules: [Domain Services must implement DomainService Marker Interface and reside in domain.service](/rule/advanced/domain-services-must-implement-domainservice-marker-interface-and-reside-in-domain-service.md) · [Domain Services must reside in domain package](/rule/advanced/domain-services-must-reside-in-domain-package.md) · [Domain Services must not have Spring annotations](/rule/advanced/domain-services-must-not-have-spring-annotations.md) · [Domain Services should be stateless (only final fields for dependencies)](/rule/advanced/domain-services-should-be-stateless-only-final-fields-for-dependencies.md)
- ADRs: [ADR-010 Domain Services Only for Multi-Aggregate Operations](/adr/adr-010-domain-services-multi-aggregate.md) · [ADR-002 Framework-Independent Domain Layer](/adr/adr-002-framework-independent-domain.md)
- Book: [Tactical Building Blocks](/book/05-domain-layer/tactical-building-blocks.md)
- Decisions: [Where does the logic live](/decision/where-does-the-logic-live.md)
- Related template: [Domain Gateway](/template/domain-gateway.md) — when the service needs external facts
