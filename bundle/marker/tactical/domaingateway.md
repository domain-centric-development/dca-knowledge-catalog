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
uses to obtain facts it does not hold, or to delegate a technology-bound computation, without
coupling the domain to framework or infrastructure types. The implementation lives outside the
domain (typically in an outgoing adapter), but the contract is owned by the domain and expressed
in domain language.

**It never writes to the outside.** A gateway enriches the model with information so that
the model can decide; it does not change the state of any external system. Persisting, sending,
publishing and calling a remote operation that has an effect are the application's business,
through an output port. A computation that touches nothing outside the process — hashing a
password, converting a currency with a supplied rate — is a gateway, because no external state
changes.

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
- Read-only towards the outside: no external state is created, changed or removed

**Example use cases:**

- Password hashing/verification (`PasswordHasher`)
- Shipping availability checks during `Order.confirm()`
- Tax rate lookup when the aggregate computes totals

**Reference:** The pattern follows Vaughn Vernon's IDDD (2013) sample code (`iddd_identityaccess`, `User` aggregate using `EncryptionService` via the `DomainRegistry`), generalized as a typed marker rather than a service locator.

## Related mentions in guides (heuristic)

- [Approach 1: DomainGateway Pattern](/guide/domain-services-with-data-dependencies/approach-1-domaingateway-pattern.md)
- [ArchUnit Governance](/guide/domain-services-with-data-dependencies/archunit-governance.md)
