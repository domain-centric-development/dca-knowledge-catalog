---
type: Template
title: "Domain Service skeleton (stateless multi-aggregate domain logic) — Java"
parent: /template/domain-service.md
tags: [template, domain, domain-service]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domainservice.md, /rule/advanced/dca-adv-009.md, /rule/advanced/dca-adv-010.md, /rule/advanced/dca-adv-011.md, /rule/advanced/dca-adv-012.md, /guide/domain-services-with-data-dependencies/default-rule-pure-domain-services-90-of-cases.md, /guide/architecture-reference-guide/framework-annotations-rules.md, /guide/readme/elements.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Domain Service skeleton (stateless multi-aggregate domain logic)](/template/domain-service.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}Calculator.java` — domain service (domain layer)

```java
package {basePackage}.{context}.domain.service;

import {basePackage}.{context}.domain.{concept}.{ValueObject};
import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainService;

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
