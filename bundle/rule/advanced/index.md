# advanced

- [Domain Events must have a timestamp field](domain-events-must-have-a-timestamp-field.md) — An event records something that happened — without a timestamp the fact cannot be ordered, replayed or audited.
- [Domain Events must implement DomainEvent Marker Interface and be records](domain-events-must-implement-domainevent-marker-interface-and-be-records.md) — Domain events should be immutable records implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCl...
- [Domain Events must not have Spring annotations](domain-events-must-not-have-spring-annotations.md) — Domain events must be framework-independent POJOs.
- [Domain Events must reside in domain package](domain-events-must-reside-in-domain-package.md) — Domain events are part of the domain layer (named in past tense).
- [Domain Events should be immutable (final or records)](domain-events-should-be-immutable-final-or-records.md) — Domain events should be immutable (final classes or records).
- [Domain Events that are not Integration Events must not have a version field](domain-events-that-are-not-integration-events-must-not-have-a-version-field.md) — Versioning is a contract concern of integration events — a purely internal domain event has no wire contract to version.
- [Domain Services must implement DomainService Marker Interface and reside in domain.service](domain-services-must-implement-domainservice-marker-interface-and-reside-in-domain-service.md) — Domain services implement DomainService marker and reside in domain.service packages (named descriptively, e.g., Pric...
- [Domain Services must not have Spring annotations](domain-services-must-not-have-spring-annotations.md) — Domain services should be framework-independent.
- [Domain Services must reside in domain package](domain-services-must-reside-in-domain-package.md) — Domain services are part of the domain layer, not application layer.
- [Domain Services should be stateless (only final fields for dependencies)](domain-services-should-be-stateless-only-final-fields-for-dependencies.md) — Domain services should be stateless (only final fields for dependencies).
- [Factories must not have Spring annotations](factories-must-not-have-spring-annotations.md) — Factories should be framework-independent.
- [Factories must reside in domain package](factories-must-reside-in-domain-package.md) — Factories are part of the domain layer (complex aggregate creation logic).
- [Factories should be stateless (only final fields for dependencies)](factories-should-be-stateless-only-final-fields-for-dependencies.md) — Factories should be stateless (only final fields for dependencies).
- [Factories should implement Factory Marker Interface](factories-should-implement-factory-marker-interface.md) — Classes implementing Factory marker should have 'Factory' in their name.
- [Integration Events must be annotated with IntegrationEventType](integration-events-must-be-annotated-with-integrationeventtype.md) — @IntegrationEventType(name, version) is the contract identity of every integration event — the serializer keys (name,...
- [Integration Events must not have a version field](integration-events-must-not-have-a-version-field.md) — The schema version is a class property (@IntegrationEventType), never per-instance payload data — a version data fiel...
- [Specifications must end with 'Specification'](specifications-must-end-with-specification.md) — Specification implementations are part of the domain layer.
- [Specifications must not have Spring annotations](specifications-must-not-have-spring-annotations.md) — Specifications should be framework-independent value objects.
