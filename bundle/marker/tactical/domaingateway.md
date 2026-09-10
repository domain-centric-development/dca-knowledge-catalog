---
type: Marker
title: DomainGateway
category: tactical
kind: interface
signature: public interface DomainGateway
package: dev.domaincentric.dca.buildingblocks.ddd.tactical
resource: dca-java/dca-building-blocks/src/main/java/dev/domaincentric/dca/buildingblocks/ddd/tactical/DomainGateway.java
tags: [tactical, marker]
---

Marker interface for Domain Gateways.

A Domain Gateway is an interface declared in the **domain layer** that the domain itself
uses to consult external facts or delegate technology-bound operations, without coupling the
domain to framework or infrastructure types. The implementation lives outside the domain
(typically in an outgoing adapter), but the contract is owned by the domain and expressed in
domain language.

**How it differs from related concepts:**

- **vs Domain Service** — A `e` contains pure domain logic; both
interface and implementation live in the domain layer (framework-free). A Domain Gateway is
a *port* to the outside world; only the interface is in the domain.
- **vs Output Port** — An Output Port (see `OutputPort`) lives in the application
layer and is used by use cases. A Domain Gateway lives in the domain layer and is used by
aggregates, entities, or domain services to enforce invariants or perform domain-bound
operations.
- **vs Repository** — A Repository persists and reconstitutes aggregates. A Domain Gateway
exposes external capability (cryptography, availability check, geocoding, …).

**Characteristics:**

- Interface in the domain layer (`{context`/domain/gateway/})
- No framework dependencies in the interface
- Implementation in the outgoing adapter layer
- Typically called by aggregates, entities, or domain services
- Side-effect-free or read-only operations are the typical case

**Example use cases:**

- Password hashing/verification (`PasswordHasher`)
- Shipping availability checks during `Order.confirm()`
- Tax rate lookup when the aggregate computes totals

**Reference:** The pattern follows Vaughn Vernon's IDDD (2013) sample code (`iddd_identityaccess`, `User` aggregate using `EncryptionService` via the `DomainRegistry`), generalized as a typed marker rather than a service locator.

## Related mentions in guides (heuristic)

- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [ArchUnit Governance](/guide/domain-services-with-data-dependencies/archunit-governance.md)
