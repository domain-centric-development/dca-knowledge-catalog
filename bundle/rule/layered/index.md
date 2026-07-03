# layered

- [Application Services must only use outbound ports (not infrastructure implementations)](application-services-must-only-use-outbound-ports-not-infrastructure-implementations.md) — Application services should only use outbound ports from sharedkernel.application.port, not infrastructure implementa...
- [Domain must not have dependencies on Infrastructure](domain-must-not-have-dependencies-on-infrastructure.md) — Domain should not depend on infrastructure concerns (Dependency Inversion Principle).
- [sharedkernel.application.port should only contain interfaces (Outbound Ports)](sharedkernel-application-port-should-only-contain-interfaces-outbound-ports.md) — sharedkernel.marker.port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) .
- [The rules of the Layered Architecture should be followed](the-rules-of-the-layered-architecture-should-be-followed.md) — The rules of the Layered Architecture should be followed.
- [Transaction boundaries belong to the application layer](transaction-boundaries-belong-to-the-application-layer.md) — Transactions are an application-layer concern - domain and incoming adapters must not manage them.
