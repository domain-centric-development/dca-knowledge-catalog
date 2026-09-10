---
type: Template
title: "Domain Gateway skeleton (domain-owned port to external capability) — Java"
parent: /template/domain-gateway.md
tags: [template, domain, gateway]
review: draft
owner: DCA catalog maintainers
evidence: [/marker/tactical/domaingateway.md, /guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md, /guide/domain-services-with-data-dependencies/archunit-governance.md]
applies_to: [java]
framework: [spring]
---

The Java code of [Domain Gateway skeleton (domain-owned port to external capability)](/template/domain-gateway.md). The prose, the evidence and what
governs it stay in that node; this file carries the skeleton only.

## `{Name}.java` — domain gateway interface (domain layer)

```java
package {basePackage}.{context}.domain.gateway;

import dev.domaincentric.dca.buildingblocks.ddd.tactical.DomainGateway;

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
