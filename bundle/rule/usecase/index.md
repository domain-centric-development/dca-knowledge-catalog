# usecase

- [Base InputPort interface must be in the building-blocks port in package](base-inputport-interface-must-be-in-the-building-blocks-port-in-package.md) — Base InputPort interface defines the generic contract for all use cases (Hexagonal Architecture).
- [DTOs must not be used in the Application Layer](dtos-must-not-be-used-in-the-application-layer.md) — Application layer should use Command/Query/Response models, not presentation DTOs (Clean Architecture).
- [DTOs must not be used in the Domain Layer](dtos-must-not-be-used-in-the-domain-layer.md) — Domain layer should not depend on DTOs (presentation concerns) - Dependency Inversion Principle.
- [HTTP Response Models must end with 'Response' and reside in adapter incoming package](http-response-models-must-end-with-response-and-reside-in-adapter-incoming-package.md) — HTTP response models should be in adapter incoming layer.
- [Use Case Commands must end with 'Command' and reside in application package](use-case-commands-must-end-with-command-and-reside-in-application-package.md) — Use case commands should be in application layer (CQRS pattern).
- [Use Case Commands should be immutable (final or records)](use-case-commands-should-be-immutable-final-or-records.md) — Use case commands should be immutable (value objects).
- [Use Case Queries must end with 'Query' and reside in application package](use-case-queries-must-end-with-query-and-reside-in-application-package.md) — Use case queries should be in application layer (CQRS pattern).
- [Use Case Queries should be immutable (final or records)](use-case-queries-should-be-immutable-final-or-records.md) — Use case queries should be immutable (value objects).
- [Use Case Result Models must end with 'Result' and reside in application package](use-case-result-models-must-end-with-result-and-reside-in-application-package.md) — Use case result models should be in application layer. Domain Value Objects with 'Result' in name are allowed in doma...
- [Use Case Result Models should be immutable (final or records)](use-case-result-models-should-be-immutable-final-or-records.md) — Use case result models should be immutable (value objects).
- [Use cases that publish domain events must be transactional](use-cases-that-publish-domain-events-must-be-transactional.md) — Integration events are relayed after commit (@TransactionalEventListener, @ApplicationModuleListener) and their publi...
- [Use cases that save an aggregate must publish its domain events](use-cases-that-save-an-aggregate-must-publish-its-domain-events.md) — A saved aggregate must not keep its events: unpublished, they are lost, and stored on the instance they may later be ...
