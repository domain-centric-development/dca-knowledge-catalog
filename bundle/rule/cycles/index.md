# cycles

- [Domain Packages must not have cyclic dependencies (package-based slice discovery)](dca-cyc-001.md) — Domain model packages should have clear boundaries and no cycles (Acyclic Dependencies Principle).
- [Application Layer must not have cyclic dependencies (package-based slice discovery)](dca-cyc-002.md) — Application services should have clear boundaries and no cycles.
- [Outgoing Adapter Packages must not have cyclic dependencies](dca-cyc-003.md) — Outgoing adapters should have clear boundaries and no cycles.
- [Incoming Adapter Packages must not have cyclic dependencies](dca-cyc-004.md) — Incoming adapters should have clear boundaries and no cycles.
- [Feature and use case packages within a module's application layer must not have cyclic dependencies](dca-cyc-005.md) — The packages directly below a module's application package are its features (application.<feature>.<usecase>) or, in ...
