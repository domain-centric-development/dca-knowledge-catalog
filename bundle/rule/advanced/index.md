# advanced

- [Domain Events must implement DomainEvent and have immutable shape](dca-adv-001.md) — Domain events should have immutable state implementing DomainEvent (named in past tense, e.g., ProductCreated, CartCl...
- [Domain Events must reside in domain package](dca-adv-002.md) — Domain events are part of the domain layer (named in past tense).
- [Domain events must not carry prohibited framework metadata](dca-adv-004.md) — Domain objects carry no metadata for container management, persistence or transaction coordination.
- [Integration Events must be annotated with IntegrationEventType](dca-adv-005.md) — @IntegrationEventType(name, version) is the contract identity of every integration event — the serializer keys (name,...
- [Integration events carry the schema version in their type metadata, not in the payload](dca-adv-006.md) — The schema version is a class property (@IntegrationEventType), never per-instance payload data — an explicit schema-...
- [Domain events that are not integration events carry no schema version](dca-adv-007.md) — Versioning is a contract concern of integration events — a purely internal domain event has no wire contract to version.
- [Domain Events must have a timestamp field](dca-adv-008.md) — An event records something that happened — without a timestamp the fact cannot be ordered, replayed or audited.
- [Marked domain services reside in a module domain](dca-adv-010.md) — Domain services are part of the domain layer, not application layer.
- [Domain services must not carry prohibited framework metadata](dca-adv-011.md) — Domain objects carry no metadata for container management, persistence or transaction coordination.
- [Domain Services should be stateless (only final fields for dependencies)](dca-adv-012.md) — Domain services should be stateless (only final fields for dependencies).
- [Types carrying the factory role are named *Factory](dca-adv-013.md) — A factory is found by its role, and read by its name: a type that creates aggregates and is not called one makes the ...
- [Factories must reside in domain package](dca-adv-014.md) — Factories are part of the domain layer (complex aggregate creation logic).
- [Factories must not carry prohibited framework metadata](dca-adv-015.md) — Domain objects carry no metadata for container management, persistence or transaction coordination.
- [Factories should be stateless (only final fields for dependencies)](dca-adv-016.md) — Factories should be stateless (only final fields for dependencies).
- [Specifications reside in the domain layer](dca-adv-017.md) — A specification is a rule of the model expressed as a predicate; it belongs where the model is, not in the layer that...
- [Specifications must not carry prohibited framework metadata](dca-adv-018.md) — Domain objects carry no metadata for container management, persistence or transaction coordination.
