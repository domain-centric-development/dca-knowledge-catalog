# tactical

- [Aggregate Roots must implement AggregateRoot<T, ID>](aggregate-roots-must-implement-aggregateroot-t-id.md) — Classes named *AggregateRoot must implement AggregateRoot interface (DDD pattern).
- [Aggregate Roots must not have fields with other Aggregate Root types](aggregate-roots-must-not-have-fields-with-other-aggregate-root-types.md) — Aggregate Roots must not have fields with other Aggregate Root types.
- [Aggregate Roots must not hold references to Repositories or other Output Ports](aggregate-roots-must-not-hold-references-to-repositories-or-other-output-ports.md) — Aggregate Roots must not hold references to Repositories or other Output Ports.
- [Domain model classes must not have public setter methods](domain-model-classes-must-not-have-public-setter-methods.md) — Domain model classes must not have public setter methods.
- [Enriched Domain Models must be Value Object records](enriched-domain-models-must-be-value-object-records.md) — Enriched domain models are immutable read projections and must be records implementing Value.
- [Entities must have an ID field](entities-must-have-an-id-field.md) — Entities must have an ID field.
- [Entities must not be instantiated directly from outside the aggregate](entities-must-not-be-instantiated-directly-from-outside-the-aggregate.md) — Entities must not be instantiated directly from outside the aggregate.
- [Entities must not have fields with Aggregate Root types](entities-must-not-have-fields-with-aggregate-root-types.md) — Entities must not have fields with Aggregate Root types.
- [Records for Value Objects are allowed (preferred pattern for simple Value Objects)](records-for-value-objects-are-allowed-preferred-pattern-for-simple-value-objects.md) — Records are a valid pattern for immutable value objects (Java 14+).
- [Repositories must only exist for Aggregate Roots](repositories-must-only-exist-for-aggregate-roots.md) — Repositories must only exist for Aggregate Roots.
- [Repository Implementations must reside in adapter.outgoing package](repository-implementations-must-reside-in-adapter-outgoing-package.md) — Repository implementations are outgoing adapters in bounded contexts.
- [Repository interfaces must reside in the application layer's shared output-port package](repository-interfaces-must-reside-in-the-application-layer-s-shared-output-port-package.md) — Repository interfaces are output ports in the application layer (Hexagonal Architecture).
- [Repository Interfaces should extend Repository Marker Interface](repository-interfaces-should-extend-repository-marker-interface.md) — Repository interfaces should extend Repository marker interface.
- [Repository methods must return Aggregate Roots](repository-methods-must-return-aggregate-roots.md) — Repository methods must return Aggregate Roots.
- [Value Object classes should be final (immutability)](value-object-classes-should-be-final-immutability.md) — Value objects should be immutable (final classes) - Vernon's DDD recommendation.
- [Value Object fields must be final (deep immutability)](value-object-fields-must-be-final-deep-immutability.md) — Value Object fields must be final (deep immutability).
- [Value Objects must not contain Aggregate Roots or Entities](value-objects-must-not-contain-aggregate-roots-or-entities.md) — Value Objects must not contain Aggregate Roots or Entities.
- [Value Objects must not have setter methods](value-objects-must-not-have-setter-methods.md) — Value Objects must not have setter methods.
