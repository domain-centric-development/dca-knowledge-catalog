# layered

- [Application Services must only use outbound ports (not infrastructure implementations)](application-services-must-only-use-outbound-ports-not-infrastructure-implementations.md) — Application services should only use outbound ports declared as interfaces (sharedkernel.marker.port.out), not infras...
- [Domain must not have dependencies on Infrastructure](domain-must-not-have-dependencies-on-infrastructure.md) — Domain should not depend on infrastructure concerns (Dependency Inversion Principle).
- [The rules of the Layered Architecture should be followed](the-rules-of-the-layered-architecture-should-be-followed.md) — The rules of the Layered Architecture should be followed.
- [The shared kernel's output-port markers must all be interfaces](the-shared-kernel-s-output-port-markers-must-all-be-interfaces.md) — sharedkernel.marker.port.out contains outbound port interfaces (Repository, OutputPort, DomainEventPublisher) .
- [Transaction boundaries belong to the application layer](transaction-boundaries-belong-to-the-application-layer.md) — Transactions are an application-layer concern - domain and incoming adapters must not manage them.
